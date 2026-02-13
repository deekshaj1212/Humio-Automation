import asyncio
from datetime import datetime
from collections import Counter
from login_automation import HumioLoginAutomation
from dashboard_type1 import DashboardType1Automation
from dashboard_type2 import DashboardType2Automation
from dashboard_type3 import DashboardType3Automation
from dashboard_type4 import DashboardType4Automation

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

DASHBOARD_AUTOMATION = {
    "dashboard_type_1": DashboardType1Automation,
    "dashboard_type_2": DashboardType2Automation,
    "dashboard_type_3": DashboardType3Automation,
    "dashboard_type_4": DashboardType4Automation,
}

async def run_all_dashboards_in_environment(environment):
    print(f"\n{'='*70}")
    print(f"Environment: {environment}")
    print(f"{'='*70}\n")
    dashboard_urls = DASHBOARD_URLS[environment]
    first_url = list(dashboard_urls.values())[0]
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
            print("Navigation completed")
        else:
            print(f"Already on {dashboard_type} from login - skipping navigation")
        print(f"Creating automation instance for {dashboard_type}...")
        automation_class = DASHBOARD_AUTOMATION[dashboard_type]
        if dashboard_type == "dashboard_type_4":
            dashboard_automation = automation_class(page, environment=environment)
        else:
            dashboard_automation = automation_class(page)
        print("Calling run_checks()...")
        result = await dashboard_automation.run_checks()
        results.append(result)
        print(f"Checks completed for {dashboard_type}")

    print(f"\n{'='*70}")
    print(f"SUMMARY FOR {environment.upper()}")
    print(f"{'='*70}")
    for result in results:
        print(result)
    print(f"{'='*70}\n")
    print("Browser will remain open. Close manually when done.")
    await login_automation.cleanup()
    return True

async def run_single_dashboard(environment, dashboard_type):
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
    if dashboard_type == "dashboard_type_4":
        dashboard_automation = automation_class(login_automation.page, environment=environment)
    else:
        dashboard_automation = automation_class(login_automation.page)
    await dashboard_automation.run_checks()
    print(f"\n{'='*70}")
    print(f"Automation completed for {dashboard_type} in {environment}")
    print(f"{'='*70}\n")
    print("Browser will remain open. Close manually when done.")
    await login_automation.cleanup()
    return True

async def run_all_environments_comprehensive_report():
    env_display_names = {
        "env1": "PRE-PROD",
        "env2": "ANE1",
        "env3": "EUC1",
        "env4": "USW2",
    }
    all_results = {}
    print(f"\n{'='*70}")
    print("COMPREHENSIVE HUMIO AUTOMATION REPORT")
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
                            "dashboard_type_4": "Service-Errors",
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
                            if dashboard_type == "dashboard_type_4":
                                dashboard_automation = automation_class(page, environment=env_key)
                            else:
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
                    print(f"[{env_display}] Critical error: {e}")
                    import traceback
                    traceback.print_exc()
                    all_results[env_display] = {"status": "FAILED", "error": str(e)}
                    continue

    finally:
        print(f"\n{'='*70}")
        print("Closing browser session...")
        if success:
            try:
                login_automation.keep_open = False
                await login_automation.cleanup()
                print("✓ Browser closed")
            except Exception as cleanup_error:
                print(f"Cleanup error: {cleanup_error}")
        else:
            print("Skipping cleanup (login not established)")

    def _ordinal(n: int) -> str:
        if 10 <= n % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"

    def _extract_main_error(error_text):
        #Extract only the main error message from a full error text.
        import re
        
        # Remove leading dashes/brackets and spaces (e.g., "- - ", "- ", or "] ")
        error_text = re.sub(r'^[\]\-\s]+', '', error_text)
        
        # Remove leading IDs and timestamps (hex strings, UUIDs, timestamps)
        error_text = re.sub(r'^(?:[a-f0-9]{16,}\s+){1,3}', '', error_text)
        error_text = re.sub(r'^[a-f0-9-]{30,}\s+', '', error_text)
        
        # Remove file paths and line numbers
        error_text = re.sub(r'^[\w.]+:\d+\s+', '', error_text)

        # Remove leading module prefixes without line numbers
        module_prefix = re.match(r'^([A-Za-z0-9_.]+):\s+', error_text)
        if module_prefix and '.' in module_prefix.group(1):
            error_text = error_text[module_prefix.end():]
        if re.match(r'^[A-Za-z0-9_.]+$', error_text) and '.' in error_text:
            return ""
        if error_text.lower().startswith('template server:'):
            return error_text.split(':', 1)[1].strip()
        if 'Unhandled exception checking is_ready for module' in error_text:
            return error_text.strip()
        match = re.search(r'(Failed fetch messages from \d+: \w+(?:Error)?)', error_text)
        if match:
            return match.group(1)
        if 'Exception while unregistering device' in error_text:
            return 'Exception while unregistering device'
        if 'Malformed gateway command received' in error_text:
            return 'Malformed gateway command received'
        
        # Extract first sentence or phrase before detailed JSON/dict data
        match = re.match(r'^([^{\[]+?)(?:\s*[{\[]|\s{3,})', error_text)
        if match:
            main_part = match.group(1).strip()
            main_part = re.sub(r':\s*Connection at.*$', '', main_part)
            main_part = re.sub(r':\s*[a-z0-9.-]+:\d+.*$', '', main_part, flags=re.IGNORECASE)
            main_part = re.sub(r'\s+P[0-9A-Z-+]+.*$', '', main_part)
            return main_part.strip()
        
        parts = error_text.split(':')
        if len(parts) >= 2:
            if len(parts) >= 3:
                second_part = parts[1].strip()
                if (second_part.endswith(('Error', 'Exception')) or 
                    (second_part and second_part[0].isupper() and 'Error' in second_part)):
                    return f"{parts[0].strip()}: {parts[1].strip()}: {parts[2].strip()}"
            if len(parts) == 2:
                first_part = parts[0].strip()
                second_part = parts[1].strip()
                if len(first_part) < 50 and len(second_part) < 100 and len(second_part) > 5:
                    if not re.search(r'[a-z0-9.-]+:\d+', second_part, re.IGNORECASE):
                        return f"{first_part}: {second_part}"
                
            if len(parts[0].strip()) < 20 and len(parts) > 2:
                return f"{parts[0].strip()}: {parts[1].strip()}"
            return parts[0].strip()
        
        if len(error_text) > 150:
            return error_text[:150].strip() + '...'
        return error_text.strip()

    def _summarize_errors(errors):
        # Summarize errors by extracting main message and counting occurrences.
        extracted_errors = [e for e in (_extract_main_error(error) for error in errors) if e]
        counter = Counter(extracted_errors)
        summarized = []
        for text, count in counter.items():
            if count > 1:
                summarized.append(f"{text} - occurred {count} times")
            else:
                summarized.append(text)
        return summarized

    report_lines = []
    now = datetime.now()
    report_lines.append(f"**{_ordinal(now.day)} {now.strftime('%B')}**")
    dashboard_display_names = {
        "dashboard_type_2": "COM Subscription And Consumption",
        "dashboard_type_1": "Data Ingestion to Sustainability Insight Center",
        "dashboard_type_3": "Activation Keys Onboarding",
        "dashboard_type_4": "Service-Errors Filter Known Issues",
    }
    for env_display in ["PRE-PROD", "ANE1", "EUC1", "USW2"]:
        if env_display in all_results:
            report_lines.append(f"\n**{env_display}**")
            env_data = all_results[env_display]
            if isinstance(env_data, dict) and env_data.get("status") in ["LOGIN_FAILED", "FAILED"]:
                report_lines.append(f"✗ {env_data.get('error', 'Failed')}")
                continue
            dashboard_order = ["dashboard_type_2", "dashboard_type_1", "dashboard_type_3", "dashboard_type_4"]
            for db_type in dashboard_order:
                if db_type in env_data:
                    db_display = dashboard_display_names[db_type]
                    report_lines.append(f"• **{db_display}**")
                    dashboard_obj = env_data[db_type]
                    if db_type == "dashboard_type_3":
                        if hasattr(dashboard_obj, "errors_dict") and dashboard_obj.errors_dict:
                            errors_dict = dashboard_obj.errors_dict
                            error_count = 0

                            if "oae" in errors_dict and isinstance(errors_dict["oae"], list) and errors_dict["oae"]:
                                report_lines.append("  o Error Details During iLO Onboard Activation Job")
                                for error_item in _summarize_errors(errors_dict["oae"]):
                                    report_lines.append(f"    ▪ {error_item}")
                                    error_count += 1

                            if "table" in errors_dict and isinstance(errors_dict["table"], list) and errors_dict["table"]:
                                report_lines.append("  o Subscription key assignment failure details")
                                for error_item in _summarize_errors(errors_dict["table"]):
                                    report_lines.append(f"    ▪ {error_item}")
                                    error_count += 1

                            if "pin" in errors_dict and isinstance(errors_dict["pin"], list) and errors_dict["pin"]:
                                report_lines.append("  o PIN Generation Failure")
                                for error_item in _summarize_errors(errors_dict["pin"]):
                                    report_lines.append(f"    ▪ {error_item}")
                                    error_count += 1

                            if "compute" in errors_dict and isinstance(errors_dict["compute"], list) and errors_dict["compute"]:
                                report_lines.append("  o Compute Provision Failure Details")
                                for error_item in _summarize_errors(errors_dict["compute"]):
                                    report_lines.append(f"    ▪ {error_item}")
                                    error_count += 1

                            if "jwt" in errors_dict:
                                report_lines.append(f"  o JWT generation failed - {errors_dict['jwt']}")
                                error_count += 1
                            if "subscription" in errors_dict:
                                report_lines.append(f"  o Subscription Key Claim Failure - {errors_dict['subscription']}")
                                error_count += 1
                            if "device" in errors_dict:
                                report_lines.append(f"  o Device not available GLP Pool - {errors_dict['device']}")
                                error_count += 1
                            if "location" in errors_dict:
                                report_lines.append(f"  o Location/Tags/Sdc Patch Failure - {errors_dict['location']}")
                                error_count += 1
                            if error_count == 0:
                                report_lines.append("  o No errors")
                        else:
                            report_lines.append("  o No errors")

                    elif db_type == "dashboard_type_4":
                        if hasattr(dashboard_obj, "widgets") and dashboard_obj.widgets:
                            for widget_data in dashboard_obj.widgets:
                                widget_name = widget_data.get("name", "Unknown Widget")
                                widget_errors = widget_data.get("errors", [])
                                if widget_errors and isinstance(widget_errors, list):
                                    report_lines.append(f"  o {widget_name}")
                                    for error in _summarize_errors(widget_errors):
                                        if widget_name == "PII Detection Count" and error.startswith("PII Detection Count - "):
                                            error = error.replace("PII Detection Count - ", "", 1)
                                        report_lines.append(f"    ▪ {error}")
                                else:
                                    report_lines.append(f"  o {widget_name} - No errors")
                        else:
                            report_lines.append("  o No widget data available")

                    else:
                        if hasattr(dashboard_obj, "result"):
                            result = dashboard_obj.result
                            if "No errors" in result:
                                report_lines.append("  o No errors")
                            elif " - " in result:
                                parts = result.split(" - ", 1)
                                if len(parts) > 1:
                                    errors = parts[1].split(" | ")
                                    for error in errors:
                                        error_clean = error.strip()
                                        if error_clean:
                                            report_lines.append(f"  o {error_clean}")
                            else:
                                report_lines.append("  o No data")
                        else:
                            report_lines.append("  o No data")

    print(f"\n{'='*70}")
    print("FINAL SUMMARY REPORT")
    print(f"{'='*70}\n")
    for line in report_lines:
        print(line)
    print(f"\n{'='*70}")
    print("REPORT GENERATION COMPLETE")
    print(f"{'='*70}\n")

async def main():
    await run_all_environments_comprehensive_report()
    # await run_all_dashboards_in_environment(environment="env1")
    # await run_single_dashboard(environment="env4", dashboard_type="dashboard_type_4")

if __name__ == "__main__":
    asyncio.run(main())
