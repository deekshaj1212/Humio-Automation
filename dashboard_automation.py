import asyncio
from login_automation import HumioLoginAutomation

DASHBOARD_URLS = {
    "env1": {
        "dashboard_type_1": "https://ccpreusw2-us-west-2.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/Data%20Ingestion%20to%20Sustainability%20Insight%20Center?dashboardId=c1aViyZqkRvBsI3eMKRpOQ6zCzPWJ35z",
        "dashboard_type_2": "https://ccpreusw2-us-west-2.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/COM%20Subscription%20and%20Consumption?dashboardId=EJp6d928ejsSA00kw2emoBhcVNf2OjOd",
        "dashboard_type_3": "https://ccpreusw2-us-west-2.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/Activation%20Key%20Onboarding?dashboardId=LtFA33nlpz73ZpH9608jqRLQBlvpbnPz",
        "dashboard_type_4": "https://ccpreusw2-us-west-2.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/%5BTS-Manisha%5D%20Service-Errors%20Filter%20Known%20Issues%20(pre-prod)?dashboardId=UCTmt1Oxn5PhLs1ReaqS1lqpyZd8a3is",
    },
    "env2": {
        "dashboard_type_1": "https://ccprodane1-ap-northeast-1.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/Data%20Ingestion%20to%20Sustainability%20Insight%20Center?dashboardId=8baepYQQfzBT8JBf1d3T51niNeKAhmeQ",
        "dashboard_type_2": "https://ccprodane1-ap-northeast-1.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/COM%20Subscription%20and%20Consumption?dashboardId=BjjaphcXKAExfBqVX5WbMjnI79hO8oDd",
        "dashboard_type_3": "https://ccprodane1-ap-northeast-1.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/Activation%20Key%20Onboarding?dashboardId=8vglYJMqNn8w7piqx8JjaPsbgINTsyvM",
        "dashboard_type_4": "https://ccprodane1-ap-northeast-1.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/%5BTS-Manisha%5D%20Service-Errors%20Filter%20Known%20Issues?dashboardId=4CgWG7CJ2siNnxNsQjMvmsrySaaBXh6o",
    },
    "env3": {
        "dashboard_type_1": "https://ccprodeuc1-eu-central-1.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/Data%20Ingestion%20to%20Sustainability%20Insight%20Center?dashboardId=CXyM0Ixx13oKBIu4qdVSouvNr3z72Q7R",
        "dashboard_type_2": "https://ccprodeuc1-eu-central-1.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/COM%20Subscription%20and%20Consumption?dashboardId=7HOpZefQ7ATnthap8qOzG4ce5mq4tsSF",
        "dashboard_type_3": "https://ccprodeuc1-eu-central-1.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/Activation%20Key%20Onboarding?dashboardId=2sU9buDIfWraWyqToP7tlvwL6CfIGuz8",
        "dashboard_type_4": "https://ccprodeuc1-eu-central-1.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/%5BTS-Manisha%5D%20Service-Errors%20Filter%20Known%20Issues?dashboardId=MEKx3SLFhPj8TTDZHVug9a5Vq6vo2MvG",
    },
    "env4": {
        "dashboard_type_1": "https://ccprodusw2-us-west-2.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/Data%20Ingestion%20to%20Sustainability%20Insight%20Center?dashboardId=k1IfQQ0CrPmymhHWIQhVVOGX9iP8F9WE",
        "dashboard_type_2": "https://ccprodusw2-us-west-2.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/COM%20Subscription%20and%20Consumption?dashboardId=PrsSt0o2jnyVDfUtF6G5RuW8J0B04hFE",
        "dashboard_type_3": "https://ccprodusw2-us-west-2.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/Activation%20Key%20Onboarding?dashboardId=8CtZeTHokVjo0k24Hw498lhqgHJNAnyf",
        "dashboard_type_4": "https://ccprodusw2-us-west-2.cloudops.compute.cloud.hpe.com/logs/computecentral/dashboards/%5BTS-Manisha%5D%20Service-Errors%20Filter%20Known%20Issues?dashboardId=UNUXGptMYR0BzrmRpEqA8NiOPQzXUqM9",
    },
}

class DashboardType1Automation:
    """Automation logic for Dashboard Type 1 - Data Ingestion to Sustainability Insight Center."""
    def __init__(self, page):
        self.page = page
        self.dashboard_name = "Data Ingestion to Sustainability Insight Center"
        self.result = None
    
    async def verify_dashboard(self):
        """Verify we are on the correct Type 1 dashboard by checking URL."""
        try:
            # Wait for page to fully stabilize
            await self.page.wait_for_load_state("domcontentloaded")
            await self.page.wait_for_timeout(1000)
            current_url = self.page.url
            print(f"Current URL: {current_url}")
            if "Ingestion%20to%20Sustainability%20Insight%" in current_url:
                print(f"Type 1 Dashboard Detected")
                return True
            else:
                print(f"Dashboard mismatch. Expected 'Ingestion%20to%20Sustainability%20Insight%' in URL")
                return False
                
        except Exception as e:
            print(f"Could not verify dashboard: {e}")
            return False
    
    async def get_failed_upload_count(self):
        """Extract the 'Files failed to upload' number from the dashboard."""
        try:
            widget = self.page.locator("#widget_box__f2a451e5-523a-43ec-9e89-0ff268d2963e")
            await widget.scroll_into_view_if_needed()
            await self.page.wait_for_timeout(500)
            value_element = widget.locator('[data-e2e="single-value-widget-value"]')
            count_text = await value_element.inner_text(timeout=5000)
            count = int(count_text.strip())
            print(f"Found failed upload count: {count}")
            return count
            
        except Exception as e:
            print(f"Could not extract failed upload count: {e}")
            return None
    
    async def generate_summary(self):
        """Generate summary based on failed upload count."""
        failed_count = await self.get_failed_upload_count()
        if failed_count is None:
            self.result = f"{self.dashboard_name}\nUnable to determine status"
            return
        if failed_count == 0:
            self.result = f"{self.dashboard_name}\nNo errors"
        else:
            self.result = f"{self.dashboard_name}\n{failed_count} files failed to upload"
    
    async def run_checks(self):
        """Run dashboard-specific checks and automation."""
        print("Running Dashboard Type 1 checks...")
        await self.page.wait_for_timeout(2000)
        is_correct_dashboard = await self.verify_dashboard()
        if not is_correct_dashboard:
            self.result = f"{self.dashboard_name} Dashboard verification failed"
            print(self.result)
            return self.result
        await self.generate_summary()
        print(self.result)
        return self.result

class DashboardType2Automation:
    """Automation logic for Dashboard Type 2 - COM Subscription and Consumption."""
    
    def __init__(self, page):
        """Initialize with Playwright page object."""
        self.page = page
        self.dashboard_name = "COM Subscription and Consumption"
        self.result = None
    
    async def verify_dashboard(self):
        """Verify we are on the correct Type 2 dashboard by checking URL."""
        try:
            # Wait for page to fully stabilize
            await self.page.wait_for_load_state("domcontentloaded")
            await self.page.wait_for_timeout(1000)
            current_url = self.page.url            
            if "COM%20Subscription%20and%20Consumption" in current_url:
                print(f"Type 2 Dashboard Detected")
                return True
            else:
                print(f"Dashboard mismatch. Expected 'COM%20Subscription%20and%20Consumption' in URL")
                return False
                
        except Exception as e:
            print(f"Could not verify dashboard: {e}")
            return False
    
    async def get_service_instance_errors(self):
        """Extract the 'Service instance ERROR (CDS)' count from the dashboard."""
        try:
            # Find the "Service instance ERROR (CDS)" link
            error_link = self.page.get_by_role("link", name="Service instance ERROR (CDS)")
            parent = error_link.locator('..')
            parent_text = await parent.inner_text()
            error_count_element = self.page.get_by_text("0", exact=True).first
            count_text = await error_count_element.inner_text()
            count = int(count_text.strip())
            print(f"Found service instance ERROR (CDS) count: {count}")
            return count
            
        except Exception as e:
            print(f"Could not extract service instance errors: {e}")
            return None
    
    async def get_upload_errors(self):
        """Extract the 'Upload ERROR (CDS)' count from the dashboard."""
        try:
            # Get the value using nth(1) as specified
            error_count_element = self.page.get_by_text("0", exact=True).nth(1)
            count_text = await error_count_element.inner_text()
            count = int(count_text.strip())
            print(f"Found Upload ERROR (CDS) count: {count}")
            return count
            
        except Exception as e:
            print(f"Could not extract upload errors: {e}")
            return None
    
    async def get_charger_schedules_errors(self):
        """Extract the 'Charger Schedules ERROR' count from the dashboard."""
        import re
        try:
            widget = self.page.locator("#widget_box__8a200ba1-6845-44f9-9289-bc7805361900")
            await widget.scroll_into_view_if_needed()
            await self.page.wait_for_timeout(500)
            value_element = widget.locator('[data-e2e="single-value-widget-value"]')
            count_text = await value_element.inner_text(timeout=5000)
            count = int(count_text.strip())
            print(f"Found Charger Schedules ERROR count: {count}")
            return count
            
        except Exception as e:
            print(f"Could not extract charger schedules errors: {e}")
            return None
    
    async def get_license_oversubscribe_count(self):
        """Extract the 'Advanced License Oversubscribe Detection Count' from the dashboard."""
        try:
            widget = self.page.locator("#widget_box__8481de95-4fc5-4ba2-9b63-dba0ed55cde7")
            await widget.scroll_into_view_if_needed()
            await self.page.wait_for_timeout(500)
            value_element = widget.locator('[data-e2e="single-value-widget-value"]')
            count_text = await value_element.inner_text(timeout=5000)
            count = int(count_text.strip())
            print(f"Found Advanced License Oversubscribe Detection Count: {count}")
            return count
            
        except Exception as e:
            print(f"Could not extract Advanced License Oversubscribe count: {e}")
            return 0
    
    async def get_charger_errors(self):
        """Extract 'Charger Errors' from the dashboard."""
        try:
            error_link = self.page.get_by_role("link", name="Charger Errors")
            widget = error_link.locator('..').locator('..').locator('..')
            await widget.scroll_into_view_if_needed()
            await self.page.wait_for_timeout(500)
            no_results_div = widget.locator('div.text-deemphasized').filter(has_text="Search completed. No results found")
            try:
                await no_results_div.wait_for(timeout=3000)
                print(f"Charger Errors: No results found (no errors)")
                return None  
            except:
                error_text = await widget.inner_text()
                print(f"Found Charger Errors: {error_text[:100]}...")
                return error_text
                
        except Exception as e:
            print(f"Could not extract charger errors: {e}")
            return None
    
    async def get_skipped_servers_count(self):
        """Extract the 'Skipped servers' count from the dashboard."""
        try:
            link = self.page.get_by_role("link", name="Skipped servers")
            widget = link.locator('..').locator('..').locator('..')
            await widget.scroll_into_view_if_needed()
            await self.page.wait_for_timeout(500)
            value_element = widget.locator('[data-e2e="single-value-widget-value"]')
            count_text = await value_element.inner_text(timeout=5000)
            count = int(count_text.strip())
            print(f"Found Skipped servers count: {count}")
            return count
            
        except Exception as e:
            print(f"Could not extract skipped servers count: {e}")
            return 0
    
    async def generate_summary(self):
        """Generate summary based on all service errors."""
        # Scroll down first to make all widgets visible
        try:
            print(f"Scrolling down to reveal all widgets")
            await self.page.evaluate("""
                () => {
                    window.scrollBy(0, 1000);
                }
            """)
            await self.page.wait_for_timeout(1500)
        except Exception as e:
            print(f"Could not scroll: {e}")
    
        errors = []
        
        # Check Service Instance Errors
        si_count = await self.get_service_instance_errors()
        if si_count is not None and si_count > 0:
            errors.append(f"{si_count} Service instance ERROR (CDS)")
        
        # Check Upload Errors
        upload_count = await self.get_upload_errors()
        if upload_count is not None and upload_count > 0:
            errors.append(f"{upload_count} Upload ERROR (CDS)")
        
        # Check Charger Schedules Errors
        charger_count = await self.get_charger_schedules_errors()
        if charger_count is not None and charger_count > 0:
            errors.append(f"{charger_count} Charger Schedules ERROR")
        
        # Check License Oversubscribe
        license_count = await self.get_license_oversubscribe_count()
        if license_count is not None and license_count > 0:
            errors.append(f"{license_count} Advanced License Oversubscribe Detection Count")
        
        # Check Charger Errors
        charger_errors = await self.get_charger_errors()
        if charger_errors is not None:
            errors.append(f"Charger Errors: {charger_errors[:100]}")
        
        # Check Skipped Servers
        skipped_count = await self.get_skipped_servers_count()
        if skipped_count is not None and skipped_count > 0:
            errors.append(f"{skipped_count} Skipped servers")
        
        # Generate result
        if errors:
            errors_text = " | ".join(errors)
            self.result = f"   ✗ {self.dashboard_name} - {errors_text}"
        else:
            self.result = f"{self.dashboard_name} - No errors"
    
    async def run_checks(self):
        """Run dashboard-specific checks and automation."""
        print("Running Dashboard Type 2 checks...")
        await self.page.wait_for_timeout(2000)
        is_correct_dashboard = await self.verify_dashboard()
        if not is_correct_dashboard:
            self.result = f"{self.dashboard_name} - Dashboard verification failed"
            print(self.result)
            return self.result
        
        await self.generate_summary()
        print(self.result)
        return self.result


class DashboardType3Automation:
    """Automation logic for Dashboard Type 3 - Activation Key Onboarding."""
    
    def __init__(self, page):
        """Initialize with Playwright page object."""
        self.page = page
        self.dashboard_name = "Activation Key Onboarding"
        self.result = None
    
    async def verify_dashboard(self):
        """Verify we are on the correct Type 3 dashboard by checking URL."""
        try:
            await self.page.wait_for_load_state("domcontentloaded")
            await self.page.wait_for_timeout(1000)
            current_url = self.page.url
            print(f"Current URL: {current_url}")
            if "Activation%20Key%20Onboarding" in current_url:
                print(f"Type 3 Dashboard Detected")
                return True
            else:
                print(f"Dashboard mismatch. Expected 'Activation%20Key%20Onboarding' in URL")
                return False
                
        except Exception as e:
            print(f"   ✗ Could not verify dashboard: {e}")
            return False
    
    async def get_jwt_generation_failed(self):
        """Extract the 'JWT generation failed' count from the dashboard."""
        try:
            widget = self.page.locator("#widget_box__65662d8f-6256-4b4f-975d-30c0a9e7267d")
            await widget.scroll_into_view_if_needed()
            await self.page.wait_for_timeout(500)
            value_element = widget.locator('[data-e2e="single-value-widget-value"]')
            count_text = await value_element.inner_text(timeout=5000)
            count = int(count_text.strip())
            print(f"Found JWT generation failed count: {count}")
            return count
            
        except Exception as e:
            print(f"Could not extract JWT generation failed count: {e}")
            return 0
    
    async def get_subscription_key_claim_failure(self):
        """Extract the 'Subscription Key Claim Failure While JWT Generation' count from the dashboard."""
        try:
            widget = self.page.locator("#widget_box__fa904b24-0480-4364-bd19-edf2a7e6a872")
            await widget.scroll_into_view_if_needed()
            await self.page.wait_for_timeout(500)
            value_element = widget.locator('[data-e2e="single-value-widget-value"]')
            count_text = await value_element.inner_text(timeout=5000)
            count = int(count_text.strip())
            print(f"Found Subscription Key Claim Failure while JWT Generation count: {count}")
            return count
            
        except Exception as e:
            print(f"Could not extract Subscription Key Claim Failure while JWT Generation count: {e}")
            return 0
    
    async def get_device_not_available_glp_pool(self):
        """Extract the 'Device not available GLP Pool' count from the dashboard."""
        try:
            widget = self.page.locator("#widget_box__a7a91c34-a179-43d1-8017-11ab0b5e62d2")
            await widget.scroll_into_view_if_needed()
            await self.page.wait_for_timeout(500)
            value_element = widget.locator('[data-e2e="single-value-widget-value"]')
            count_text = await value_element.inner_text(timeout=5000)
            count = int(count_text.strip())
            print(f"Found Device not available GLP Pool count: {count}")
            return count
            
        except Exception as e:
            print(f"Could not extract Device not available GLP Pool count: {e}")
            return 0
    
    async def get_location_tags_sdc_patch_failure(self):
        """Extract the 'Location/Tags/Sdc Patch Failure Count' from the dashboard."""
        try:
            # Try multiple widget IDs (different between environments)
            widget_ids = [
                "#widget_box__24c7e9ab-3f07-43b1-985d-96fd8a382fb0",  # env1
                "#widget_box__9ca37872-2576-4389-b9ec-e611738b8b2a",  # env3
                "#widget_box__77afab0c-0551-4d44-97e9-47a171a3df60",  # env2
                "#widget_box__aeba4442-77dc-401c-8deb-16ba500016d5"   # env4
            ]
            
            widget = None
            for widget_id in widget_ids:
                try:
                    temp_widget = self.page.locator(widget_id)
                    await temp_widget.wait_for(timeout=2000)
                    widget = temp_widget
                    break
                except:
                    continue
            if not widget:
                print(f"Location/Tags/Sdc Patch Failure widget not found")
                return 0
            
            try:
                await widget.scroll_into_view_if_needed(timeout=10000)
            except:
                await self.page.evaluate("window.scrollBy(0, 2000)")
                await self.page.wait_for_timeout(1000)
            await self.page.wait_for_timeout(500)
            
            try:
                content_div = widget.locator('div.text-deemphasized.w-full.h-full.flex.items-center.justify-center.border-t.border-normal.shadow-base.shadow-inner-md')
                content_text = await content_div.inner_text(timeout=2000)
                if "Search completed. No results found" in content_text:
                    print(f"Location/Tags/Sdc Patch Failure: No results found (0)")
                    return 0
            except:
                pass
            
            try:
                value_element = widget.locator('[data-e2e="single-value-widget-value"]')
                count_text = await value_element.inner_text(timeout=3000)
                count = int(count_text.strip())
                print(f"Found Location/Tags/Sdc Patch Failure Count: {count}")
                return count
            except:
                try:
                    value_element = widget.locator('div[data-e2e*="value"]')
                    count_text = await value_element.inner_text(timeout=3000)
                    count = int(count_text.strip())
                    print(f"Found Location/Tags/Sdc Patch Failure Count: {count}")
                    return count
                except:
                    print(f"Location/Tags/Sdc Patch Failure: No data found (0)")
                    return 0
            
        except Exception as e:
            print(f"Could not extract Location/Tags/Sdc Patch Failure Count: {e}")
            return 0
    
    async def get_sdc_patch_failure_errors(self):
        """Extract error details if Location/Tags/Sdc Patch Failure Count > 0."""
        try:
            widget = self.page.locator("#widget_box__72e5beef-64dc-4be4-becd-9970e2a6c87f")
            await widget.scroll_into_view_if_needed()
            await self.page.wait_for_timeout(500)
            content_div = widget.locator('div.text-deemphasized.w-full.h-full.flex.items-center.justify-center.border-t.border-normal.shadow-base.shadow-inner-md')
            content_text = await content_div.inner_text(timeout=5000)
            if "Search completed. No results found" in content_text:
                print(f"SDC Patch Failure: No results found")
                return None
            else:
                print(f"Found SDC Patch Failure errors: {content_text[:100]}...")
                return content_text
                
        except Exception as e:
            print(f"Could not extract SDC Patch Failure errors: {e}")
            return None
    
    async def get_oae_errors(self):
        """Extract Error Details During iLO Onboard Activation Job."""
        try:
            # Try multiple widget IDs (different between environments)
            widget_ids = [
                "#widget_box__fe7e56ad-8d35-45fa-a535-80bb1ce67ab7",  # env1
                "#widget_box__77afab0c-0551-4d44-97e9-47a171a3df60"   # env2
            ]
            
            widget = None
            for widget_id in widget_ids:
                try:
                    temp_widget = self.page.locator(widget_id)
                    await temp_widget.wait_for(timeout=2000)
                    widget = temp_widget
                    break
                except:
                    continue
            
            if not widget:
                print(f"Error Details During iLO Onboard Activation Job widget not found")
                return None
            
            try:
                await widget.scroll_into_view_if_needed(timeout=10000)
            except:
                await self.page.evaluate("window.scrollBy(0, 2000)")
                await self.page.wait_for_timeout(1000)
            
            await self.page.wait_for_timeout(500)
            
            try:
                table = widget.locator('div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table')
                await table.wait_for(timeout=2000)
                # It's a table - extract error codes from columns 5 and 6
                error_codes = []
                rows = widget.locator('div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table > tbody > tr')
                row_count = await rows.count()
                for i in range(min(row_count, 20)):  # Limit to 20 rows
                    try:
                        # Get column 5 - error code
                        col5 = rows.nth(i).locator('td:nth-child(5) > div')
                        code_text = await col5.inner_text(timeout=1000)
                        
                        # Get column 6 - error name
                        col6 = rows.nth(i).locator('td:nth-child(6) > div')
                        name_text = await col6.inner_text(timeout=1000)
                        
                        if code_text.strip() and name_text.strip():
                            error_codes.append(f"{code_text.strip()} - {name_text.strip()}")
                    except:
                        continue
                if error_codes:
                    preview = ", ".join(error_codes[:5])
                    print(f"   Found Error Details During iLO Onboard Activation Job: {preview}")
                    return error_codes  # Return as list
                else:
                    print(f"   Error Details During iLO Onboard Activation Job: No error codes found")
                    return None
                    
            except:
                # Not a table - try text content div (env1/env2 style)
                try:
                    content_div = widget.locator('div.text-deemphasized.w-full.h-full.flex.items-center.justify-center.border-t.border-normal.shadow-base.shadow-inner-md')
                    content_text = await content_div.inner_text(timeout=2000)
                    # Check if it's "No results found" or still searching
                    if "Search completed. No results found" in content_text or "Searching" in content_text:
                        print(f"Error Details During iLO Onboard Activation Job: No results found")
                        return None
                    else:
                        print(f"Error Details During iLO Onboard Activation Job: No results found")
                        return None  # Don't return text content, only structured errors
                except:
                    print(f"Error Details During iLO Onboard Activation Job: No results found")
                    return None
                
        except Exception as e:
            print(f"Could not extract Error Details During iLO Onboard Activation Job: {e}")
            return None
    
    async def get_error_codes_simple(self):
        """Extract Subscription key claim failure details."""
        try:
            widget = self.page.locator("#widget_box__0104eef2-6852-4bbc-ab64-43934aaf268f")
            await widget.scroll_into_view_if_needed(timeout=5000)
            await self.page.wait_for_timeout(500)
            try:
                content_div = widget.locator('div.text-deemphasized.w-full.h-full.flex.items-center.justify-center.border-t.border-normal.shadow-base.shadow-inner-md')
                content_text = await content_div.inner_text(timeout=2000)
                
                if "Search completed. No results found" in content_text or "Searching" in content_text:
                    print(f"Subscription key claim failure details: No results found")
                    return None
                else:
                    print(f"Found Subscription key claim failure details")
                    return None  # Don't return text, only structured data
            except:
                print(f"Subscription key claim failure details: No results found")
                return None
                
        except Exception as e:
            print(f"Subscription key claim failure details: No results found")
            return None
    
    async def get_table_error_codes(self):
        """Extract Subscription key assignment failure details."""
        try:
            widget = self.page.locator("#widget_box__79b189d5-cfa5-48be-846f-e9073556b286")
            await widget.scroll_into_view_if_needed()
            await self.page.wait_for_timeout(500)
            try:
                no_results = widget.locator('div.text-deemphasized').filter(has_text="Search completed. No results found")
                await no_results.wait_for(timeout=2000)
                print(f"   Subscription key assignment failure details: No results found")
                return None
            except:
                pass
            
            error_codes = []
            rows = widget.locator('table > tbody > tr')
            row_count = await rows.count()
            for i in range(row_count):
                try:
                    error_cell = rows.nth(i).locator('td:nth-child(6) > div')
                    error_text = await error_cell.inner_text(timeout=3000)
                    if error_text.strip():
                        error_codes.append(error_text.strip())
                except:
                    continue
            if error_codes:
                preview = ", ".join(error_codes[:5])
                print(f"Found Subscription key assignment failure details: {preview}...")
                return error_codes
            else:
                print(f"   Subscription key assignment failure details: No data found")
                return None
                
        except Exception as e:
            print(f"   ⚠ Could not extract Subscription key assignment failure details: {e}")
            return None
    
    async def get_pin_generation_failure_details(self):
        """Extract PIN Generation Failure error codes from table."""
        try:
            # Try multiple widget IDs (different between environments)
            widget_ids = [
                "#widget_box__7edd90fc-15d3-4ba7-9fc0-49b0614780d8"   # env1/env2
            ]
            
            widget = None
            for widget_id in widget_ids:
                try:
                    temp_widget = self.page.locator(widget_id)
                    await temp_widget.wait_for(timeout=2000)
                    widget = temp_widget
                    break
                except:
                    continue
            
            if not widget:
                print(f"PIN Generation Failure widget not found")
                return None
            try:
                await widget.scroll_into_view_if_needed(timeout=10000)
            except:
                await self.page.evaluate("window.scrollBy(0, 2000)")
                await self.page.wait_for_timeout(1000)
            await self.page.wait_for_timeout(500)   
            content_container = widget.locator('div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div')
            try:
                table = widget.locator('div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table')
                await table.wait_for(timeout=3000)
                await widget.evaluate("""
                    (element) => {
                        const scrollableDiv = element.querySelector('div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div');
                        if (scrollableDiv) {
                            scrollableDiv.scrollLeft = scrollableDiv.scrollWidth;
                        }
                    }
                """)
                await self.page.wait_for_timeout(500)
                error_codes = []
                rows = widget.locator('div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table > tbody > tr')
                row_count = await rows.count()
                for i in range(row_count):
                    try:
                        # Get column 7 (error code)
                        col7 = rows.nth(i).locator('td:nth-child(7) > div')
                        code_text = await col7.inner_text(timeout=2000)
                        
                        # Get column 8 (error name)
                        col8 = rows.nth(i).locator('td:nth-child(8) > div')
                        name_text = await col8.inner_text(timeout=2000)
                        
                        if code_text.strip() and name_text.strip():
                            error_codes.append(f"{code_text.strip()} - {name_text.strip()}")
                    except:
                        continue
                
                if error_codes:
                    preview = ", ".join(error_codes[:3])
                    print(f"   Found PIN Generation Failure errors: {preview}...")
                    return error_codes
                else:
                    print(f"   PIN Generation Failure: No error codes found")
                    return None
                    
            except:
                try:
                    content_div = widget.locator('div.text-deemphasized.w-full.h-full.flex.items-center.justify-center.border-t.border-normal.shadow-base.shadow-inner-md')
                    content_text = await content_div.inner_text(timeout=3000)
                    if "Search completed. No results found" in content_text:
                        print(f"PIN Generation Failure: No results found")
                        return None
                    else:
                        # Attempt to parse lines as errors
                        raw_lines = [line.strip() for line in content_text.splitlines() if line.strip()]
                        if raw_lines:
                            print(f"   Found PIN Generation Failure errors: {', '.join(raw_lines[:3])}...")
                            return raw_lines
                        print(f"PIN Generation Failure: No results found")
                        return None
                except:
                    try:
                        no_results = content_container.locator('div.text-deemphasized').filter(has_text="Search completed. No results found")
                        await no_results.wait_for(timeout=2000)
                        print(f"PIN Generation Failure: No results found")
                        return None
                    except:
                        print(f"PIN Generation Failure: Unable to determine content")
                        return None
                
        except Exception as e:
            print(f"Could not extract PIN Generation Failure details: {e}")
            return None
    
    async def get_compute_provision_failure_details(self):
        """Extract Compute Provision Failure error codes."""
        try:
            widget = self.page.locator("#widget_box__99bc4e96-1f7b-4d1f-a326-c46ee1ab0623")         
            try:
                await widget.scroll_into_view_if_needed(timeout=10000)
            except:
                await self.page.evaluate("window.scrollBy(0, 2000)")
                await self.page.wait_for_timeout(1000)
            await self.page.wait_for_timeout(500)
            
            try:
                await widget.wait_for(timeout=3000)
            except:
                print(f"Compute Provision Failure Details widget not found")
                return None
            
            try:
                table = widget.locator('div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table')
                await table.wait_for(timeout=2000)
                error_codes = []
                rows = widget.locator('div.widget-box__content.z-40 > div > div.flex.flex-1.flex-col.h-full.table-widget > div > table > tbody > tr')
                row_count = await rows.count()
                for i in range(min(row_count, 20)):  # Limit to 20 rows
                    try:
                        # Get column 4 (error code)
                        col4 = rows.nth(i).locator('td:nth-child(4) > div')
                        code_text = await col4.inner_text(timeout=1000)
                        
                        # Get column 5 (error name)
                        col5 = rows.nth(i).locator('td:nth-child(5) > div')
                        name_text = await col5.inner_text(timeout=1000)
                        
                        if code_text.strip() and name_text.strip():
                            error_codes.append(f"{code_text.strip()} - {name_text.strip()}")
                    except:
                        continue
                
                if error_codes:
                    print(f"   Found Compute Provision Failure errors: {len(error_codes)} errors")
                    return error_codes  # Return as list
                else:
                    print(f"   Compute Provision Failure Details: No error codes found")
                    return None
                    
            except:
                try:
                    content_div = widget.locator('div.text-deemphasized.w-full.h-full.flex.items-center.justify-center.border-t.border-normal.shadow-base.shadow-inner-md')
                    content_text = await content_div.inner_text(timeout=2000)
                    if "Search completed. No results found" in content_text or "Searching" in content_text:
                        print(f"Compute Provision Failure Details: No results found")
                        return None
                    else:
                        print(f"Compute Provision Failure Details: No results found")
                        return None  # Don't return text, only structured data
                except:
                    print(f"Compute Provision Failure Details: No results found")
                    return None
                
        except Exception as e:
            print(f"Could not extract Compute Provision Failure Details: {e}")
            return None
    
    async def generate_summary(self):
        """Generate summary based on all errors."""
        try:
            print(f"Scrolling down to reveal all widgets...")
            await self.page.evaluate("""
                () => {
                    window.scrollBy(0, 1000);
                }
            """)
            await self.page.wait_for_timeout(1500)
        except Exception as e:
            print(f"Could not scroll: {e}")
        self.errors_dict = {}
        errors = []
        
        # Check JWT generation failed
        jwt_count = await self.get_jwt_generation_failed()
        if jwt_count is not None and jwt_count > 0:
            errors.append(f"{jwt_count} JWT generation failed")
            self.errors_dict['jwt'] = jwt_count
        
        # Check Subscription Key Claim Failure
        subscription_count = await self.get_subscription_key_claim_failure()
        if subscription_count is not None and subscription_count > 0:
            errors.append(f"{subscription_count} Subscription Key Claim Failure While JWT Generation")
            self.errors_dict['subscription'] = subscription_count
        
        # Check Device not available GLP Pool
        device_count = await self.get_device_not_available_glp_pool()
        if device_count is not None and device_count > 0:
            errors.append(f"{device_count} Device not available GLP Pool")
            self.errors_dict['device'] = device_count
        
        # Check Location/Tags/Sdc Patch Failure Count
        sdc_count = await self.get_location_tags_sdc_patch_failure()
        if sdc_count is not None and sdc_count > 0:
            errors.append(f"{sdc_count} Location/Tags/Sdc Patch Failure Count")
            self.errors_dict['location'] = sdc_count
            
            # If SDC count > 0, get error details
            sdc_errors = await self.get_sdc_patch_failure_errors()
            if sdc_errors is not None:
                self.errors_dict['sdc_details'] = sdc_errors[:100]
        
        # Check OAE Errors
        oae_errors = await self.get_oae_errors()
        if oae_errors is not None and isinstance(oae_errors, list):
            self.errors_dict['oae'] = oae_errors  # Store as list
        
        # Check Simple Error Codes (skip - no structured data returned)
        simple_errors = await self.get_error_codes_simple()
        
        # Check Table Error Codes
        table_errors = await self.get_table_error_codes()
        if table_errors is not None and isinstance(table_errors, list):
            self.errors_dict['table'] = table_errors
        
        # Check PIN Generation Failure Details
        pin_errors = await self.get_pin_generation_failure_details()
        if pin_errors is not None and isinstance(pin_errors, list):
            self.errors_dict['pin'] = pin_errors  # Store as list
        
        # Check Compute Provision Failure Details
        compute_errors = await self.get_compute_provision_failure_details()
        if compute_errors is not None and isinstance(compute_errors, list):
            self.errors_dict['compute'] = compute_errors  # Store as list
        
        # Generate result
        if errors or self.errors_dict:
            if errors:
                errors_text = " | ".join(errors)
                self.result = f"   ✗ {self.dashboard_name} - {errors_text}"
            else:
                self.result = f"   ✗ {self.dashboard_name} - Has errors"
        else:
            self.result = f"   ✓ {self.dashboard_name} - No errors"
    
    async def run_checks(self):
        """Run dashboard-specific checks and automation."""
        print("Running Dashboard Type 3 checks...")
        await self.page.wait_for_timeout(2000)
        is_correct_dashboard = await self.verify_dashboard()
        if not is_correct_dashboard:
            self.result = f"   ✗ {self.dashboard_name} - Dashboard verification failed"
            print(self.result)
            return self.result
        await self.generate_summary()
        print(self.result)
        return self.result


class DashboardType4Automation:
    """Automation logic for Dashboard Type 4 - Service-Errors Filter Known Issues."""
    
    def __init__(self, page):
        """Initialize with Playwright page object."""
        self.page = page
        self.dashboard_name = "Service-Errors Filter Known Issues"
        self.result = None
        self.service_errors = {}

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

    async def extract_service_errors(self):
        """Extract service-specific errors for zinc-app, roundup, neptune, keysmith, charger."""
        services = ["zinc-app", "roundup", "neptune", "keysmith", "charger"]
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
    
    async def run_checks(self):
        """Run dashboard-specific checks and automation."""
        print("Running Dashboard Type 4 checks...")
        await self.page.wait_for_timeout(2000)
        await self.extract_service_errors()
        self.result = f"   ✓ {self.dashboard_name} - Completed"
        print(self.result)
        return self.result


# Map dashboard types to their automation classes
DASHBOARD_AUTOMATION = {
    "dashboard_type_1": DashboardType1Automation,
    "dashboard_type_2": DashboardType2Automation,
    "dashboard_type_3": DashboardType3Automation,
    "dashboard_type_4": DashboardType4Automation,
}


async def run_all_dashboards_in_environment(environment):
    """
    Run automation for all 4 dashboard types in a specific environment.
    Logs in once, then runs all dashboards without re-logging in.
    
    Args:
        environment: Environment name (env1, env2, env3, env4)
    """
    print(f"\n{'='*70}")
    print(f"Environment: {environment}")
    print(f"{'='*70}\n")
    
    # Login once for the entire environment
    dashboard_urls = DASHBOARD_URLS[environment]
    first_url = list(dashboard_urls.values())[0]  # Get first dashboard URL for login
    
    print("Step 1: Logging in once for the environment...")
    login_automation = HumioLoginAutomation(dashboard_url=first_url)
    success = await login_automation.run()
    if not success:
        print(f"Login failed for {environment}")
        return False
    page = login_automation.page
    print(f"\nLogin successful. Session will be reused for all dashboards.\n")
    results = []
    
    for dashboard_type, dashboard_url in dashboard_urls.items():
        print(f"\nStep 2.{list(dashboard_urls.keys()).index(dashboard_type) + 1}: Processing {dashboard_type}...")
        print(f"   Dashboard URL: {dashboard_url}")
        if dashboard_url != first_url:
            print(f"   Navigating to {dashboard_type}...")
            await page.goto(dashboard_url, wait_until="networkidle")
            await page.wait_for_load_state("networkidle")
            print(f"Navigation completed")
        else:
            print(f"Already on {dashboard_type} from login - skipping navigation")
        print(f"Creating automation instance for {dashboard_type}...")
        automation_class = DASHBOARD_AUTOMATION[dashboard_type]
        dashboard_automation = automation_class(page)
        print(f"Calling run_checks()...")
        result = await dashboard_automation.run_checks()
        results.append(result)
        print(f"Checks completed for {dashboard_type}")
    
    # Print final summary
    print(f"\n{'='*70}")
    print(f"SUMMARY FOR {environment.upper()}")
    print(f"{'='*70}")
    for result in results:
        print(result)
    print(f"{'='*70}\n")
    
    # Keep browser open at the end
    print("Browser will remain open. Close manually when done.")
    await login_automation.cleanup()
    
    return True


async def run_single_dashboard(environment, dashboard_type):
    """
    Run automation for a single dashboard in a specific environment.
    
    Args:
        environment: Environment name (env1, env2, env3, env4)
        dashboard_type: Type of dashboard (dashboard_type_1, etc.)
    """
    print(f"\n{'='*70}")
    print(f"Environment: {environment}")
    print(f"Dashboard Type: {dashboard_type}")
    print(f"{'='*70}\n")
    
    dashboard_url = DASHBOARD_URLS[environment][dashboard_type]
    print("Step 1: Logging in...")
    login_automation = HumioLoginAutomation(dashboard_url=dashboard_url)    
    success = await login_automation.run()
    if not success:
        print(f"Login failed for {dashboard_type} in {environment}")
        return False
    
    print(f"\nStep 2: Running {dashboard_type} automation...")
    automation_class = DASHBOARD_AUTOMATION[dashboard_type]
    dashboard_automation = automation_class(login_automation.page)
    await dashboard_automation.run_checks() 
    print(f"\n{'='*70}")
    print(f"Automation completed for {dashboard_type} in {environment}")
    print(f"{'='*70}\n")
    print("Browser will remain open. Close manually when done.")
    await login_automation.cleanup()
    return True


async def run_all_environments_comprehensive_report():
    """
    Run automation for all 4 environments and generate a comprehensive summary report.
    Uses a single browser session and navigates between all dashboards.
    """
    from datetime import datetime
    
    env_display_names = {
        "env1": "PRE-PROD",
        "env2": "ANE1",
        "env3": "EUC1",
        "env4": "USW2"
    }
    all_results = {}
    print(f"\n{'='*70}")
    print(f"COMPREHENSIVE HUMIO AUTOMATION REPORT")
    print(f"{'='*70}\n")
    print("Initializing browser session...")
    login_automation = HumioLoginAutomation(dashboard_url=DASHBOARD_URLS["env1"]["dashboard_type_1"])
    success = await login_automation.run()
    if not success:
        print("Initial login failed. Cannot continue.")
        all_results[env_display_names["env1"]] = {"status": "LOGIN_FAILED", "error": "Initial login failed"}
        success = False
    else:
        print("Browser session initialized\n")
        page = login_automation.page
    try:
        if success:
            for env_key in ["env1", "env2", "env3", "env4"]:
                env_display = env_display_names[env_key]
                print(f"\n{'='*70}")
                print(f"Processing {env_display} ({env_key})")
                print(f"{'='*70}")
                dashboard_urls = DASHBOARD_URLS[env_key]
                env_results = {}
                
                try:
                    dashboard_list = list(dashboard_urls.items())
                    for idx, (dashboard_type, dashboard_url) in enumerate(dashboard_list):
                        dashboard_name = {
                            "dashboard_type_1": "Data Ingestion",
                            "dashboard_type_2": "COM Subscription",
                            "dashboard_type_3": "Activation Keys",
                            "dashboard_type_4": "Service-Errors"
                        }.get(dashboard_type, dashboard_type)
                        
                        try:
                            if not (env_key == "env1" and idx == 0):
                                print(f"\n[{env_display}] Navigating to {dashboard_name}...")
                                await page.goto(dashboard_url, wait_until="networkidle")
                                await page.wait_for_load_state("networkidle")
                                await page.wait_for_timeout(2000)
                                print(f"[{env_display}] Navigation completed")
                            else:
                                print(f"\n[{env_display}] Already on {dashboard_name}")
                            
                            print(f"[{env_display}] Running checks for {dashboard_name}...")
                            automation_class = DASHBOARD_AUTOMATION[dashboard_type]
                            dashboard_automation = automation_class(page)
                            await dashboard_automation.run_checks()
                            env_results[dashboard_type] = dashboard_automation
                            print(f"[{env_display}] Checks completed for {dashboard_name}")
                            
                        except Exception as e:
                            print(f"[{env_display}] Error processing {dashboard_name}: {e}")
                            env_results[dashboard_type] = f"Error: {str(e)}"
                            continue
                    
                    all_results[env_display] = env_results
                    
                except Exception as e:
                    print(f"[{env_display}] ✗ Critical error: {e}")
                    import traceback
                    traceback.print_exc()
                    all_results[env_display] = {"status": "FAILED", "error": str(e)}
                    continue
    
    finally:
        # Cleanup browser at the end
        print(f"\n{'='*70}")
        print("Closing browser session...")
        if success:
            try:
                login_automation.keep_open = False
                await login_automation.cleanup()
                print("✓ Browser closed")
            except Exception as cleanup_error:
                print(f"⚠ Cleanup error: {cleanup_error}")
        else:
            print("⚠ Skipping cleanup (login not established)")
    
    from datetime import datetime
    
    def _ordinal(n: int) -> str:
        if 10 <= n % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"

    def _summarize_errors(errors):
        """Count duplicates and format with occurrence count."""
        from collections import Counter
        counter = Counter(errors)
        summarized = []
        for text, count in counter.items():
            if count > 1:
                summarized.append(f"{text} - occurred {count} times")
            else:
                summarized.append(text)
        return summarized

    report_lines = []
    now = datetime.now()
    report_lines.append(f"{_ordinal(now.day)} {now.strftime('%B')}")
    dashboard_display_names = {
        "dashboard_type_2": "COM Subscription And Consumption",
        "dashboard_type_1": "Data Ingestion to Sustainability Insight Center",
        "dashboard_type_3": "Activation Keys Onboarding",
        "dashboard_type_4": "Service-Errors Filter Known Issues"
    }
    
    # Process each environment in order
    for env_display in ["PRE-PROD", "ANE1", "EUC1", "USW2"]:
        if env_display in all_results:
            report_lines.append(f"\n{env_display}")
            env_data = all_results[env_display]
            if isinstance(env_data, dict) and env_data.get("status") in ["LOGIN_FAILED", "FAILED"]:
                report_lines.append(f"✗ {env_data.get('error', 'Failed')}")
                continue
            
            # Show results for each dashboard type in specified order
            dashboard_order = ["dashboard_type_2", "dashboard_type_1", "dashboard_type_3", "dashboard_type_4"]
            for db_type in dashboard_order:
                if db_type in env_data:
                    db_display = dashboard_display_names[db_type]
                    report_lines.append(f"•\t{db_display}")
                    dashboard_obj = env_data[db_type]
                    
                    # Handle Type 3 dashboard with structured errors
                    if db_type == "dashboard_type_3":
                        if hasattr(dashboard_obj, 'errors_dict') and dashboard_obj.errors_dict:
                            errors_dict = dashboard_obj.errors_dict
                            error_count = 0
                            
                            if 'oae' in errors_dict and isinstance(errors_dict['oae'], list) and errors_dict['oae']:
                                report_lines.append("o\tError Details During iLO Onboard Activation Job")
                                for error_item in _summarize_errors(errors_dict['oae']):
                                    report_lines.append(f"\t{error_item}")
                                    error_count += 1
                            
                            if 'table' in errors_dict and isinstance(errors_dict['table'], list) and errors_dict['table']:
                                report_lines.append("o\tSubscription key assignment failure details")
                                for error_item in _summarize_errors(errors_dict['table']):
                                    report_lines.append(f"\t{error_item}")
                                    error_count += 1
                            
                            if 'pin' in errors_dict and isinstance(errors_dict['pin'], list) and errors_dict['pin']:
                                report_lines.append("o\tPIN Generation Failure")
                                for error_item in _summarize_errors(errors_dict['pin']):
                                    report_lines.append(f"\t{error_item}")
                                    error_count += 1
                            
                            if 'compute' in errors_dict and isinstance(errors_dict['compute'], list) and errors_dict['compute']:
                                report_lines.append("o\tCompute Provision Failure Details")
                                for error_item in _summarize_errors(errors_dict['compute']):
                                    report_lines.append(f"\t{error_item}")
                                    error_count += 1
                            
                            if 'jwt' in errors_dict:
                                report_lines.append(f"o\tJWT generation failed - {errors_dict['jwt']}")
                                error_count += 1
                            if 'subscription' in errors_dict:
                                report_lines.append(f"o\tSubscription Key Claim Failure - {errors_dict['subscription']}")
                                error_count += 1
                            if 'device' in errors_dict:
                                report_lines.append(f"o\tDevice not available GLP Pool - {errors_dict['device']}")
                                error_count += 1
                            if 'location' in errors_dict:
                                report_lines.append(f"o\tLocation/Tags/Sdc Patch Failure - {errors_dict['location']}")
                                error_count += 1
                            
                            if error_count == 0:
                                report_lines.append("o\tNo errors")
                        else:
                            report_lines.append("o\tNo errors")
                    
                    # Handle Type 4 dashboard with services
                    # elif db_type == "dashboard_type_4":
    #                        if hasattr(dashboard_obj, 'service_errors') and dashboard_obj.service_errors:
    #                            service_order = ["zinc-app", "roundup", "neptune", "keysmith", "charger"]
    #                            for service in service_order:
    #                                errors = dashboard_obj.service_errors.get(service, [])
    #                                if errors:
    #                                    report_lines.append(f"o\t{service}")
    #                                    for err in errors:
    #                                        report_lines.append(f"\t{err}")
    #                                else:
    #                                    report_lines.append(f"o\t{service} - No errors")
    #                        else:
    #                            report_lines.append("o\tNo errors")
                    
                    
                    # Handle Type 1 and Type 2
                    else:
                        if hasattr(dashboard_obj, 'result'):
                            result = dashboard_obj.result
                            if "No errors" in result:
                                report_lines.append(f"o\tNo errors")
                            elif " - " in result:
                                # Extract errors after the " - "
                                parts = result.split(" - ", 1)
                                if len(parts) > 1:
                                    errors = parts[1].split(" | ")
                                    for error in errors:
                                        error_clean = error.strip()
                                        if error_clean:
                                            report_lines.append(f"o\t{error_clean}")
                            else:
                                report_lines.append(f"o\tNo data")
                        else:
                            report_lines.append(f"o\tNo data")
    
    # Print the formatted report
    print(f"\n{'='*70}")
    print(f"FINAL SUMMARY REPORT")
    print(f"{'='*70}\n")
    for line in report_lines:
        print(line)
    
    print(f"\n{'='*70}")
    print(f"REPORT GENERATION COMPLETE")
    print(f"{'='*70}\n")
async def main():
    # Run all environments and generate comprehensive report
    await run_all_environments_comprehensive_report()
    
    # to run single environment
    # await run_all_dashboards_in_environment(environment="env1")
    
    # to run single dashboard
    # await run_single_dashboard(environment="env1", dashboard_type="dashboard_type_1")


if __name__ == "__main__":
    asyncio.run(main())
