# 🍑 PeachFuzz V2

**The Modern, High-Performance, Asynchronous Web Fuzzer.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-yellow.svg)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)

PeachFuzz is a next-generation security testing tool designed for speed and usability. Built with Python's `asyncio` and `aiohttp`, it delivers blazing fast scanning capabilities wrapped in a sleek, modern GUI.

> ⚠️ **Disclaimer**: This tool is for educational purposes and authorized security testing only. Misuse of this tool to attack targets without prior mutual consent is illegal.

## ✨ Features

- **🚀 Hyper-Fast Scanning**: Powered by asynchronous networking to handle hundreds of concurrent requests.
- **🖥️ Modern Interface**: Built with `CustomTkinter` for a beautiful, dark-mode experience.
- **🛡️ Multiple Attack Vectors**:
  - **Directory Brute-forcing**: Discover hidden paths and files.
  - **SQL Injection**: Test parameters for SQLi vulnerabilities.
  - **XSS Scanning**: Detect Cross-Site Scripting flaws.
  - **LFI & Command Injection**: **[NEW]** Scan for Local File Inclusion and OS Command Injection.
- **⚙️ Advanced Configuration**:
  - **Proxy Support**: Route traffic through Burp Suite, ZAP, or other proxies.
  - **Custom Headers**: Inject Authentication tokens, Cookies, or JSON headers.
  - **User-Agent Spoofing**: **[NEW]** One-click preset for popular browsers (Chrome, Firefox, iPhone).
  - **HTTP Methods**: Support for GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD.
- **📊 Professional Reporting**:
  - Real-time clickable results log.
  - detailed Request/Response inspector.
  - Export results to **JSON** or **CSV**.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/PeachFuzz.git
    cd PeachFuzz
    ```

2.  **Set up Virtual Environment** (Recommended):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

1.  **Launch the Application**:
    ```bash
    python main.py
    ```

2.  **Configure Scan**:
    - **General Tab**: specific Target URL, Thread count, and Scan Type.
    - **Advanced Tab**: Set Proxies, User-Agents, or Custom Headers.

3.  **Start Fuzzing**:
    - Click **Start Scan** and watch the results pour in.
    - Click any result row to view the detailed request and response payload.

4.  **Export**:
    - Save your findings using the "Export Results" button for reporting.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Built with ❤️ using Antigravity*
