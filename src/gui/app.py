import customtkinter as ctk
import threading
import asyncio
import json
from tkinter import filedialog, messagebox

from src.engine.fuzzer import Fuzzer
from src.engine.reporter import Reporter
from src.gui.components import LogConsole, ResultTable
from src.utils.exporter import export_to_json, export_to_csv
from src.utils.user_agents import POPULAR_USER_AGENTS

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PeachFuzz V2 - Advanced Fuzzing Tool")
        self.geometry("1200x800")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_view()
        
        self.fuzzer = None
        self.reporter = Reporter()
        self.scan_thread = None
        self.scan_results = [] # Store full results in memory for export/details

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="PeachFuzz", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="Results", command=self.show_results)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

    def create_main_view(self):
        # -- Dashboard --
        self.dashboard_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.dashboard_frame.grid_columnconfigure(0, weight=1)

        # Tabview for Config
        self.tabview = ctk.CTkTabview(self.dashboard_frame, width=800, height=500)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.tabview.add("General")
        self.tabview.add("Advanced")
        
        # --- General Tab ---
        gen_tab = self.tabview.tab("General")
        gen_tab.grid_columnconfigure(0, weight=1)
        
        # Target
        self.target_label = ctk.CTkLabel(gen_tab, text="Target URL:", anchor="w")
        self.target_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        self.target_entry = ctk.CTkEntry(gen_tab, placeholder_text="http://example.com")
        self.target_entry.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="ew")

        # Threads
        self.concurrency_label = ctk.CTkLabel(gen_tab, text="Threads:", anchor="w")
        self.concurrency_label.grid(row=2, column=0, padx=20, pady=(10,0), sticky="w")
        self.concurrency_slider = ctk.CTkSlider(gen_tab, from_=1, to=100, number_of_steps=99)
        self.concurrency_slider.set(10)
        self.concurrency_slider.grid(row=3, column=0, padx=20, pady=(5, 20), sticky="ew")
        
        # Scan Type (Radio Buttons)
        self.type_frame = ctk.CTkFrame(gen_tab)
        self.type_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.scan_type = ctk.StringVar(value="directory")
        types = [
            ("Directory Scan", "directory"),
            ("SQL Injection", "sqli"),
            ("XSS Scan", "xss"),
            ("LFI Scan", "lfi"),
            ("Command Injection", "cmd")
        ]
        
        for i, (text, val) in enumerate(types):
            rb = ctk.CTkRadioButton(self.type_frame, text=text, variable=self.scan_type, value=val)
            rb.grid(row=0, column=i, padx=10, pady=10)

        # --- Advanced Tab ---
        adv_tab = self.tabview.tab("Advanced")
        adv_tab.grid_columnconfigure(0, weight=1)
        
        # HTTP Method
        self.method_label = ctk.CTkLabel(adv_tab, text="HTTP Method:", anchor="w")
        self.method_label.grid(row=0, column=0, padx=20, pady=(20,0), sticky="w")
        self.method_entry = ctk.CTkOptionMenu(adv_tab, values=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
        self.method_entry.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="w")
        
        # Proxy
        self.proxy_label = ctk.CTkLabel(adv_tab, text="Proxy (e.g. http://127.0.0.1:8080):", anchor="w")
        self.proxy_label.grid(row=2, column=0, padx=20, pady=(10,0), sticky="w")
        self.proxy_entry = ctk.CTkEntry(adv_tab, placeholder_text="http://127.0.0.1:8080")
        self.proxy_entry.grid(row=3, column=0, padx=20, pady=(5, 20), sticky="ew")
        
        # User-Agent Presets
        self.ua_label = ctk.CTkLabel(adv_tab, text="User-Agent Preset:", anchor="w")
        self.ua_label.grid(row=4, column=0, padx=20, pady=(10,0), sticky="w")
        
        self.ua_var = ctk.StringVar(value="PeachFuzz Default")
        self.ua_entry = ctk.CTkOptionMenu(adv_tab, values=list(POPULAR_USER_AGENTS.keys()), 
                                         variable=self.ua_var, command=self.update_headers_with_ua)
        self.ua_entry.grid(row=5, column=0, padx=20, pady=(5, 20), sticky="w")

        # Headers
        self.headers_label = ctk.CTkLabel(adv_tab, text="Custom Headers (JSON format or Key:Value per line):", anchor="w")
        self.headers_label.grid(row=6, column=0, padx=20, pady=(10,0), sticky="w")
        self.headers_entry = ctk.CTkTextbox(adv_tab, height=150)
        self.headers_entry.grid(row=7, column=0, padx=20, pady=(5, 20), sticky="nsew")
        self.headers_entry.insert("1.0", '{"User-Agent": "PeachFuzz-V2"}')

        # Control Buttons (Bottom of Dashboard)
        self.btn_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.btn_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(1, weight=1)
        
        self.start_button = ctk.CTkButton(self.btn_frame, text="Start Scan", command=self.start_scan, fg_color="green", height=50)
        self.start_button.grid(row=0, column=0, padx=10, sticky="ew")
        
        self.stop_button = ctk.CTkButton(self.btn_frame, text="Stop", command=self.stop_scan, fg_color="red", state="disabled", height=50)
        self.stop_button.grid(row=0, column=1, padx=10, sticky="ew")

        # -- Results --
        self.results_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(0, weight=1)
        
        # ResultTable
        self.result_table = ResultTable(self.results_frame, headers=["Status", "Method", "URL", "Length", "Info"], command=self.show_details)
        self.result_table.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="nsew")
        
        # Export Bar
        self.export_frame = ctk.CTkFrame(self.results_frame)
        self.export_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.status_label = ctk.CTkLabel(self.export_frame, text="Ready", anchor="w")
        self.status_label.pack(side="left", padx=10)
        
        self.export_btn = ctk.CTkButton(self.export_frame, text="Export Results", command=self.export_results)
        self.export_btn.pack(side="right", padx=10, pady=5)

        # Initial View
        self.show_dashboard()

    def update_headers_with_ua(self, choice):
        ua_string = POPULAR_USER_AGENTS.get(choice, "")
        if not ua_string:
            return
            
        # Get current text
        current_text = self.headers_entry.get("1.0", "end").strip()
        
        # Try to parse as JSON first
        try:
            headers = json.loads(current_text)
            headers["User-Agent"] = ua_string
            new_text = json.dumps(headers, indent=4)
        except:
             # Assume text format Key: Value
             lines = current_text.splitlines()
             new_lines = []
             found = False
             
             # Clean out existing User-Agent
             for line in lines:
                 if line.lower().startswith("user-agent:"):
                     continue
                 if line.strip():
                    new_lines.append(line)
             
             new_lines.append(f"User-Agent: {ua_string}")
             new_text = "\n".join(new_lines)

        self.headers_entry.delete("1.0", "end")
        self.headers_entry.insert("1.0", new_text)

    def show_dashboard(self):
        self.results_frame.grid_forget()
        self.dashboard_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

    def show_results(self):
        self.dashboard_frame.grid_forget()
        self.results_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

    def parse_headers(self, text):
        # Try JSON first
        try:
            return json.loads(text)
        except:
            pass
        
        # Try Line by Line
        headers = {}
        for line in text.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip()] = v.strip()
        return headers

    def log_result_callback(self, result):
        self.scan_results.append(result) # Store full data
        
        formatted = self.reporter.format_for_gui(result)
        
        method = result.get("method", "GET")
        
        row_values = [
            formatted[0], # Status
            method,
            formatted[1], # URL
            formatted[2], # Length
            formatted[3]  # Info
        ]
        
        # Log to file
        self.reporter.log_result(result)
        
        # Update GUI
        self.after(0, lambda: self.result_table.add_row(row_values, full_data=result))
        self.after(0, lambda: self.status_label.configure(text=f"Scanned: {len(self.scan_results)}"))

    def show_details(self, data):
        # Create a Toplevel window
        top = ctk.CTkToplevel(self)
        top.title("Request Details")
        top.geometry("600x400")
        
        # Use simple text widget
        text = ctk.CTkTextbox(top)
        text.pack(fill="both", expand=True, padx=10, pady=10)
        
        details = f"""URL: {data.get('url')}
Method: {data.get('method')}
Status: {data.get('status')}
Payload: {data.get('payload')}

--- Response ---
{data.get('response')}
"""
        text.insert("1.0", details)

    def export_results(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json"), ("CSV", "*.csv")])
        if not filename:
            return
            
        success = False
        if filename.endswith(".json"):
            success = export_to_json(self.scan_results, filename)
        elif filename.endswith(".csv"):
            success = export_to_csv(self.scan_results, filename)
             
        if success:
             messagebox.showinfo("Export", "Results exported successfully!")
        else:
             messagebox.showerror("Export", "Failed to export results.")

    def run_fuzzer_async(self, target, concurrency, mode, proxy, headers, method):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        self.fuzzer = Fuzzer(
            target_url=target,
            concurrency=int(concurrency),
            proxy=proxy,
            headers=headers,
            reporter_callback=self.log_result_callback
        )
        
        try:
            if mode == "directory":
                loop.run_until_complete(self.fuzzer.scan_directory(method=method))
            else:
                loop.run_until_complete(self.fuzzer.fuzz_parameters(method=method, vuln_type=mode))
                
            self.after(0, self.on_scan_complete)
        finally:
            loop.close()

    def start_scan(self):
        target = self.target_entry.get()
        if not target:
            return
            
        # Reset results
        self.scan_results = []
        
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(text="Scanning...")
        
        concurrency = self.concurrency_slider.get()
        mode = self.scan_type.get()
        
        # Advanced Params
        method = self.method_entry.get()
        proxy = self.proxy_entry.get()
        if not proxy: proxy = None
        
        headers_text = self.headers_entry.get("1.0", "end")
        headers = self.parse_headers(headers_text)
        
        self.scan_thread = threading.Thread(
            target=self.run_fuzzer_async,
            args=(target, concurrency, mode, proxy, headers, method),
            daemon=True
        )
        self.scan_thread.start()

    def stop_scan(self):
        if self.fuzzer:
            self.fuzzer.stop()
        self.status_label.configure(text="Stopping...")

    def on_scan_complete(self):
        self.status_label.configure(text=f"Scan Complete. Found: {len(self.scan_results)}")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        messagebox.showinfo("PeachFuzz", "Scan Completed!")

def main():
    app = App()
    app.mainloop()
