"""Dashboard Type 4 - Service-Errors Filter Known Issues automation."""


class DashboardType4Automation:
    """Automation logic for Dashboard Type 4 - Service-Errors Filter Known Issues."""
    
    def __init__(self, page, environment=None):
        """Initialize with Playwright page object."""
        self.page = page
        self.dashboard_name = "Service-Errors Filter Known Issues"
        self.result = None
        self.environment = environment
        self.widgets = []  # List of {"name": str, "errors": list} dicts
        # Widget names to extract - order will be discovered dynamically
        self.widget_names = ["charger", "keysmith", "neptune", "roundup", "zinc"]

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

    async def _wait_for_widget_loaded(self, widget_element, heading):
        """Wait until a widget finishes loading its content."""
        try:
            print(f"[Type 4] Waiting for widget to load: {heading}")
            max_wait = 15  # Reduced from 30 to 15 seconds
            for i in range(max_wait):
                try:
                    # No results indicator
                    no_results = widget_element.locator('div.text-deemphasized').filter(has_text="Search completed. No results found")
                    if await no_results.count() > 0:
                        print(f"[Type 4] {heading}: Widget loaded (no results)")
                        return True

                    # Table presence with rows
                    rows = widget_element.locator('table > tbody > tr')
                    row_count = await rows.count()
                    if row_count > 0:
                        print(f"[Type 4] {heading}: Widget loaded ({row_count} rows)")
                        return True

                    # Table visible (even if empty yet)
                    table = widget_element.locator("div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table")
                    if await table.is_visible():
                        print(f"[Type 4] {heading}: Widget loaded (table visible)")
                        return True
                    
                    # Log progress every 3 seconds
                    if i > 0 and i % 3 == 0:
                        print(f"[Type 4] {heading}: Still waiting... ({i}s elapsed)")
                        
                except Exception as e:
                    if i == 0:
                        print(f"[Type 4] {heading}: Initial check error: {e}")
                    pass

                await self.page.wait_for_timeout(1000)

            print(f"[Type 4] {heading}: Widget load timeout after {max_wait}s - proceeding anyway")
            return True  # Changed to True to proceed even on timeout
        except Exception as e:
            print(f"[Type 4] {heading}: Widget load check failed: {e} - proceeding anyway")
            return True  # Proceed even on error

    async def extract_widget(self, widget_id, title_selector, content_selector, widget_name):
        """Extract a single widget's title and errors.
        
        Args:
            widget_id: Widget ID (without widget_box__ prefix)
            title_selector: CSS selector for widget title
            content_selector: CSS selector for content area (text when no errors)
            widget_name: Display name for the widget
            
        Returns:
            dict with 'name' and 'errors' keys
        """
        print(f"[Type 4] Extracting widget: {widget_name}...")
        errors = []
        
        try:
            # Wait for widget to be visible
            widget = self.page.locator(f"#widget_box__{widget_id}")
            await widget.wait_for(state="visible", timeout=10000)
            await widget.scroll_into_view_if_needed(timeout=5000)
            await self.page.wait_for_timeout(1500)
            
            # Try to get the title (use widget_name as fallback)
            display_name = widget_name
            try:
                title_element = self.page.locator(title_selector)
                display_name = await title_element.inner_text(timeout=3000)
                print(f"[Type 4] Widget title: {display_name}")
            except:
                print(f"[Type 4] Using default name: {widget_name}")
            
            # Check the content area for "No results found" message
            try:
                content_div = self.page.locator(content_selector)
                await content_div.wait_for(state="visible", timeout=3000)
                content_text = await content_div.inner_text(timeout=2000)
                
                if "Search completed. No results found" in content_text or "No results found" in content_text:
                    print(f"[Type 4] {display_name}: No errors found")
                    return {"name": display_name, "errors": []}
            except:
                # Content div not found, might have table instead
                pass
            
            # Try to extract from table
            try:
                print(f"[Type 4] Looking for table data in {display_name}...")
                table_selector = f"#widget_box__{widget_id} > div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table > tbody"
                tbody = self.page.locator(table_selector)
                await tbody.wait_for(state="visible", timeout=3000)
                
                rows = tbody.locator("tr")
                row_count = await rows.count()
                
                if row_count > 0:
                    print(f"[Type 4] Extracting {row_count} rows from {display_name}")
                    for i in range(min(row_count, 200)):
                        try:
                            row = rows.nth(i)
                            await row.scroll_into_view_if_needed(timeout=2000)
                            # Try specific cell selector first
                            error_cell = row.locator("td.last\\:w-full.text-titles-and-attributes.relative.text-left > div > a")
                            error_text = await error_cell.inner_text(timeout=1500)
                            if error_text.strip():
                                errors.append(error_text.strip())
                        except:
                            # Fallback to entire row text
                            try:
                                row_text = await rows.nth(i).inner_text(timeout=1500)
                                if row_text.strip():
                                    errors.append(row_text.strip())
                            except:
                                continue
                    
                    print(f"[Type 4] Extracted {len(errors)} errors from {display_name}")
            except Exception as e:
                print(f"[Type 4] No table found in {display_name}: {e}")
            
            return {"name": display_name, "errors": errors}
            
        except Exception as e:
            print(f"[Type 4] Error extracting widget {widget_name}: {e}")
            return {"name": widget_name, "errors": []}

    async def _extract_widget_errors(self, widget):
        """Extract error lines from a widget container."""
        try:
            await widget.scroll_into_view_if_needed(timeout=5000)
        except:
            await self.page.evaluate("window.scrollBy(0, 2000)")
            await self.page.wait_for_timeout(500)

        # No results check
        try:
            no_results = widget.locator('div.text-deemphasized').filter(has_text="Search completed. No results found")
            await no_results.wait_for(timeout=1500)
            return []
        except:
            pass

        # Table-based extraction
        try:
            rows = widget.locator('table > tbody > tr')
            row_count = await rows.count()
            if row_count > 0:
                errors = []
                for i in range(min(row_count, 20)):
                    try:
                        row_text = await rows.nth(i).inner_text(timeout=1500)
                        if row_text.strip():
                            errors.append(row_text.strip())
                    except:
                        continue
                return errors
        except:
            pass

        # Fallback: extract text lines from widget content
        try:
            content = await widget.inner_text(timeout=2000)
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            # Remove generic phrases
            filtered = [line for line in lines if "Search completed" not in line and "No results found" not in line]
            return filtered
        except:
            return []

    async def extract_charger_errors_from_widget(self):
        """Extract charger errors from the specific widget with ID e3ed716e-b03e-4ec8-beb9-59956a659f00."""
        try:
            print("[Type 4] Waiting for charger errors widget to load...")
            
            # Select the specific charger errors widget
            widget = self.page.locator("#widget_box__e3ed716e-b03e-4ec8-beb9-59956a659f00")
            await widget.wait_for(state="visible", timeout=10000)
            print("[Type 4] Widget is visible, waiting for content to load...")
            
            # Scroll widget into view
            try:
                await widget.scroll_into_view_if_needed(timeout=5000)
            except:
                await self.page.evaluate("window.scrollBy(0, 2000)")
            
            # Wait for widget content to load (either table or "no results" message)
            await self.page.wait_for_timeout(2000)
            
            # Wait for the widget content area to be ready
            content_area = widget.locator("div.widget-box__content.z-40")
            await content_area.wait_for(state="visible", timeout=5000)
            print("[Type 4] Widget content area loaded")
            
            # Additional wait to ensure data is fully rendered
            await self.page.wait_for_timeout(1500)
            
            # Extract the widget title
            try:
                title_selector = "#widget_box__e3ed716e-b03e-4ec8-beb9-59956a659f00 > div.group.flex.flex-initial.items-center.justify-between.space-x-3.rounded-t.p-3.w-full > div.flex.items-center.space-x-1.min-w-0 > a > h2"
                title_element = self.page.locator(title_selector)
                widget_title = await title_element.inner_text(timeout=2000)
                print(f"[Type 4] Found charger widget: {widget_title}")
            except Exception as e:
                print(f"[Type 4] Could not extract widget title: {e}")
                widget_title = "Charger Errors"
            
            # Check for errors in the content area
            content_selector = "#widget_box__e3ed716e-b03e-4ec8-beb9-59956a659f00 > div.widget-box__content.z-40 > div > div.text-deemphasized.w-full.h-full.flex.items-center.justify-center.border-t.border-normal.shadow-base.shadow-inner-md"
            content_div = self.page.locator(content_selector)
            
            try:
                # Check if "No results found" message is displayed
                await content_div.wait_for(state="visible", timeout=3000)
                no_results_text = await content_div.inner_text(timeout=2000)
                if "Search completed. No results found" in no_results_text:
                    print(f"[Type 4] Charger errors widget: No errors found")
                    return {"title": widget_title, "errors": [], "has_results": False}
            except:
                # Content div not found or not visible, might have table instead
                pass
            
            # Try to extract from table if it exists
            charger_errors = []
            try:
                print("[Type 4] Looking for table data in charger errors widget...")
                table = widget.locator("div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table")
                await table.wait_for(state="visible", timeout=5000)
                print("[Type 4] Table found, waiting for rows to load...")
                
                # Wait for table body to be populated
                tbody = table.locator("tbody")
                await tbody.wait_for(state="visible", timeout=3000)
                await self.page.wait_for_timeout(1000)
                
                rows = table.locator("tbody > tr")
                row_count = await rows.count()
                
                if row_count > 0:
                    print(f"[Type 4] Extracting {row_count} rows from charger errors table")
                    for i in range(min(row_count, 100)):  # Limit to 100 rows
                        try:
                            row_text = await rows.nth(i).inner_text(timeout=1500)
                            if row_text.strip():
                                charger_errors.append(row_text.strip())
                        except:
                            continue
                    
                    # Check for pagination (tab buttons at the bottom)
                    try:
                        pagination_buttons = widget.locator("div.widget-box__footer button[data-e2e*='button']")
                        button_count = await pagination_buttons.count()
                        if button_count > 0:
                            print(f"[Type 4] Found {button_count} pagination buttons, checking for additional pages...")
                            # Try to click next page buttons and extract more errors
                            for btn_idx in range(1, min(button_count, 5)):  # Check up to 5 pages
                                try:
                                    btn = pagination_buttons.nth(btn_idx)
                                    await btn.click(timeout=2000)
                                    print(f"[Type 4] Clicked pagination button {btn_idx}, waiting for page to load...")
                                    await self.page.wait_for_timeout(2000)  # Wait for new page data
                                    
                                    # Extract errors from new page
                                    new_rows = table.locator("tbody > tr")
                                    new_row_count = await new_rows.count()
                                    for i in range(min(new_row_count, 100)):
                                        try:
                                            row_text = await new_rows.nth(i).inner_text(timeout=1500)
                                            if row_text.strip() and row_text.strip() not in charger_errors:
                                                charger_errors.append(row_text.strip())
                                        except:
                                            continue
                                except:
                                    break
                    except:
                        pass
                    
                    print(f"[Type 4] Extracted {len(charger_errors)} charger errors total")
                    return {"title": widget_title, "errors": charger_errors, "has_results": True}
            except:
                pass
            
            # Fallback: try to extract text content
            try:
                all_content = await widget.inner_text(timeout=2000)
                lines = [line.strip() for line in all_content.splitlines() if line.strip()]
                filtered = [line for line in lines if "Search completed" not in line and "No results found" not in line]
                if filtered:
                    print(f"[Type 4] Extracted {len(filtered)} charger errors from text content")
                    return {"title": widget_title, "errors": filtered, "has_results": True}
            except:
                pass
            
            print(f"[Type 4] No charger errors data found")
            return {"title": widget_title, "errors": [], "has_results": False}
            
        except Exception as e:
            print(f"[Type 4] Error extracting charger errors: {e}")
            return {"title": "Charger Errors", "errors": [], "has_results": False}

    async def extract_service_errors(self):
        """Extract service-specific errors for zinc-app, roundup, neptune, keysmith (charger handled separately)."""
        services = ["zinc-app", "roundup", "neptune", "keysmith"]
        results = {}

        for service in services:
            # Find widget containing the service name
            widget = self.page.locator("div.widget-box").filter(has_text=service).first
            try:
                if await widget.count() == 0:
                    results[service] = []
                    continue
            except:
                results[service] = []
                continue

            errors = await self._extract_widget_errors(widget)
            results[service] = errors

        self.service_errors = results
        return results
    
    async def extract_additional_widgets(self):
        """Extract errors from 4 additional widgets with specific IDs."""
        widget_configs = [
            {
                "id": "9cea05d9-a425-4e82-a001-767bd5ef1132",
                "title_selector": "#widget_box__9cea05d9-a425-4e82-a001-767bd5ef1132 > div.group.flex.flex-initial.items-center.justify-between.space-x-3.rounded-t.p-3.w-full > div.flex.items-center.space-x-1.min-w-0 > a > h2",
                "content_selector": "#widget_box__9cea05d9-a425-4e82-a001-767bd5ef1132 > div.widget-box__content.z-40 > div > div.text-deemphasized.w-full.h-full.flex.items-center.justify-center.border-t.border-normal.shadow-base.shadow-inner-md",
                "type": "simple"
            },
            {
                "id": "54ac38aa-73b4-43b0-9de8-e9ca94a4a22f",
                "title_selector": "#widget_box__54ac38aa-73b4-43b0-9de8-e9ca94a4a22f > div.group.flex.flex-initial.items-center.justify-between.space-x-3.rounded-t.p-3.w-full > div.flex.items-center.space-x-1.min-w-0 > a > h2",
                "content_selector": "#widget_box__54ac38aa-73b4-43b0-9de8-e9ca94a4a22f > div.widget-box__content.z-40 > div > div.text-deemphasized.w-full.h-full.flex.items-center.justify-center.border-t.border-normal.shadow-base.shadow-inner-md",
                "type": "simple"
            },
            {
                "id": "173d8fc2-5b40-43a2-9821-55aa390c38d1",
                "title_selector": "#widget_box__173d8fc2-5b40-43a2-9821-55aa390c38d1 > div.group.flex.flex-initial.items-center.justify-between.space-x-3.rounded-t.p-3.w-full > div.flex.items-center.space-x-1.min-w-0 > a > h2",
                "content_selector": "#widget_box__173d8fc2-5b40-43a2-9821-55aa390c38d1 > div.widget-box__content.z-40 > div > div.text-deemphasized.w-full.h-full.flex.items-center.justify-center.border-t.border-normal.shadow-base.shadow-inner-md",
                "type": "simple"
            },
            {
                "id": "96ccea84-6792-4b32-8f90-e3627d4e38ac",
                "title_selector": "#widget_box__96ccea84-6792-4b32-8f90-e3627d4e38ac > div.group.flex.flex-initial.items-center.justify-between.space-x-3.rounded-t.p-3.w-full > div.flex.items-center.space-x-1.min-w-0 > a > h2",
                "content_selector": "#widget_box__96ccea84-6792-4b32-8f90-e3627d4e38ac > div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full",
                "pagination_selector": "#widget_box__96ccea84-6792-4b32-8f90-e3627d4e38ac > div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-initial.justify-between.py-0\\.5.px-6.overflow-auto > humio-resize-observer > ol",
                "type": "paginated"
            }
        ]
        
        results = {}
        
        for config in widget_configs:
            widget_id = config["id"]
            print(f"[Type 4] Processing widget {widget_id}...")
            
            try:
                # Wait for widget to be visible
                widget = self.page.locator(f"#widget_box__{widget_id}")
                await widget.wait_for(state="visible", timeout=10000)
                await widget.scroll_into_view_if_needed(timeout=5000)
                await self.page.wait_for_timeout(1500)
                
                # Extract title
                title = "Unknown Widget"
                try:
                    title_element = self.page.locator(config["title_selector"])
                    title = await title_element.inner_text(timeout=3000)
                    print(f"[Type 4] Widget title: {title}")
                except Exception as e:
                    print(f"[Type 4] Could not extract title for widget {widget_id}: {e}")
                
                # Extract errors based on widget type
                errors = []
                
                if config["type"] == "simple":
                    # Check for "No results found" or extract text content
                    try:
                        content_div = self.page.locator(config["content_selector"])
                        await content_div.wait_for(state="visible", timeout=3000)
                        content_text = await content_div.inner_text(timeout=2000)
                        
                        if "Search completed. No results found" in content_text:
                            print(f"[Type 4] {title}: No errors found")
                        else:
                            # Extract lines as errors
                            lines = [line.strip() for line in content_text.splitlines() if line.strip()]
                            filtered = [line for line in lines if "Search completed" not in line and "Searching" not in line]
                            if filtered:
                                errors = filtered
                                print(f"[Type 4] {title}: Found {len(errors)} errors")
                    except Exception as e:
                        print(f"[Type 4] Could not extract content from widget {widget_id}: {e}")
                
                elif config["type"] == "paginated":
                    # Handle widget with pagination
                    try:
                        print(f"[Type 4] Checking for paginated content in {title}...")
                        
                        # Wait for content area
                        content_area = self.page.locator(config["content_selector"])
                        await content_area.wait_for(state="visible", timeout=5000)
                        await self.page.wait_for_timeout(1000)
                        
                        # Look for pagination bar
                        try:
                            pagination_bar = self.page.locator(config["pagination_selector"])
                            await pagination_bar.wait_for(state="visible", timeout=3000)
                            
                            # Find all pagination buttons
                            page_buttons = pagination_bar.locator("li > button")
                            button_count = await page_buttons.count()
                            print(f"[Type 4] Found {button_count} pagination buttons")
                            
                            # Iterate through each page
                            for page_idx in range(button_count):
                                try:
                                    print(f"[Type 4] Clicking page {page_idx + 1}...")
                                    btn = page_buttons.nth(page_idx)
                                    await btn.click(timeout=3000)
                                    await self.page.wait_for_timeout(2000)  # Wait for page to load
                                    
                                    # Extract errors from table
                                    table_selector = f"#widget_box__{widget_id} > div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table > tbody"
                                    tbody = self.page.locator(table_selector)
                                    
                                    try:
                                        await tbody.wait_for(state="visible", timeout=3000)
                                        rows = tbody.locator("tr")
                                        row_count = await rows.count()
                                        
                                        for i in range(row_count):
                                            try:
                                                # Scroll the row into view to ensure it's fully rendered
                                                row = rows.nth(i)
                                                await row.scroll_into_view_if_needed(timeout=2000)
                                                
                                                # Extract error text from the specified column
                                                error_cell = row.locator("td.last\\:w-full.text-titles-and-attributes.relative.text-left > div > a")
                                                error_text = await error_cell.inner_text(timeout=1500)
                                                if error_text.strip() and error_text.strip() not in errors:
                                                    errors.append(error_text.strip())
                                                    print(f"[Type 4] Page {page_idx + 1} - Extracted: {error_text[:80]}...")
                                            except:
                                                # Try alternative extraction
                                                try:
                                                    row_text = await rows.nth(i).inner_text(timeout=1500)
                                                    if row_text.strip() and row_text.strip() not in errors:
                                                        errors.append(row_text.strip())
                                                        print(f"[Type 4] Page {page_idx + 1} - Extracted (alt): {row_text[:80]}...")
                                                except:
                                                    continue
                                    except:
                                        print(f"[Type 4] No table data found on page {page_idx + 1}")
                                
                                except Exception as e:
                                    print(f"[Type 4] Error processing page {page_idx + 1}: {e}")
                                    continue
                            
                            print(f"[Type 4] {title}: Extracted {len(errors)} total errors from {button_count} pages")
                        
                        except:
                            # No pagination, try direct table extraction
                            print(f"[Type 4] No pagination found, trying direct extraction...")
                            try:
                                table_selector = f"#widget_box__{widget_id} > div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table > tbody"
                                tbody = self.page.locator(table_selector)
                                await tbody.wait_for(state="visible", timeout=3000)
                                rows = tbody.locator("tr")
                                row_count = await rows.count()
                                
                                for i in range(min(row_count, 100)):
                                    try:
                                        row_text = await rows.nth(i).inner_text(timeout=1500)
                                        if row_text.strip():
                                            errors.append(row_text.strip())
                                    except:
                                        continue
                                
                                print(f"[Type 4] {title}: Found {len(errors)} errors")
                            except:
                                print(f"[Type 4] No table data found in {title}")
                    
                    except Exception as e:
                        print(f"[Type 4] Error extracting paginated content from {title}: {e}")
                
                results[title] = errors
                
            except Exception as e:
                print(f"[Type 4] Widget {widget_id} not found or error: {e}")
                continue
        
        return results
    
    async def _find_widget_by_title(self, title_text):
        """Find a widget by its heading text, regardless of order or ID."""
        try:
            print(f"[Type 4] Searching for '{title_text}' widget...")
            # Find all widget boxes
            all_widgets = self.page.locator("div[id^='widget_box__']")
            
            try:
                widget_count = await all_widgets.count()
                print(f"[Type 4] Found {widget_count} total widgets on page")
            except Exception as e:
                print(f"[Type 4] Error counting widgets: {e}")
                return {"found": False}
            
            for i in range(widget_count):
                widget = all_widgets.nth(i)
                try:
                    # Look for heading in the widget - use shorter timeout
                    heading = widget.locator("div.group.flex.flex-initial.items-center.justify-between > div.flex.items-center > a > h2")
                    heading_text = await heading.inner_text(timeout=800)  # Reduced from 2000ms
                    
                    if i < 3:  # Log first 3 widget headings to help debug
                        print(f"[Type 4]   Widget {i+1}: '{heading_text}'")
                    
                    # Check if heading matches (case-insensitive, partial match)
                    if title_text.lower() in heading_text.lower():
                        # Extract widget ID from the parent div
                        widget_id_attr = await widget.get_attribute("id", timeout=500)
                        if widget_id_attr and widget_id_attr.startswith("widget_box__"):
                            widget_id = widget_id_attr.replace("widget_box__", "")
                            print(f"[Type 4] ✓ Found '{title_text}' widget: ID={widget_id}, heading='{heading_text}'")
                            return {
                                "widget_element": widget,
                                "widget_id": widget_id,
                                "heading": heading_text,
                                "found": True
                            }
                except Exception as e:
                    # Skip widgets that timeout or have errors
                    if i < 3:  # Only log first few errors
                        print(f"[Type 4]   Widget {i+1}: Skipping (error reading heading)")
                    continue
            
            print(f"[Type 4] ✗ Widget '{title_text}' not found")
            return {"found": False}
        
        except Exception as e:
            print(f"[Type 4] Error searching for widget '{title_text}': {e}")
            return {"found": False}

    async def run_checks(self):
        """Run dashboard-specific checks and automation."""
        print("\n" + "="*60)
        print("Running Dashboard Type 4 checks...")
        print(f"[Type 4] Environment: {self.environment}")
        print("="*60)
        
        # Wait for dashboard to fully load
        print(f"[Type 4] Step 1/3: Waiting for dashboard to load...")
        await self._wait_for_dashboard_load()
        await self.page.wait_for_timeout(1000)
        print(f"[Type 4] ✓ Dashboard loaded")
        
        # Dynamically discover widgets by heading text - order doesn't matter
        print(f"\n[Type 4] Step 2/3: Discovering widgets...")
        self.widgets = []
        print(f"[Type 4] Looking for {len(self.widget_names)} widgets: {', '.join(self.widget_names)}")
        
        for idx, widget_name in enumerate(self.widget_names, 1):
            print(f"\n[Type 4] Processing widget {idx}/{len(self.widget_names)}: {widget_name}")
            widget_info = await self._find_widget_by_title(widget_name)
            
            if widget_info.get("found"):
                # Extract data from this widget
                print(f"[Type 4] Extracting data from {widget_name}...")
                widget_data = await self._extract_widget_data(
                    widget_element=widget_info["widget_element"],
                    widget_id=widget_info["widget_id"],
                    widget_name=widget_name,
                    heading=widget_info["heading"]
                )
                self.widgets.append(widget_data)
                print(f"[Type 4] ✓ Completed {widget_name}: {len(widget_data.get('errors', []))} errors")
            else:
                print(f"[Type 4] ✗ Skipping {widget_name} - not found on dashboard")
        
        print(f"\n[Type 4] Step 3/3: Finalizing...")
        print(f"[Type 4] Successfully extracted {len(self.widgets)} widgets")
        self.result = f"   ✓ {self.dashboard_name} - Completed"
        print(self.result)
        print("="*60 + "\n")
        return self.result
    
    async def _check_and_handle_pagination(self, widget_element, widget_id, heading):
        """Check if widget has pagination and extract errors from all pages.
        
        Returns:
            list of error strings from all pages
        """
        errors = []
        
        try:
            print(f"[Type 4] {heading}: Checking for pagination buttons...")
            
            # Look for pagination buttons in the widget footer
            # The buttons have data-e2e="pagination-page" attribute
            pagination_buttons = widget_element.locator('button[data-e2e="pagination-page"]')
            
            # Use a short timeout for checking pagination existence
            try:
                button_count = await pagination_buttons.count()
            except:
                print(f"[Type 4] {heading}: Pagination check timed out, assuming no pagination")
                return errors
            
            if button_count <= 1:
                print(f"[Type 4] {heading}: No pagination found (only {button_count} button(s))")
                return errors
            
            print(f"[Type 4] {heading}: ✓ Found pagination with {button_count} page buttons")
            
            # Extract errors from all pages
            for page_idx in range(button_count):
                try:
                    print(f"[Type 4] {heading}: Processing page {page_idx + 1}/{button_count}...")
                    
                    # Get the button fresh each time (in case DOM changes)
                    btn = widget_element.locator('button[data-e2e="pagination-page"]').nth(page_idx)
                    
                    # Scroll button into view
                    try:
                        await btn.scroll_into_view_if_needed(timeout=1000)
                    except:
                        pass
                    
                    # Check if button is already active (aria-current="true")
                    is_current = None
                    try:
                        is_current = await btn.get_attribute("aria-current", timeout=1000)
                    except:
                        pass
                    
                    if is_current == "true":
                        print(f"[Type 4] {heading}: Page {page_idx + 1} already active")
                    else:
                        # Click the page button
                        print(f"[Type 4] {heading}: Clicking page {page_idx + 1}...")
                        try:
                            await btn.click(timeout=2000)
                            await self.page.wait_for_timeout(2000)  # Wait for data to load
                        except Exception as e:
                            print(f"[Type 4] {heading}: Could not click page {page_idx + 1}: {e}")
                            continue
                    
                    # Extract errors from current page table
                    table_selector = f"#widget_box__{widget_id} table tbody"
                    tbody = self.page.locator(table_selector)
                    
                    try:
                        await tbody.wait_for(state="visible", timeout=2000)
                        rows = tbody.locator("tr")
                        row_count = await rows.count()
                        
                        print(f"[Type 4] {heading}: Page {page_idx + 1} - Found {row_count} rows")
                        
                        for i in range(row_count):
                            try:
                                row = rows.nth(i)
                                
                                # Try to extract from the last column with data
                                try:
                                    # Try link in cell first
                                    error_link = row.locator("td:last-child div > a")
                                    error_text = await error_link.inner_text(timeout=1000)
                                    if error_text.strip():
                                        if error_text.strip() not in errors:
                                            errors.append(error_text.strip())
                                        continue
                                except:
                                    pass
                                
                                # Try to get text from last td that has content
                                cells = row.locator("td")
                                cell_count = await cells.count()
                                
                                for cell_idx in range(cell_count - 1, -1, -1):
                                    try:
                                        cell = cells.nth(cell_idx)
                                        cell_text = await cell.inner_text(timeout=1000)
                                        if cell_text.strip():
                                            if cell_text.strip() not in errors:
                                                errors.append(cell_text.strip())
                                            break
                                    except:
                                        continue
                                        
                            except:
                                continue
                    
                    except Exception as e:
                        print(f"[Type 4] {heading}: Could not extract data from page {page_idx + 1}: {e}")
                
                except Exception as e:
                    print(f"[Type 4] {heading}: Error processing page {page_idx + 1}: {e}")
                    continue
            
            print(f"[Type 4] {heading}: ✓ Extracted {len(errors)} unique errors from {button_count} pages")
            return errors
            
        except Exception as e:
            print(f"[Type 4] {heading}: Pagination check error: {e}")
            return errors

    async def _extract_widget_data(self, widget_element, widget_id, widget_name, heading):
        """Extract error data from a discovered widget."""
        errors = []
        try:
            # Scroll widget into view with shorter timeout
            try:
                await widget_element.scroll_into_view_if_needed(timeout=2000)  # Reduced from 5000ms
            except:
                print(f"[Type 4] {heading}: Could not scroll into view, proceeding anyway")
            
            await self.page.wait_for_timeout(500)

            # Wait until widget content is loaded before extraction
            await self._wait_for_widget_loaded(widget_element, heading)
            
            # Check for "No results" message
            try:
                no_results = widget_element.locator('div.text-deemphasized').filter(has_text="Search completed. No results found")
                await no_results.wait_for(timeout=1000)  # Reduced from 2000ms
                print(f"[Type 4] {heading}: No errors found")
                return {"name": heading, "errors": []}
            except:
                pass
            
            # Try to extract from table - first check for pagination
            try:
                table = widget_element.locator("div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table")
                await table.wait_for(state="visible", timeout=2000)  # Reduced from 3000ms
                
                # Check for pagination and handle if found
                paginated_errors = await self._check_and_handle_pagination(widget_element, widget_id, heading)
                if paginated_errors:
                    errors = paginated_errors
                else:
                    # No pagination, extract from current page only
                    rows = table.locator("tbody > tr")
                    row_count = await rows.count()
                    
                    if row_count > 0:
                        print(f"[Type 4] {heading}: Found {row_count} rows (no pagination)")
                        for i in range(min(row_count, 200)):
                            try:
                                row = rows.nth(i)
                                # Try to get error text from link in last column
                                try:
                                    error_cell = row.locator("td.last\\:w-full.text-titles-and-attributes.relative.text-left > div > a")
                                    error_text = await error_cell.inner_text(timeout=800)  # Reduced from 1500ms
                                    if error_text.strip():
                                        errors.append(error_text.strip())
                                except:
                                    # Fallback to entire row
                                    row_text = await row.inner_text(timeout=800)  # Reduced from 1500ms
                                    if row_text.strip():
                                        errors.append(row_text.strip())
                            except:
                                continue
            except:
                print(f"[Type 4] {heading}: No table found")
            
            print(f"[Type 4] {heading}: Extracted {len(errors)} errors total")
            return {"name": heading, "errors": errors}
        
        except Exception as e:
            print(f"[Type 4] Error extracting {heading}: {e}")
            return {"name": heading, "errors": []}
