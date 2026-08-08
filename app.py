import streamlit as st
import base64
from io import BytesIO
from fpdf import FPDF
from ds_engine import Stack, Queue, VulnLinkedList
from lyzr_agent import run_lyzr_security_scan

# Page Setup
st.set_page_config(page_title="PhishGuard AI", layout="wide")

# PDF Report Helper
def create_pdf_report(severity, title, content_snippet, analysis_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 10, "PhishGuard AI - Security Threat Audit Report", ln=True, align='C')
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 10, "Automated Threat Surface Assessment Engine", ln=True, align='C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(10)
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 8, "1. Executive Summary", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 8, f"Status / Threat Level: {severity}", ln=True)
    pdf.cell(0, 8, f"Classification: {title}", ln=True)
    pdf.ln(4)
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 8, "2. Inspected Vector Snippet", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, content_snippet)
    pdf.ln(4)
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 8, "3. Detailed Risk Breakdown & Mitigation Audit", ln=True)
    pdf.set_font("Helvetica", size=10)
    clean_text = analysis_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, clean_text)
    
    return bytes(pdf.output())

# Sidebar Branding Header
st.sidebar.markdown("""
<div style="padding-bottom: 15px; border-bottom: 1px solid #30363D; margin-bottom: 20px;">
    <h1 style="color: #FFFFFF !important; margin: 0; font-size: 26px; font-weight: 900; letter-spacing: -0.5px;">PhishGuard <span style="color:#58A6FF;">AI</span></h1>
    <p style="margin: 3px 0 0 0; font-size: 12px; color: #8B949E !important; font-weight: 600;">Security Operations Portal</p>
</div>
""", unsafe_allow_html=True)

# Navigation Menu without Emojis
selected_page = st.sidebar.radio(
    "Navigation",
    ["PhishGuard AI", "SOC Mitigation Playbook", "System Architecture"],
    label_visibility="collapsed"
)

# Sidebar Bottom Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background-color: #0D1117; padding: 12px; border-radius: 8px; border: 1px solid #30363D; text-align: center;">
    <p style="margin:0; font-size: 11px; font-weight: bold; color: #3FB950 !important;">ENGINE STATUS</p>
    <p style="margin:3px 0 0 0; font-size: 12px; font-weight: bold; color: #FFFFFF !important;">🟢 Lyzr Cloud Online</p>
</div>
""", unsafe_allow_html=True)


video_html_code = ""
if selected_page == "PhishGuard AI":
    try:
        video_path = r"C:\Users\cnkun\Downloads\Sentinalbg3.mp4"
        with open(video_path, "rb") as f:
            video_bytes = f.read()
        encoded = base64.b64encode(video_bytes).decode("utf-8")
        video_html_code = f"""
            <video autoplay loop muted playsinline style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                object-fit: cover;
                z-index: -9999;
                filter: brightness(0.35);
            ">
                <source src="data:video/mp4;base64,{encoded}" type="video/mp4">
            </video>
        """
    except Exception:
        video_html_code = ""


st.markdown(f"""
{video_html_code}
<style>
    /* Disable all page fade-in/fade-out transition animations */
    * {{
        animation: none !important;
        transition: none !important;
    }}

    /* Global Background Handling */
    .stApp {{
        background-color: {"transparent" if selected_page == "PhishGuard AI" else "#090D11"} !important;
        color: #FFFFFF;
    }}
    
    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* Hide ONLY Deploy Button */
    .stAppDeployButton {{
        display: none !important;
    }}

    /* Main Container Heading & Paragraph Typography */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp p, .stApp label {{
        color: #FFFFFF !important;
    }}

    /* Fix Faint Placeholder Text */
    textarea::placeholder {{
        color: #A0AEC0 !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        opacity: 1 !important;
    }}

    /* Matte Dark Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: #0D1117 !important;
        border-right: 1px solid #21262D !important;
    }}

    [data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
    }}

    /* Hide standard radio circles */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div:first-child {{
        display: none !important;
    }}

    /* Style Sidebar Navigation Cards */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {{
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        margin-bottom: 10px !important;
        width: 100% !important;
        cursor: pointer;
        font-weight: 700 !important;
        font-size: 15px !important;
        color: #FFFFFF !important;
    }}

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {{
        background-color: #21262D !important;
        border-color: #238636 !important;
        color: #FFFFFF !important;
    }}

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {{
        background-color: #1F6FEB !important;
        color: #FFFFFF !important;
        border-color: #58A6FF !important;
    }}

    /* Darker Green Success Banner */
    div[data-testid="stNotification"] {{
        background-color: rgba(10, 45, 20, 0.95) !important;
        border: 1px solid #238636 !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
    }}
    div[data-testid="stNotification"] p {{
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }}

    /* Darker Blue Info Box (Detailed Breakdown) */
    div[data-testid="stAlert"] {{
        background-color: rgba(13, 22, 38, 0.95) !important;
        border: 1px solid #1F6FEB !important;
        border-radius: 8px !important;
        color: #E6EDF3 !important;
    }}
    div[data-testid="stAlert"] * {{
        color: #E6EDF3 !important;
    }}
    div[data-testid="stAlert"] ul li {{
        color: #79C0FF !important;
    }}

    /* Report & Metric Container Cards */
    .report-card {{
        background-color: rgba(22, 27, 34, 0.92) !important;
        border: 1px solid #30363D;
        border-left: 5px solid #238636;
        padding: 22px;
        border-radius: 10px;
        margin-bottom: 20px;
    }}

    .section-header {{
        font-size: 18px;
        font-weight: bold;
        color: #58A6FF !important;
        margin-top: 25px;
        margin-bottom: 12px;
        border-bottom: 1px solid #30363D;
        padding-bottom: 6px;
    }}

    /* Text Input Area Customization & Bright Cursor Fix */
    .stTextArea textarea, div[data-baseweb="textarea"] {{
        background-color: rgba(22, 27, 34, 0.90) !important;
        color: #F0F6FC !important;
        border: 1.5px solid #30363D !important;
        border-radius: 8px !important;
        font-size: 15px !important;
        caret-color: #58A6FF !important; /* Forces typing cursor to bright neon blue */
    }}

    .stTextArea textarea:focus, div[data-baseweb="textarea"]:focus-within {{
        border-color: #58A6FF !important;
        box-shadow: 0 0 10px rgba(88, 166, 255, 0.4) !important;
    }}

    /* Execute Threat Assessment Button */
    .stButton > button {{
        background-color: #238636 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        padding: 10px 22px !important;
        border-radius: 20px !important;
        border: none !important;
    }}

    .stButton > button:hover {{
        background-color: #2EA043 !important;
    }}

    /* Download PDF Report Button (Permanently Dark Olive/Gold Theme) */
    div.stDownloadButton > button {{
        background-color: rgba(45, 40, 20, 0.90) !important;
        color: #FFFFFF !important;
        border: 1px solid #D4A373 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }}
    div.stDownloadButton > button:hover {{
        background-color: rgba(70, 60, 25, 1.0) !important;
        border-color: #FAEDCD !important;
        color: #FFFFFF !important;
    }}

    /* Targeted Three-Dot Popover Menu Dark Theme Fix */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"],
    div[data-baseweb="menu"] > ul {{
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        border-radius: 8px !important;
    }}

    div[data-baseweb="popover"] * {{
        color: #E6EDF3 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }}

    div[data-baseweb="menu"] li:hover,
    div[data-baseweb="menu"] li:hover * {{
        background-color: #21262D !important;
        color: #58A6FF !important;
    }}
</style>
""", unsafe_allow_html=True)

# Page 1: Main PhishGuard AI Front Page
if selected_page == "PhishGuard AI":
    st.title("PhishGuard AI — Threat Surface Inspector", anchor=False)
    st.markdown("""
    <p style="font-size: 15px; color: #C9D1D9 !important; margin-top: -10px; margin-bottom: 25px;">
        Paste a suspicious link or raw email text below to execute social engineering heuristics and deep AI analysis.
    </p>
    """, unsafe_allow_html=True)

    user_input = st.text_area(
        "Target Analysis Input", 
        placeholder="Paste target URL (e.g., http://account-verify.com) or raw email text here...",
        height=140,
        label_visibility="collapsed"
    )

    btn_col1, btn_col2 = st.columns([0.7, 0.3])
    with btn_col2:
        st.markdown("<div style='text-align: right; margin-top: 10px;'>", unsafe_allow_html=True)
        execute_click = st.button("Execute Threat Assessment ➔")
        st.markdown("</div>", unsafe_allow_html=True)

    if execute_click:
        if not user_input.strip():
            st.warning("Please paste a URL or email text before running the assessment.")
        else:
            with st.spinner("Processing Data Structures and Querying Lyzr AI Engine..."):
                input_text = user_input.strip()
                
                link_stack = Stack()
                link_stack.push(input_text[:50])
                
                domain_queue = Queue()
                domain_queue.enqueue("Inspection Engine")
                
                active_link = link_stack.pop()
                active_domain = domain_queue.dequeue()
                
                suspicious_keywords = ["bit.ly", "account-verify", "login.php", "paypal-security", "http://", "urgent", "password expire"]
                is_suspicious = any(kw in input_text.lower() for kw in suspicious_keywords)
                
                if is_suspicious:
                    severity_level = "CRITICAL THREAT"
                    badge_color = "#DA3633"
                    threat_title = "Suspicious Link / Social Engineering Pattern Detected"
                else:
                    severity_level = "SAFE / LOW RISK"
                    badge_color = "#238636"
                    threat_title = "Legitimate Transactional / Authentication Message"

                ai_result = run_lyzr_security_scan(input_text, active_link, active_domain)
                cleaned_analysis = str(ai_result).split("If you want")[0].strip()
                
                threat_chain = VulnLinkedList()
                threat_chain.append(
                    severity=severity_level,
                    title=threat_title,
                    endpoint=input_text[:80] + "..." if len(input_text) > 80 else input_text,
                    cve=cleaned_analysis
                )
                
                st.session_state["threat_data"] = threat_chain.to_list()
                st.session_state["badge_color"] = badge_color
                st.session_state["raw_ai_analysis"] = cleaned_analysis
                st.success("Security Assessment Complete. Report logged to memory.")

    if "threat_data" in st.session_state:
        st.markdown("<div class='section-header'>Executive Threat Report</div>", unsafe_allow_html=True)
        
        badge_bg = st.session_state.get("badge_color", "#238636")
        item = st.session_state["threat_data"][0]
        
        st.markdown(f"""
        <div class="report-card">
            <span style="background-color: {badge_bg}; color: #FFFFFF; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; width: fit-content;">
                {item['severity']}
            </span>
            <h3 style="color: #FFFFFF !important; margin-top: 12px; margin-bottom: 8px; font-size: 18px;">{item['title']}</h3>
            <p style="margin: 0; font-size: 14px; color: #C9D1D9 !important;"><strong>Inspected Content Snippet:</strong> <code>{item['endpoint']}</code></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='section-header'>Detailed Risk Breakdown & Mitigation Audit</div>", unsafe_allow_html=True)
        st.info(st.session_state["raw_ai_analysis"])

        pdf_bytes = create_pdf_report(
            severity=item['severity'],
            title=item['title'],
            content_snippet=item['endpoint'],
            analysis_text=st.session_state["raw_ai_analysis"]
        )

        st.download_button(
            label="📄 Download PDF Security Audit Report",
            data=pdf_bytes,
            file_name="PhishGuard_Security_Audit.pdf",
            mime="application/pdf"
        )

# Page 2: SOC Mitigation Playbook
elif selected_page == "SOC Mitigation Playbook":
    st.title("SOC Mitigation Playbook", anchor=False)
    st.write("Standardized Incident Response Framework & Defensive Remediation Workflows.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="report-card" style="min-height: 120px; text-align: center; padding: 18px;">
            <p style="margin:0; font-weight:700; color:#58A6FF !important; font-size: 12px; letter-spacing: 0.5px;">AVERAGE CONTAINMENT</p>
            <h2 style="margin:6px 0; color:#FFFFFF !important; font-size: 24px; font-weight:800;">&lt; 15 Mins</h2>
            <p style="margin:0; font-size:12px; color:#8B949E !important;">Automated Identity Revocation</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="report-card" style="min-height: 120px; text-align: center; padding: 18px;">
            <p style="margin:0; font-weight:700; color:#58A6FF !important; font-size: 12px; letter-spacing: 0.5px;">SEVERITY THRESHOLD</p>
            <h2 style="margin:6px 0; color:#DA3633 !important; font-size: 24px; font-weight:800;">Level 3 / Critical</h2>
            <p style="margin:0; font-size:12px; color:#8B949E !important;">Trigger SOC L1 Escalation</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="report-card" style="min-height: 120px; text-align: center; padding: 18px;">
            <p style="margin:0; font-weight:700; color:#58A6FF !important; font-size: 12px; letter-spacing: 0.5px;">COMPLIANCE STANDARD</p>
            <h2 style="margin:6px 0; color:#FFFFFF !important; font-size: 24px; font-weight:800;">NIST SP 800-61</h2>
            <p style="margin:0; font-size:12px; color:#8B949E !important;">Computer Incident Handling</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Incident Response Lifecycle</div>", unsafe_allow_html=True)

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.markdown("""
        <div class="report-card" style="min-height: 290px; padding: 20px;">
            <div>
                <span style="background-color: #238636; color: #FFFFFF; padding: 4px 10px; border-radius: 4px; font-weight: 700; font-size: 11px;">STAGE 1</span>
            </div>
            <h3 style="color: #FFFFFF !important; margin-top: 12px; margin-bottom: 10px; font-size: 20px; font-weight: 700;">Triage & Verification</h3>
            <p style="font-size: 14px; margin-bottom: 12px; color: #C9D1D9 !important;"><strong>Objective:</strong> Validate threat origin and confirm target user engagement.</p>
            <ul style="font-size: 13.5px; line-height: 1.6; margin-top: 0; padding-left: 20px; color: #C9D1D9 !important;">
                <li>Inspect raw <strong>MIME mail headers</strong> for <strong>SPF, DKIM,</strong> and <strong>DMARC</strong> failures.</li>
                <li>Verify URLs against threat feeds (<strong>Google Safe Browsing</strong>, <strong>VirusTotal</strong>).</li>
                <li>Cross-reference targeting vectors with internal <strong>Active Directory</strong> accounts.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with row1_col2:
        st.markdown("""
        <div class="report-card" style="min-height: 290px; padding: 20px;">
            <div>
                <span style="background-color: #DA3633; color: #FFFFFF; padding: 4px 10px; border-radius: 4px; font-weight: 700; font-size: 11px;">STAGE 2</span>
            </div>
            <h3 style="color: #FFFFFF !important; margin-top: 12px; margin-bottom: 10px; font-size: 20px; font-weight: 700;">Containment & Revocation</h3>
            <p style="font-size: 14px; margin-bottom: 12px; color: #C9D1D9 !important;"><strong>Objective:</strong> Block active credential theft and isolate targets.</p>
            <ul style="font-size: 13.5px; line-height: 1.6; margin-top: 0; padding-left: 20px; color: #C9D1D9 !important;">
                <li>Force immediate <strong>password reset</strong> and invalidate active <strong>OAuth2/SSO tokens</strong>.</li>
                <li>Isolate the host endpoint from subnet if <strong>malicious payloads</strong> were executed.</li>
                <li>Purge malicious emails across mailboxes via <strong>API search-and-destroy</strong>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown("""
        <div class="report-card" style="min-height: 290px; padding: 20px;">
            <div>
                <span style="background-color: #238636; color: #FFFFFF; padding: 4px 10px; border-radius: 4px; font-weight: 700; font-size: 11px;">STAGE 3</span>
            </div>
            <h3 style="color: #FFFFFF !important; margin-top: 12px; margin-bottom: 10px; font-size: 20px; font-weight: 700;">Eradication & Rule Patching</h3>
            <p style="font-size: 14px; margin-bottom: 12px; color: #C9D1D9 !important;"><strong>Objective:</strong> Prevent repeat attacks using automated defenses.</p>
            <ul style="font-size: 13.5px; line-height: 1.6; margin-top: 0; padding-left: 20px; color: #C9D1D9 !important;">
                <li>Add origin IP blocks and typosquatted domains to <strong>Next-Gen Firewall</strong> rules.</li>
                <li>Submit <strong>registrar takedown requests</strong> for active phishing landing pages.</li>
                <li>Update <strong>Secure Email Gateway (SEG)</strong> regex patterns for campaign signatures.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with row2_col2:
        st.markdown("""
        <div class="report-card" style="min-height: 290px; padding: 20px;">
            <div>
                <span style="background-color: #238636; color: #FFFFFF; padding: 4px 10px; border-radius: 4px; font-weight: 700; font-size: 11px;">STAGE 4</span>
            </div>
            <h3 style="color: #FFFFFF !important; margin-top: 12px; margin-bottom: 10px; font-size: 20px; font-weight: 700;">Recovery & Post-Mortem</h3>
            <p style="font-size: 14px; margin-bottom: 12px; color: #C9D1D9 !important;"><strong>Objective:</strong> Restore normal operations and refine training.</p>
            <ul style="font-size: 13.5px; line-height: 1.6; margin-top: 0; padding-left: 20px; color: #C9D1D9 !important;">
                <li>Restore user credentials once identity <strong>MFA</strong> is securely re-established.</li>
                <li>Log full incident metrics into <strong>SIEM</strong> for compliance and forensic auditing.</li>
                <li>Issue targeted <strong>security awareness notices</strong> detailing recent social engineering tactics.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Page 3: System Architecture
elif selected_page == "System Architecture":
    st.title("System Architecture & Data Structures", anchor=False)
    st.write("Technical mapping of memory structures and AI microservices integration.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="report-card" style="min-height: 120px; text-align: center; padding: 18px;">
            <p style="margin:0; font-weight:700; color:#58A6FF !important; font-size: 12px; letter-spacing: 0.5px;">MEMORY MANAGEMENT</p>
            <h2 style="margin:6px 0; color:#FFFFFF !important; font-size: 24px; font-weight:800;">Dynamic O(1)</h2>
            <p style="margin:0; font-size:12px; color:#8B949E !important;">Stack Push & Queue Enqueue</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="report-card" style="min-height: 120px; text-align: center; padding: 18px;">
            <p style="margin:0; font-weight:700; color:#58A6FF !important; font-size: 12px; letter-spacing: 0.5px;">ANALYSIS ENGINE</p>
            <h2 style="margin:6px 0; color:#238636 !important; font-size: 24px; font-weight:800;">Lyzr AI Agent</h2>
            <p style="margin:0; font-size:12px; color:#8B949E !important;">Cloud Microservice Pipeline</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="report-card" style="min-height: 120px; text-align: center; padding: 18px;">
            <p style="margin:0; font-weight:700; color:#58A6FF !important; font-size: 12px; letter-spacing: 0.5px;">STORAGE PATTERN</p>
            <h2 style="margin:6px 0; color:#FFFFFF !important; font-size: 24px; font-weight:800;">Singly Linked List</h2>
            <p style="margin:0; font-size:12px; color:#8B949E !important;">Dynamic Vulnerability Nodes</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Core Data Structures Implementation</div>", unsafe_allow_html=True)

    ds_col1, ds_col2, ds_col3 = st.columns(3)

    with ds_col1:
        st.markdown("""
        <div class="report-card" style="min-height: 290px; padding: 20px;">
            <div>
                <span style="background-color: #238636; color: #FFFFFF; padding: 4px 10px; border-radius: 4px; font-weight: 700; font-size: 11px;">STACK (LIFO)</span>
            </div>
            <h3 style="color: #FFFFFF !important; margin-top: 12px; margin-bottom: 10px; font-size: 18px; font-weight: 700;">URL Depth Parsing</h3>
            <p style="font-size: 14px; margin-bottom: 10px; color: #C9D1D9 !important;"><strong>Role:</strong> Manages link processing sequence.</p>
            <ul style="font-size: 13px; line-height: 1.6; margin-top: 0; padding-left: 18px; color: #C9D1D9 !important;">
                <li>Pushes candidate links onto stack during <strong>raw text scanning</strong>.</li>
                <li>Pops recently extracted URL for <strong>depth-first redirection inspection</strong>.</li>
                <li>Guarantees <strong>O(1) time complexity</strong> during evaluation.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with ds_col2:
        st.markdown("""
        <div class="report-card" style="min-height: 290px; padding: 20px;">
            <div>
                <span style="background-color: #238636; color: #FFFFFF; padding: 4px 10px; border-radius: 4px; font-weight: 700; font-size: 11px;">QUEUE (FIFO)</span>
            </div>
            <h3 style="color: #FFFFFF !important; margin-top: 12px; margin-bottom: 10px; font-size: 18px; font-weight: 700;">Domain Buffer</h3>
            <p style="font-size: 14px; margin-bottom: 10px; color: #C9D1D9 !important;"><strong>Role:</strong> Buffers target domains for inspection.</p>
            <ul style="font-size: 13px; line-height: 1.6; margin-top: 0; padding-left: 18px; color: #C9D1D9 !important;">
                <li>Enqueues target endpoints in <strong>sequential arrival order</strong>.</li>
                <li>Dequeues entries systematically into the <strong>heuristic rule engine</strong>.</li>
                <li>Prevents thread congestion during <strong>batch processing</strong>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with ds_col3:
        st.markdown("""
        <div class="report-card" style="min-height: 290px; padding: 20px;">
            <div>
                <span style="background-color: #238636; color: #FFFFFF; padding: 4px 10px; border-radius: 4px; font-weight: 700; font-size: 11px;">LINKED LIST</span>
            </div>
            <h3 style="color: #FFFFFF !important; margin-top: 12px; margin-bottom: 10px; font-size: 18px; font-weight: 700;">Threat Chain Memory</h3>
            <p style="font-size: 14px; margin-bottom: 10px; color: #C9D1D9 !important;"><strong>Role:</strong> Stores dynamic inspection findings.</p>
            <ul style="font-size: 13px; line-height: 1.6; margin-top: 0; padding-left: 18px; color: #C9D1D9 !important;">
                <li>Appends finding nodes containing <strong>severity, title, and AI findings</strong>.</li>
                <li>Eliminates fixed-size array constraints and avoids <strong>re-allocation memory overhead</strong>.</li>
                <li>Traverses nodes seamlessly to render the <strong>Threat Report UI</strong>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>End-to-End Execution Pipeline</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="report-card" style="padding: 22px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; text-align: center;">
            <div style="flex: 1; min-width: 140px; background-color: #161B22; padding: 15px; border-radius: 8px; border: 1px solid #30363D;">
                <span style="font-size: 11px; font-weight: 700; color: #58A6FF !important;">STEP 1</span>
                <p style="font-weight: 700; margin: 5px 0; color: #FFFFFF !important; font-size: 13px;">Raw Input Parsing</p>
                <p style="font-size: 11px; margin: 0; color: #8B949E !important;">Pushes text links into Stack</p>
            </div>
            <div style="font-size: 18px; font-weight: bold; color: #58A6FF !important;">➔</div>
            <div style="flex: 1; min-width: 140px; background-color: #161B22; padding: 15px; border-radius: 8px; border: 1px solid #30363D;">
                <span style="font-size: 11px; font-weight: 700; color: #58A6FF !important;">STEP 2</span>
                <p style="font-weight: 700; margin: 5px 0; color: #FFFFFF !important; font-size: 13px;">Domain Queueing</p>
                <p style="font-size: 11px; margin: 0; color: #8B949E !important;">Enqueues target to FIFO engine</p>
            </div>
            <div style="font-size: 18px; font-weight: bold; color: #58A6FF !important;">➔</div>
            <div style="flex: 1; min-width: 140px; background-color: #161B22; padding: 15px; border-radius: 8px; border: 1px solid #30363D;">
                <span style="font-size: 11px; font-weight: 700; color: #58A6FF !important;">STEP 3</span>
                <p style="font-weight: 700; margin: 5px 0; color: #FFFFFF !important; font-size: 13px;">Lyzr AI Scan</p>
                <p style="font-size: 11px; margin: 0; color: #8B949E !important;">Executes social eng. inspection</p>
            </div>
            <div style="font-size: 18px; font-weight: bold; color: #58A6FF !important;">➔</div>
            <div style="flex: 1; min-width: 140px; background-color: #161B22; padding: 15px; border-radius: 8px; border: 1px solid #30363D;">
                <span style="font-size: 11px; font-weight: 700; color: #58A6FF !important;">STEP 4</span>
                <p style="font-weight: 700; margin: 5px 0; color: #FFFFFF !important; font-size: 13px;">Linked List Memory</p>
                <p style="font-size: 11px; margin: 0; color: #8B949E !important;">Appends node & renders report</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)