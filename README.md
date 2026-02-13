# Humio CloudOps Dashboard Automation

Automated error tracking and monitoring across multiple Humio CloudOps environments. Generates comprehensive summary from COM Subscription, Data Ingestion, Activation Keys, and Service Errors dashboards across 4 production environments.

## Steps to get this working:

1. **Clone the repo and install dependencies:**
   ```powershell
   pip install -r requirements.txt
   playwright install msedge
   ```

2. **Run the automation:**
   ```powershell
   python dashboard_automation_main.py
   ```

3. **Wait for the initial login to complete** where you select the browser certificate and authenticate with Windows Hello fingerprint/biometric.

4. **Let it run and wait for the script to parse through all environments** while the script:
   - Extracts error metrics and details from 16 dashboards total
   - Compiles everything into a structured summary report

5. **The monitoring summary will be generated** showing errors across:
   - **PRE-PROD** (us-west-2 pre-production)
   - **ANE1** (ap-northeast-1 production)
   - **EUC1** (eu-central-1 production)
   - **USW2** (us-west-2 production)
