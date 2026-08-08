# PhishGuard-AI
A SOC threat inspection portal powered by a C-backed memory engine (Stacks, Queues, Singly Linked Lists) and Lyzr AI agent integration for real-time phishing and social engineering detection.


# PhishGuard AI 🛡️
> **Data Structure-Driven Threat Surface & Memory Engine**

PhishGuard AI is a high-performance Security Operations Center (SOC) threat inspection portal. It combines custom C data structures (**Stack**, **Queue**, **Singly Linked List**) with an AI-powered agent (**Sentinel AI / Lyzr**) to inspect suspicious URL vectors, raw email content, and social engineering patterns in real time.

---

## 🌟 Key Features

- **LIFO Stack (Link Depth Parsing):** Unrolls and inspects nested URL redirect hops in deterministic $O(1)$ time.
- **FIFO Queue (Domain Inspection Buffer):** Buffers target domains sequentially using a circular array buffer to prevent thread congestion during high-volume scans.
- **Singly Linked List (Threat Memory):** Dynamically allocates finding nodes on the heap using `malloc()` with $O(1)$ tail-appends for persistent audit logging.
- **C-Native Engine Integration:** High-velocity memory routines written in C (`ds_engine.c`) linked seamlessly via Python `ctypes`.
- **Automated PDF Security Reports:** Generates executive threat reports detailing risk levels and NIST SP 800-61 incident response playbooks.

---

## 📁 Repository Structure

```text
SENTINALAI/
├── .streamlit/
│   ├── config.toml       # Custom dark matte UI theme settings
│   └── secrets.toml      # API keys and environment variables
├── resources/            # Media assets (background video, logos)
├── app.py                # Main Streamlit dashboard interface
├── ds_engine.c           # Core Data Structures implementation in C (DLL exports)
├── ds_engine.py          # Python ctypes bindings & fallback DS classes
├── lyzr_agent.py         # AI Threat Surface heuristic scanner agent
└── requirements.txt      # Python dependencies
