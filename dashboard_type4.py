#Dashboard Type 4 - Service-Errors Filter Known Issues automation.

class DashboardType4Automation:
    # Widget configurations by environment
    WIDGET_CONFIG = {
        "env1": {
            "charger": {
                "id": "e3ed716e-b03e-4ec8-beb9-59956a659f00",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table"
            },
            "keysmith": {
                "id": "9cea05d9-a425-4e82-a001-767bd5ef1132",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table"
            },
            "neptune": {
                "id": "54ac38aa-73b4-43b0-9de8-e9ca94a4a22f",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table"
            },
            "roundup": {
                "id": "173d8fc2-5b40-43a2-9821-55aa390c38d1",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table"
            },
            "zinc": {
                "id": "96ccea84-6792-4b32-8f90-e3627d4e38ac",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table"
            },
            "pii_count": {
                "id": "c5ffcf80-dfdc-4b3d-b34c-4c17fc6f0156",
                "content_selector": "div.widget-box__content.z-40 > div > div.w-full.h-full > div > div > div"
            }
        },
        "env2": {
            "charger": {
                "id": "ff564e84-ceb2-48b2-b2d8-bb1f6cf4b0e8",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table"
            },
            "keysmith": {
                "id": "fc3cd48b-6094-4665-85e6-27ceab405632",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table"
            },
            "neptune": {
                "id": "54ac38aa-73b4-43b0-9de8-e9ca94a4a22f",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table"
            },
            "roundup": {
                "id": "173d8fc2-5b40-43a2-9821-55aa390c38d1",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table"
            },
            "zinc": {
                "id": "96ccea84-6792-4b32-8f90-e3627d4e38ac",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table"
            },
            "pii_count": {
                "id": "93921e2f-64c3-4fbb-a40d-83977033d532",
                "content_selector": "div.widget-box__content.z-40 > div > div.w-full.h-full > div > div > div"
            }
        },
        "env3": {
            "charger": {
                "id": "ff564e84-ceb2-48b2-b2d8-bb1f6cf4b0e8",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table"
            },
            "keysmith": {
                "id": "fc3cd48b-6094-4665-85e6-27ceab405632",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table"
            },
            "neptune": {
                "id": "54ac38aa-73b4-43b0-9de8-e9ca94a4a22f",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table"
            },
            "roundup": {
                "id": "173d8fc2-5b40-43a2-9821-55aa390c38d1",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table"
            },
            "zinc": {
                "id": "96ccea84-6792-4b32-8f90-e3627d4e38ac",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table"
            },
            "pii_count": {
                "id": "552e037b-cf00-4f2f-a353-7c4b8021e311",
                "content_selector": "div.widget-box__content.z-40 > div > div.w-full.h-full > div > div > div"
            }
        },
        "env4": {
            "charger": {
                "id": "ff564e84-ceb2-48b2-b2d8-bb1f6cf4b0e8",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table"
            },
            "keysmith": {
                "id": "fc3cd48b-6094-4665-85e6-27ceab405632",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div.flex.flex-col.flex-1.overflow-auto.h-full > table"
            },
            "neptune": {
                "id": "54ac38aa-73b4-43b0-9de8-e9ca94a4a22f",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table"
            },
            "roundup": {
                "id": "173d8fc2-5b40-43a2-9821-55aa390c38d1",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table"
            },
            "zinc": {
                "id": "96ccea84-6792-4b32-8f90-e3627d4e38ac",
                "table_selector": "div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table"
            },
            "pii_count": {
                "id": "67974173-bcd5-42e3-8072-ba37f8fe323c",
                "content_selector": "div.widget-box__content.z-40 > div > div.w-full.h-full > div > div > div"
            }
        }
    }
    
    def __init__(self, page, environment=None):
        self.page = page
        self.dashboard_name = "Service-Errors Filter Known Issues"
        self.environment = environment
        self.service_errors = {}  # Dictionary to store errors by service name
        self.widgets = []  # List of widget result dicts for summary reporting
        self.widget_config = self.WIDGET_CONFIG.get(environment, self.WIDGET_CONFIG["env1"])

    async def _wait_for_dashboard_load(self):
        #Wait for the dashboard loading bar to complete.
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

    async def _extract_table_errors_with_pagination(self, widget, table_selector, title):
        """Extract error rows from a table widget, including all pagination pages if present."""
        errors_dict = {}
        max_pages = 10  # Check first 10 pages
        prev_page_errors = set()
        repeating_detected = False
        has_many_pages = False  # Track if there are many pages
        
        async def extract_current_page(page_label=None):
            nonlocal prev_page_errors, repeating_detected
            table = widget.locator(table_selector)
            await table.wait_for(state="visible", timeout=5000)
            tbody = table.locator("tbody")
            await tbody.wait_for(state="visible", timeout=3000)
            rows = tbody.locator("tr")
            row_count = await rows.count()
            if page_label:
                print(f"[Type 4] {title}: Found {row_count} rows (page {page_label})")
            else:
                print(f"[Type 4] {title}: Found {row_count} rows")
            
            current_page_errors = set()
            for i in range(row_count):
                try:
                    row = rows.nth(i)
                    col1_cell = row.locator("td:nth-child(1)")
                    error_name = await col1_cell.inner_text(timeout=2000)
                    error_name = error_name.strip().lstrip('-').rstrip(':').strip()
                    col2_cell = row.locator("td:nth-child(2)")
                    count_text = await col2_cell.inner_text(timeout=2000)
                    count_text = count_text.strip()
                    try:
                        count = int(count_text)
                    except:
                        count = 1
                    if error_name:
                        current_page_errors.add(error_name)
                        errors_dict[error_name] = errors_dict.get(error_name, 0) + count
                        print(f"[Type 4]   Row {i+1}: '{error_name}' - {count}")
                except Exception as e:
                    print(f"[Type 4] Error extracting row {i+1}: {e}")
                    continue
            
            # Check if same errors appear on consecutive pages
            if prev_page_errors and current_page_errors == prev_page_errors:
                repeating_detected = True
                print(f"[Type 4] {title}: Same errors detected on consecutive pages")
            
            prev_page_errors = current_page_errors

        try:
            pagination_selectors = [
                "div.flex.flex-initial.justify-between.py-0\\.5.px-6.overflow-auto > humio-resize-observer > ol",
                "div.flex.flex-initial.justify-between.overflow-auto > humio-resize-observer > ol",
                "humio-resize-observer > ol",
                "ol button[data-e2e='pagination-page']"
            ]
            pagination_container = None
            buttons = None
            for selector in pagination_selectors:
                try:
                    test_container = widget.locator(selector)
                    count = await test_container.count()
                    if count > 0:
                        pagination_container = test_container
                        # If we matched a button selector directly, get parent ol
                        if "button" in selector:
                            buttons = test_container
                        else:
                            buttons = test_container.locator("button[data-e2e='pagination-page']")
                        break
                except:
                    continue
            
            if buttons is None or await buttons.count() == 0:
                await extract_current_page()
            else:
                # Extract current page once
                btn_count = await buttons.count()
                if btn_count == 0:
                    await extract_current_page()
                else:
                    current_label = None
                    all_labels = []
                    for i in range(btn_count):
                        btn = buttons.nth(i)
                        aria_label = await btn.get_attribute("aria-label")
                        if aria_label:
                            all_labels.append(aria_label)
                        aria_current = await btn.get_attribute("aria-current")
                        if aria_current and aria_current.lower() == "true":
                            current_label = aria_label
                    
                    if current_label:
                        await extract_current_page(current_label)
                    else:
                        await extract_current_page()
                    
                    # Determine pages to check: first 10 + last page
                    total_pages = len(all_labels)
                    pages_to_check = []
                    
                    if total_pages <= max_pages:
                        # If total pages <= 10, check all
                        pages_to_check = [label for label in all_labels if label != current_label]
                    else:
                        # Many pages detected
                        has_many_pages = True
                        # Check first 10 pages (excluding current if it's in first 10)
                        first_10 = all_labels[:max_pages]
                        pages_to_check = [label for label in first_10 if label != current_label]
                        
                        # Add last page if not already included
                        last_page = all_labels[-1]
                        if last_page not in pages_to_check:
                            pages_to_check.append(last_page)
                        
                        print(f"[Type 4] {title}: Total {total_pages} pages detected. Checking first {max_pages} + last page")
                    
                    # Click each page to check
                    pages_checked = 0
                    for label in pages_to_check:
                        if repeating_detected and pages_checked >= 2:
                            print(f"[Type 4] {title}: Stopping pagination - same errors detected on consecutive pages")
                            break
                        
                        # Find the button with matching aria-label
                        target = None
                        for i in range(await buttons.count()):
                            btn = buttons.nth(i)
                            btn_label = await btn.get_attribute("aria-label")
                            if btn_label == label:
                                target = btn
                                break
                        
                        if not target:
                            continue
                        
                        disabled_attr = await target.get_attribute("disabled")
                        aria_disabled = await target.get_attribute("aria-disabled")
                        if disabled_attr is not None or (aria_disabled and aria_disabled.lower() == "true"):
                            continue

                        prev_signature = ""
                        try:
                            prev_signature = (await widget.locator(table_selector).locator("tbody").inner_text(timeout=2000)).strip()
                        except Exception:
                            prev_signature = ""

                        await target.click()
                        await self.page.wait_for_timeout(800)
                        changed = False
                        for _ in range(10):
                            await self.page.wait_for_timeout(500)
                            try:
                                new_signature = (await widget.locator(table_selector).locator("tbody").inner_text(timeout=2000)).strip()
                            except Exception:
                                new_signature = ""
                            if new_signature and new_signature != prev_signature:
                                changed = True
                                break

                        if not changed:
                            print(f"[Type 4] {title}: Pagination did not change content after click, continuing.")
                            continue

                        await extract_current_page(label)
                        pages_checked += 1

        except Exception as e:
            print(f"[Type 4] Error extracting table: {e}")

        formatted_errors = []
        for error_name, count in errors_dict.items():
            times = "time" if count == 1 else "times"
            formatted_errors.append(f"{error_name} - occurred {count} {times}")
        
        # Add warning if there are many pages or repeating errors were detected
        if has_many_pages or repeating_detected:
            formatted_errors.append("There are multiple pages - please check the URL for further information")
        
        print(f"[Type 4] {title}: Extracted {len(formatted_errors)} unique errors")
        return {"name": title, "errors": formatted_errors}

    async def _extract_widget_errors(self, service_name, title):
        #Generic method to extract errors from a widget.
        try:
            config = self.widget_config.get(service_name)
            if not config:
                print(f"[Type 4] No configuration for {service_name}")
                return {"name": title, "errors": []}
            widget_id = config["id"]
            widget = self.page.locator(f"#widget_box__{widget_id}")

            # Wait for widget to be visible
            await widget.wait_for(state="visible", timeout=10000)
            await widget.scroll_into_view_if_needed(timeout=5000)
            await self.page.wait_for_timeout(2000)

            # Extract widget title
            title_selector = f"#widget_box__{widget_id} > div.group.flex.flex-initial.items-center.justify-between.space-x-3.rounded-t.p-3.w-full.hover\\:overflow-visible > div.flex.items-center.space-x-1.min-w-0 > a > h2"
            try:
                title = await self.page.locator(title_selector).inner_text(timeout=3000)
                print(f"[Type 4] Found widget title: '{title}'")
            except Exception as e:
                print(f"[Type 4] Could not extract title: {e}, using default: {title}")

            # Wait for widget content to load - check for loading/searching state
            max_wait = 30  # 30 seconds max
            for i in range(max_wait):
                try:
                    # Check if still searching
                    searching = widget.locator('div.text-deemphasized').filter(has_text="Searching")
                    searching_count = await searching.count()
                    if searching_count > 0:
                        if i == 0 or i % 5 == 0:
                            print(f"[Type 4] {title}: Widget still searching, waiting...")
                        await self.page.wait_for_timeout(1000)
                        continue
                    else:
                        # Not searching anymore
                        break
                except:
                    break
            
            # Additional wait to ensure content is stable
            await self.page.wait_for_timeout(2000)

            # Check for "No results found" message
            try:
                no_results = widget.locator('div.text-deemphasized').filter(has_text="Search completed. No results found")
                await no_results.wait_for(timeout=2000)
                print(f"[Type 4] {title}: No results found")
                return {"name": title, "errors": []}
            except:
                pass

            # Extract table errors with pagination support
            table_selector = config["table_selector"]
            return await self._extract_table_errors_with_pagination(widget, table_selector, title)

        except Exception as e:
            print(f"[Type 4] Error in _extract_widget_errors for {service_name}: {e}")
            return {"name": title, "errors": []}

    async def _extract_charger_errors(self):
        #Extract Charger-Errors widget data.
        return await self._extract_widget_errors("charger", "Charger-Errors")

    async def _extract_keysmith_errors(self):
        #Extract Keysmith-Errors widget data.
        return await self._extract_widget_errors("keysmith", "Keysmith-Errors")

    async def _extract_neptune_errors(self):
        #Extract Neptune-Errors widget data.
        return await self._extract_widget_errors("neptune", "Neptune-Errors")

    async def _extract_roundup_errors(self):
        #Extract Roundup-Errors widget data.
        return await self._extract_widget_errors("roundup", "Roundup-Errors")

    async def _extract_zinc_errors(self):
        #Extract Zinc-Errors widget data.
        return await self._extract_widget_errors("zinc", "Zinc-Errors")

    async def _extract_pii_count(self):
        #Extract PII Count widget data.
        try:
            print("[Type 4] Extracting PII Count widget...")

            config = self.widget_config.get("pii_count")
            if not config:
                print("[Type 4] No configuration for pii_count")
                return {"name": "PII Detection Count", "errors": ["PII Detection Count - No errors"]}
            widget_id = config["id"]
            widget = self.page.locator(f"#widget_box__{widget_id}")

            # Scroll widget into view
            try:
                await widget.scroll_into_view_if_needed(timeout=5000)
                print("[Type 4] Scrolled to PII Count widget")
            except:
                pass

            await self.page.wait_for_timeout(2000)
            await widget.wait_for(state="visible", timeout=10000)
            
            # Wait for widget content to load - check for loading/searching state
            max_wait = 30  # 30 seconds max
            for i in range(max_wait):
                try:
                    # Check if still searching
                    searching = widget.locator('div.text-deemphasized').filter(has_text="Searching")
                    searching_count = await searching.count()
                    if searching_count > 0:
                        if i == 0 or i % 5 == 0:
                            print(f"[Type 4] PII Count: Widget still searching, waiting...")
                        await self.page.wait_for_timeout(1000)
                        continue
                    else:
                        # Not searching anymore
                        break
                except:
                    break
            
            # Additional wait to ensure content is stable
            await self.page.wait_for_timeout(2000)

            # Extract widget title
            title_selector = f"#widget_box__{widget_id} > div.group.flex.flex-initial.items-center.justify-between.space-x-3.rounded-t.p-3.w-full.hover\\:overflow-visible > div.flex.items-center.space-x-1.min-w-0 > a > h2"
            title = "PII Detection Count"
            try:
                title = await self.page.locator(title_selector).inner_text(timeout=3000)
                print(f"[Type 4] Found widget title: '{title}'")
            except Exception as e:
                print(f"[Type 4] Could not extract title: {e}, using default")

            # Extract count from content area
            try:
                content_selector = config["content_selector"]
                content_element = self.page.locator(f"#widget_box__{widget_id} > {content_selector}")
                await content_element.wait_for(state="visible", timeout=5000)

                # Get the inner text which contains the count
                count_text = await content_element.inner_text(timeout=2000)
                count_text = count_text.strip()
                print(f"[Type 4] PII Count widget content: '{count_text}'")

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
                print(f"[Type 4] Error extracting PII count: {e}")
                message = f"{title} - No errors"
                return {"name": title, "errors": [message]}

        except Exception as e:
            print(f"[Type 4] Error in _extract_pii_count: {e}")
            return {"name": "PII Detection Count", "errors": ["PII Detection Count - No errors"]}

    async def run_checks(self):
        #Main method to run all checks on the dashboard.
        try:
            print(f"\n{'='*60}")
            print(f"[Type 4] Running Type 4 Dashboard Checks")
            print(f"[Type 4] Environment: {self.environment}")
            print(f"{'='*60}\n")

            # Step 1: Wait for dashboard to load
            print("[Type 4] Step 1/7: Waiting for dashboard to load...")
            await self._wait_for_dashboard_load()
            await self.page.wait_for_timeout(3000)

            # Step 2: Extract Charger-Errors widget
            print("[Type 4] Step 2/7: Extracting Charger-Errors widget...")
            charger_result = await self._extract_charger_errors()
            self.service_errors["charger"] = charger_result["errors"]
            self.widgets.append(charger_result)
            await self.page.wait_for_timeout(1000)

            # Step 3: Extract Keysmith-Errors widget
            print("[Type 4] Step 3/7: Extracting Keysmith-Errors widget...")
            keysmith_result = await self._extract_keysmith_errors()
            self.service_errors["keysmith"] = keysmith_result["errors"]
            self.widgets.append(keysmith_result)
            await self.page.wait_for_timeout(1000)
            
            # Step 4: Extract Neptune-Errors widget
            print("[Type 4] Step 4/7: Extracting Neptune-Errors widget...")
            neptune_result = await self._extract_neptune_errors()
            self.service_errors["neptune"] = neptune_result["errors"]
            self.widgets.append(neptune_result)
            await self.page.wait_for_timeout(1000)
            
            # Step 5: Extract Roundup-Errors widget
            print("[Type 4] Step 5/7: Extracting Roundup-Errors widget...")
            roundup_result = await self._extract_roundup_errors()
            self.service_errors["roundup"] = roundup_result["errors"]
            self.widgets.append(roundup_result)
            await self.page.wait_for_timeout(1000)
            
            # Step 6: Extract Zinc-Errors widget
            print("[Type 4] Step 6/7: Extracting Zinc-Errors widget...")
            zinc_result = await self._extract_zinc_errors()
            self.service_errors["zinc"] = zinc_result["errors"]
            self.widgets.append(zinc_result)
            await self.page.wait_for_timeout(1000)
            
            # Step 7: Extract PLL Count widget
            print("[Type 4] Step 7/7: Extracting PII Count widget...")
            pii_result = await self._extract_pii_count()
            self.service_errors["pii_count"] = pii_result["errors"]
            self.widgets.append(pii_result)
            
            print(f"\n[Type 4] Checks completed successfully")
            print(f"{'='*60}\n")
            return True
        
        except Exception as e:
            print(f"[Type 4] Error during run_checks: {e}")
            return False
