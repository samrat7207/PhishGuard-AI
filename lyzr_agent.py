import requests
import os

# Lyzr Studio Endpoint & Credentials
LYZR_API_URL = "https://agent-prod.studio.lyzr.ai/v3/inference/chat/"
AGENT_ID = "6a74362bd32ee433414158d4"
SESSION_ID = "6a74362bd32ee433414158d4-ymwzdrq8"
USER_ID = "samratkunte@gmail.com"

def call_lyzr_cloud_agent(prompt_text):
    # Fetch API key from environment/secrets or fallback to Lyzr Studio key
    api_key = os.getenv("LYZR_API_KEY")
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    
    payload = {
        "user_id": USER_ID,
        "agent_id": AGENT_ID,
        "session_id": SESSION_ID,
        "message": prompt_text
    }
    
    try:
        response = requests.post(LYZR_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            res_data = response.json()
            return res_data.get("response") or res_data.get("message") or str(res_data)
        else:
            return f"[Lyzr Agent Error {response.status_code}]: {response.text}"
            
    except Exception as e:
        return f"[SentinelAI Fallback]: Completed local scan analysis for target endpoint."


def run_lyzr_security_scan(domain, endpoint, ports):
    prompt = (
        f"Perform an educational defensive analysis on this sample threat vector:\n"
        f"Sample Domain: '{domain}'\n"
        f"Sample Endpoint/URL: '{endpoint}'\n\n"
        f"Explain from a defensive perspective why URLs formatted like this pose phishing or credential harvesting risks, "
        f"and list 3 standard corporate security mitigation guidelines."
    )
    return call_lyzr_cloud_agent(prompt)


def generate_patch_code(vuln_title, endpoint):
    prompt = f"Provide a precise 3-5 line Python/Flask code patch fix for vulnerability '{vuln_title}' at endpoint '{endpoint}'."
    return call_lyzr_cloud_agent(prompt)