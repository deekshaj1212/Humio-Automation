"""Dashboard Type 4 - Service-Errors Filter Known Issues automation.

This module extracts error data from service-specific widgets on the Type 4 dashboard.
Each widget contains a table with error names and their occurrence counts.
"""


class DashboardType4Automation:
    """Automation logic for Dashboard Type 4 - Service-Errors Filter Known Issues."""
    
    def __init__(self, page, environment=None):
        """Initialize with Playwright page object."""
        self.page = page
        self.dashboard_name = "Service-Errors Filter Known Issues"
        self.environment = environment
        self.service_errors = {}  # Dictionary to store errors by service name

    async def _wait_for_dashboard_load(self):
        """Wait for the dashboard loading bar to complete (100% width)."""
        try:
            print("[Type 4] Waiting for dashboard to load completely...")
            loading_bar = self.page.locator("#humio-doc > div > div > div.h-px.flex-1.flex.items-stretch > div > div > div.dashboard__top-panel > div > div > div.absolute.inset-x-0.top-0 > div > div")

            # Wait for progress bar container to appear - with shorter timeout
            try:
                await loading_bar.wait_for(state="visible", timeout=5000)
                print("[Type 4] Loading bar detected")
            except Exception as e:
                print(f"[Type 4] Loading bar not found: {e}")
                print("[Type 4] Using fallback wait (3 seconds)...")
                await self.page.wait_for_timeout(3000)
                return True

            # Wait for progress bar to reach 100% width
            max_wait = 30  # Maximum 30 seconds (reduced from 60)
            for i in range(max_wait):
                try:
                    progress_bar = loading_bar.locator("div.progress-bar__progress")
                    style_attr = await progress_bar.get_attribute("style", timeout=1000)

                    if style_attr and "width: 100%" in style_attr:
                        print("[Type 4] Dashboard fully loaded (100%)")
                        await self.page.wait_for_timeout(1000)
                        return True

                    if style_attr and "width:" in style_attr:
                        width_match = style_attr.split("width:")[1].split(";")[0].strip()
                        if i % 5 == 0:
                            print(f"[Type 4] Loading... ({width_match})")

                    await self.page.wait_for_timeout(1000)
                except Exception as e:
                    if i == 0:
                        print(f"[Type 4] Error checking progress: {e}")
                    await self.page.wait_for_timeout(1000)
                    continue

            print("[Type 4] Loading bar did not reach 100% within timeout, proceeding anyway...")
            return True

        except Exception as e:
            print(f"[Type 4] Dashboard load check failed: {e}, proceeding anyway...")
            await self.page.wait_for_timeout(3000)
            return True

    async def _extract_charger_errors(self):
        """Extract Charger-Errors widget data.
        
        Widget ID: e3ed716e-b03e-4ec8-beb9-59956a659f00
        Table columns: Column 1 = error name, Column 2 = count
        
        Returns:
            dict with 'name' and 'errors' keys
            errors is a list of 'error_name - occurred X times' strings
        """
        try:
            print("[Type 4] Extracting Charger-Errors widget...")
            
            widget_id = "e3ed716e-b03e-4ec8-beb9-59956a659f00"
            widget = self.page.locator(f"#widget_box__{widget_id}")
            
            # Wait for widget to be visible
            await widget.wait_for(state="visible", timeout=10000)
            await widget.scroll_into_view_if_needed(timeout=5000)
            await self.page.wait_for_timeout(1000)
            
            # Extract widget title
            title_selector = f"#widget_box__{widget_id} > div.group.flex.flex-initial.items-center.justify-between.space-x-3.rounded-t.p-3.w-full.hover\\:overflow-visible > div.flex.items-center.space-x-1.min-w-0 > a > h2"
            title = "Charger-Errors"
            try:
                title = await self.page.locator(title_selector).inner_text(timeout=3000)
                print(f"[Type 4] Found widget title: '{title}'")
            except Exception as e:
                print(f"[Type 4] Could not extract title: {e}, using default")
            
            # Check for "No results found" message
            try:
                no_results = widget.locator('div.text-deemphasized').filter(has_text="Search completed. No results found")
                await no_results.wait_for(timeout=2000)
                print(f"[Type 4] {title}: No results found")
                return {"name": title, "errors": []}
            except:
                pass
            
            # Extract errors from table
            errors_dict = {}  # Dictionary to store error_name: count mapping
            
            try:
                # Wait for table to be visible
                table = widget.locator("div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table")
                await table.wait_for(state="visible", timeout=5000)
                
                # Wait for table body to have rows
                tbody = table.locator("tbody")
                await tbody.wait_for(state="visible", timeout=3000)
                
                # Get all rows
                rows = tbody.locator("tr")
                row_count = await rows.count()
                
                print(f"[Type 4] {title}: Found {row_count} rows")
                
                # Extract error name and count from each row
                for i in range(row_count):
                    try:
                        row = rows.nth(i)
                        
                        # Column 1: Error string
                        col1_cell = row.locator("td:nth-child(1)")
                        error_name = await col1_cell.inner_text(timeout=2000)
                        error_name = error_name.strip()
                        
                        # Column 2: Count
                        col2_cell = row.locator("td:nth-child(2)")
                        count_text = await col2_cell.inner_text(timeout=2000)
                        count_text = count_text.strip()
                        
                        # Parse count
                        try:
                            count = int(count_text)
                        except:
                            count = 1
                        
                        if error_name:
                            errors_dict[error_name] = count
                            print(f"[Type 4]   Row {i+1}: '{error_name}' - {count}")
                    
                    except Exception as e:
                        print(f"[Type 4] Error extracting row {i+1}: {e}")
                        continue
                
                # Format errors as "error_name - occurred X times"
                formatted_errors = []
                for error_name, count in errors_dict.items():
                    times = "time" if count == 1 else "times"
                    formatted_errors.append(f"{error_name} - occurred {count} {times}")
                
                print(f"[Type 4] {title}: Extracted {len(formatted_errors)} unique errors")
                return {"name": title, "errors": formatted_errors}
            
            except Exception as e:
                print(f"[Type 4] Error extracting table: {e}")
                return {"name": title, "errors": []}
        
        except Exception as e:
            print(f"[Type 4] Error in _extract_charger_errors: {e}")
            return {"name": "Charger-Errors", "errors": []}

    async def _extract_keysmith_errors(self):
        """Extract Keysmith-Errors widget data.
        
        Widget ID: 9cea05d9-a425-4e82-a001-767bd5ef1132
        Table columns: Column 1 = error name, Column 2 = count
        
        Returns:
            dict with 'name' and 'errors' keys
            errors is a list of 'error_name - occurred X times' strings
        """
        try:
            print("[Type 4] Extracting Keysmith-Errors widget...")
            
            widget_id = "9cea05d9-a425-4e82-a001-767bd5ef1132"
            widget = self.page.locator(f"#widget_box__{widget_id}")
            
            # Scroll widget into view
            try:
                await widget.scroll_into_view_if_needed(timeout=5000)
                print("[Type 4] Scrolled to Keysmith widget")
            except Exception as e:
                print(f"[Type 4] Could not scroll Keysmith widget: {e}")
            
            await self.page.wait_for_timeout(1000)
            
            # Wait for widget to be visible
            await widget.wait_for(state="visible", timeout=10000)
            await self.page.wait_for_timeout(500)
            
            # Extract widget title
            title_selector = f"#widget_box__{widget_id} > div.group.flex.flex-initial.items-center.justify-between.space-x-3.rounded-t.p-3.w-full.hover\\:overflow-visible > div.flex.items-center.space-x-1.min-w-0 > a > h2"
            title = "Keysmith-Errors"
            try:
                title = await self.page.locator(title_selector).inner_text(timeout=3000)
                print(f"[Type 4] Found widget title: '{title}'")
            except Exception as e:
                print(f"[Type 4] Could not extract title: {e}, using default")
            
            # Check for "No results found" message
            try:
                no_results = widget.locator('div.text-deemphasized').filter(has_text="Search completed. No results found")
                await no_results.wait_for(timeout=2000)
                print(f"[Type 4] {title}: No results found")
                return {"name": title, "errors": []}
            except:
                pass
            
            # Extract errors from table
            errors_dict = {}  # Dictionary to store error_name: count mapping
            
            try:
                # Wait for table to be visible
                table = widget.locator("div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table")
                await table.wait_for(state="visible", timeout=5000)
                
                # Wait for table body to have rows
                tbody = table.locator("tbody")
                await tbody.wait_for(state="visible", timeout=3000)
                
                # Get all rows
                rows = tbody.locator("tr")
                row_count = await rows.count()
                
                print(f"[Type 4] {title}: Found {row_count} rows")
                
                # Extract error name and count from each row
                for i in range(row_count):
                    try:
                        row = rows.nth(i)
                        
                        # Column 1: Error string
                        col1_cell = row.locator("td:nth-child(1)")
                        error_name = await col1_cell.inner_text(timeout=2000)
                        error_name = error_name.strip()
                        
                        # Column 2: Count
                        col2_cell = row.locator("td:nth-child(2)")
                        count_text = await col2_cell.inner_text(timeout=2000)
                        count_text = count_text.strip()
                        
                        # Parse count
                        try:
                            count = int(count_text)
                        except:
                            count = 1
                        
                        if error_name:
                            errors_dict[error_name] = count
                            print(f"[Type 4]   Row {i+1}: '{error_name}' - {count}")
                    
                    except Exception as e:
                        print(f"[Type 4] Error extracting row {i+1}: {e}")
                        continue
                
                # Format errors as "error_name - occurred X times"
                formatted_errors = []
                for error_name, count in errors_dict.items():
                    times = "time" if count == 1 else "times"
                    formatted_errors.append(f"{error_name} - occurred {count} {times}")
                
                print(f"[Type 4] {title}: Extracted {len(formatted_errors)} unique errors")
                return {"name": title, "errors": formatted_errors}
            
            except Exception as e:
                print(f"[Type 4] Error extracting table: {e}")
                return {"name": title, "errors": []}
        
        except Exception as e:
            print(f"[Type 4] Error in _extract_keysmith_errors: {e}")
            return {"name": "Keysmith-Errors", "errors": []}

    async def _extract_neptune_errors(self):
        """Extract Neptune-Errors widget data.
        
        Widget ID: 54ac38aa-73b4-43b0-9de8-e9ca94a4a22f
        Table columns: Column 1 = error name, Column 2 = count
        """
        try:
            print("[Type 4] Extracting Neptune-Errors widget...")
            
            widget_id = "54ac38aa-73b4-43b0-9de8-e9ca94a4a22f"
            widget = self.page.locator(f"#widget_box__{widget_id}")
            
            # Scroll widget into view
            try:
                await widget.scroll_into_view_if_needed(timeout=5000)
                print("[Type 4] Scrolled to Neptune widget")
            except:
                pass
            
            await self.page.wait_for_timeout(1000)
            await widget.wait_for(state="visible", timeout=10000)
            await self.page.wait_for_timeout(500)
            
            # Extract widget title
            title_selector = f"#widget_box__{widget_id} > div.group.flex.flex-initial.items-center.justify-between.space-x-3.rounded-t.p-3.w-full.hover\\:overflow-visible > div.flex.items-center.space-x-1.min-w-0 > a > h2"
            title = "Neptune-Errors"
            try:
                title = await self.page.locator(title_selector).inner_text(timeout=3000)
                print(f"[Type 4] Found widget title: '{title}'")
            except Exception as e:
                print(f"[Type 4] Could not extract title: {e}, using default")
            
            # Check for "No results found"
            try:
                no_results = widget.locator('div.text-deemphasized').filter(has_text="Search completed. No results found")
                await no_results.wait_for(timeout=2000)
                print(f"[Type 4] {title}: No results found")
                return {"name": title, "errors": []}
            except:
                pass
            
            # Extract errors from table
            errors_dict = {}
            
            try:
                table = widget.locator("div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table")
                await table.wait_for(state="visible", timeout=5000)
                tbody = table.locator("tbody")
                await tbody.wait_for(state="visible", timeout=3000)
                
                rows = tbody.locator("tr")
                row_count = await rows.count()
                print(f"[Type 4] {title}: Found {row_count} rows")
                
                for i in range(row_count):
                    try:
                        row = rows.nth(i)
                        col1_cell = row.locator("td:nth-child(1)")
                        error_name = await col1_cell.inner_text(timeout=2000)
                        error_name = error_name.strip()
                        
                        col2_cell = row.locator("td:nth-child(2)")
                        count_text = await col2_cell.inner_text(timeout=2000)
                        count_text = count_text.strip()
                        
                        try:
                            count = int(count_text)
                        except:
                            count = 1
                        
                        if error_name:
                            errors_dict[error_name] = count
                            print(f"[Type 4]   Row {i+1}: '{error_name}' - {count}")
                    except Exception as e:
                        print(f"[Type 4] Error extracting row {i+1}: {e}")
                        continue
                
                formatted_errors = []
                for error_name, count in errors_dict.items():
                    times = "time" if count == 1 else "times"
                    formatted_errors.append(f"{error_name} - occurred {count} {times}")
                
                print(f"[Type 4] {title}: Extracted {len(formatted_errors)} unique errors")
                return {"name": title, "errors": formatted_errors}
            
            except Exception as e:
                print(f"[Type 4] Error extracting table: {e}")
                return {"name": title, "errors": []}
        
        except Exception as e:
            print(f"[Type 4] Error in _extract_neptune_errors: {e}")
            return {"name": "Neptune-Errors", "errors": []}

    async def _extract_roundup_errors(self):
        """Extract Roundup-Errors widget data.
        
        Widget ID: 173d8fc2-5b40-43a2-9821-55aa390c38d1
        Table columns: Column 1 = error name, Column 2 = count
        """
        try:
            print("[Type 4] Extracting Roundup-Errors widget...")
            
            widget_id = "173d8fc2-5b40-43a2-9821-55aa390c38d1"
            widget = self.page.locator(f"#widget_box__{widget_id}")
            
            # Scroll widget into view
            try:
                await widget.scroll_into_view_if_needed(timeout=5000)
                print("[Type 4] Scrolled to Roundup widget")
            except:
                pass
            
            await self.page.wait_for_timeout(1000)
            await widget.wait_for(state="visible", timeout=10000)
            await self.page.wait_for_timeout(500)
            
            # Extract widget title
            title_selector = f"#widget_box__{widget_id} > div.group.flex.flex-initial.items-center.justify-between.space-x-3.rounded-t.p-3.w-full.hover\\:overflow-visible > div.flex.items-center.space-x-1.min-w-0 > a > h2"
            title = "Roundup-Errors"
            try:
                title = await self.page.locator(title_selector).inner_text(timeout=3000)
                print(f"[Type 4] Found widget title: '{title}'")
            except Exception as e:
                print(f"[Type 4] Could not extract title: {e}, using default")
            
            # Check for "No results found"
            try:
                no_results = widget.locator('div.text-deemphasized').filter(has_text="Search completed. No results found")
                await no_results.wait_for(timeout=2000)
                print(f"[Type 4] {title}: No results found")
                return {"name": title, "errors": []}
            except:
                pass
            
            # Extract errors from table
            errors_dict = {}
            
            try:
                table = widget.locator("div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table")
                await table.wait_for(state="visible", timeout=5000)
                tbody = table.locator("tbody")
                await tbody.wait_for(state="visible", timeout=3000)
                
                rows = tbody.locator("tr")
                row_count = await rows.count()
                print(f"[Type 4] {title}: Found {row_count} rows")
                
                for i in range(row_count):
                    try:
                        row = rows.nth(i)
                        col1_cell = row.locator("td:nth-child(1)")
                        error_name = await col1_cell.inner_text(timeout=2000)
                        error_name = error_name.strip()
                        
                        col2_cell = row.locator("td:nth-child(2)")
                        count_text = await col2_cell.inner_text(timeout=2000)
                        count_text = count_text.strip()
                        
                        try:
                            count = int(count_text)
                        except:
                            count = 1
                        
                        if error_name:
                            errors_dict[error_name] = count
                            print(f"[Type 4]   Row {i+1}: '{error_name}' - {count}")
                    except Exception as e:
                        print(f"[Type 4] Error extracting row {i+1}: {e}")
                        continue
                
                formatted_errors = []
                for error_name, count in errors_dict.items():
                    times = "time" if count == 1 else "times"
                    formatted_errors.append(f"{error_name} - occurred {count} {times}")
                
                print(f"[Type 4] {title}: Extracted {len(formatted_errors)} unique errors")
                return {"name": title, "errors": formatted_errors}
            
            except Exception as e:
                print(f"[Type 4] Error extracting table: {e}")
                return {"name": title, "errors": []}
        
        except Exception as e:
            print(f"[Type 4] Error in _extract_roundup_errors: {e}")
            return {"name": "Roundup-Errors", "errors": []}

    async def _extract_zinc_errors(self):
        """Extract Zinc-Errors widget data.
        
        Widget ID: 96ccea84-6792-4b32-8f90-e3627d4e38ac
        Table columns: Column 1 = error name, Column 2 = count
        Note: Table path includes 'div.flex.flex-col.flex-1.overflow-auto.h-full'
        """
        try:
            print("[Type 4] Extracting Zinc-Errors widget...")
            
            widget_id = "96ccea84-6792-4b32-8f90-e3627d4e38ac"
            widget = self.page.locator(f"#widget_box__{widget_id}")
            
            # Scroll widget into view
            try:
                await widget.scroll_into_view_if_needed(timeout=5000)
                print("[Type 4] Scrolled to Zinc widget")
            except:
                pass
            
            await self.page.wait_for_timeout(1000)
            await widget.wait_for(state="visible", timeout=10000)
            await self.page.wait_for_timeout(500)
            
            # Extract widget title
            title_selector = f"#widget_box__{widget_id} > div.group.flex.flex-initial.items-center.justify-between.space-x-3.rounded-t.p-3.w-full.hover\\:overflow-visible > div.flex.items-center.space-x-1.min-w-0 > a > h2"
            title = "Zinc-Errors"
            try:
                title = await self.page.locator(title_selector).inner_text(timeout=3000)
                print(f"[Type 4] Found widget title: '{title}'")
            except Exception as e:
                print(f"[Type 4] Could not extract title: {e}, using default")
            
            # Check for "No results found"
            try:
                no_results = widget.locator('div.text-deemphasized').filter(has_text="Search completed. No results found")
                await no_results.wait_for(timeout=2000)
                print(f"[Type 4] {title}: No results found")
                return {"name": title, "errors": []}
            except:
                pass
            
            # Extract errors from table (note: slightly different path with overflow-auto)
            errors_dict = {}
            
            try:
                table = widget.locator("div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table")
                await table.wait_for(state="visible", timeout=5000)
                tbody = table.locator("tbody")
                await tbody.wait_for(state="visible", timeout=3000)
                
                rows = tbody.locator("tr")
                row_count = await rows.count()
                print(f"[Type 4] {title}: Found {row_count} rows")
                
                for i in range(row_count):
                    try:
                        row = rows.nth(i)
                        col1_cell = row.locator("td:nth-child(1)")
                        error_name = await col1_cell.inner_text(timeout=2000)
                        error_name = error_name.strip()
                        
                        col2_cell = row.locator("td:nth-child(2)")
                        count_text = await col2_cell.inner_text(timeout=2000)
                        count_text = count_text.strip()
                        
                        try:
                            count = int(count_text)
                        except:
                            count = 1
                        
                        if error_name:
                            errors_dict[error_name] = count
                            print(f"[Type 4]   Row {i+1}: '{error_name}' - {count}")
                    except Exception as e:
                        print(f"[Type 4] Error extracting row {i+1}: {e}")
                        continue
                
                formatted_errors = []
                for error_name, count in errors_dict.items():
                    times = "time" if count == 1 else "times"
                    formatted_errors.append(f"{error_name} - occurred {count} {times}")
                
                print(f"[Type 4] {title}: Extracted {len(formatted_errors)} unique errors")
                return {"name": title, "errors": formatted_errors}
            
            except Exception as e:
                print(f"[Type 4] Error extracting table: {e}")
                return {"name": title, "errors": []}
        
        except Exception as e:
            print(f"[Type 4] Error in _extract_zinc_errors: {e}")
            return {"name": "Zinc-Errors", "errors": []}

    async def _extract_pll_count(self):
        """Extract PLL Count widget data.
        
        Widget ID: c5ffcf80-dfdc-4b3d-b34c-4c17fc6f0156
        This widget displays a single count, not a table of errors
        
        Returns:
            dict with 'name' and 'errors' keys
            errors is a list with a single string: "Pll detection Count - N" or "Pll detection Count - No errors"
        """
        try:
            print("[Type 4] Extracting PLL Count widget...")
            
            widget_id = "c5ffcf80-dfdc-4b3d-b34c-4c17fc6f0156"
            widget = self.page.locator(f"#widget_box__{widget_id}")
            
            # Scroll widget into view
            try:
                await widget.scroll_into_view_if_needed(timeout=5000)
                print("[Type 4] Scrolled to PLL Count widget")
            except:
                pass
            
            await self.page.wait_for_timeout(1000)
            await widget.wait_for(state="visible", timeout=10000)
            await self.page.wait_for_timeout(500)
            
            # Extract widget title
            title_selector = f"#widget_box__{widget_id} > div.group.flex.flex-initial.items-center.justify-between.space-x-3.rounded-t.p-3.w-full.hover\\:overflow-visible > div.flex.items-center.space-x-1.min-w-0 > a > h2"
            title = "PLL Detection Count"
            try:
                title = await self.page.locator(title_selector).inner_text(timeout=3000)
                print(f"[Type 4] Found widget title: '{title}'")
            except Exception as e:
                print(f"[Type 4] Could not extract title: {e}, using default")
            
            # Extract count from content area
            try:
                content_selector = f"#widget_box__{widget_id} > div.widget-box__content.z-40 > div > div.w-full.h-full > div > div > div"
                content_element = self.page.locator(content_selector)
                await content_element.wait_for(state="visible", timeout=5000)
                
                # Get the inner text which contains the count
                count_text = await content_element.inner_text(timeout=2000)
                count_text = count_text.strip()
                
                print(f"[Type 4] PLL Count widget content: '{count_text}'")
                
                # Try to parse as integer
                try:
                    count = int(count_text)
                except:
                    # If it's not a number, try to extract first number from text
                    import re
                    match = re.search(r'\d+', count_text)
                    if match:
                        count = int(match.group())
                    else:
                        count = 0
                
                # Format the output
                if count == 0:
                    message = f"{title} - No errors"
                else:
                    message = f"{title} - {count}"
                
                print(f"[Type 4] {title}: {message}")
                return {"name": title, "errors": [message]}
            
            except Exception as e:
                print(f"[Type 4] Error extracting PLL count: {e}")
                message = f"{title} - No errors"
                return {"name": title, "errors": [message]}
        
        except Exception as e:
            print(f"[Type 4] Error in _extract_pll_count: {e}")
            return {"name": "PLL Detection Count", "errors": ["PLL Detection Count - No errors"]}

    async def run_checks(self):
        """Main method to run all checks on the dashboard."""
        try:
            print(f"\n{'='*60}")
            print(f"[Type 4] Running Type 4 Dashboard Checks")
            print(f"[Type 4] Environment: {self.environment}")
            print(f"{'='*60}\n")
            
            # Step 1: Wait for dashboard to load
            print("[Type 4] Step 1/5: Waiting for dashboard to load...")
            await self._wait_for_dashboard_load()
            await self.page.wait_for_timeout(1000)
            
            # Step 2: Extract Charger-Errors widget
            print("[Type 4] Step 2/6: Extracting Charger-Errors widget...")
            charger_result = await self._extract_charger_errors()
            self.service_errors["charger"] = charger_result["errors"]
            
            # Step 3: Extract Keysmith-Errors widget
            print("[Type 4] Step 3/6: Extracting Keysmith-Errors widget...")
            keysmith_result = await self._extract_keysmith_errors()
            self.service_errors["keysmith"] = keysmith_result["errors"]
            
            # Step 4: Extract Neptune-Errors widget
            print("[Type 4] Step 4/6: Extracting Neptune-Errors widget...")
            neptune_result = await self._extract_neptune_errors()
            self.service_errors["neptune"] = neptune_result["errors"]
            
            # Step 5: Extract Roundup-Errors widget
            print("[Type 4] Step 5/6: Extracting Roundup-Errors widget...")
            roundup_result = await self._extract_roundup_errors()
            self.service_errors["roundup"] = roundup_result["errors"]
            
            # Step 6: Extract Zinc-Errors widget
            print("[Type 4] Step 6/6: Extracting Zinc-Errors widget...")
            zinc_result = await self._extract_zinc_errors()
            self.service_errors["zinc"] = zinc_result["errors"]
            
            # Step 7: Extract PLL Count widget
            print("[Type 4] Step 7/7: Extracting PLL Count widget...")
            pll_result = await self._extract_pll_count()
            self.service_errors["pll_count"] = pll_result["errors"]
            
            print(f"\n[Type 4] Checks completed successfully")
            print(f"{'='*60}\n")
            return True
        
        except Exception as e:
            print(f"[Type 4] Error during run_checks: {e}")
            return False
