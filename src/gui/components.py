import customtkinter as ctk

class ScrollableLabelButtonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = ctk.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        label = ctk.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        self.label_list.append(label)

class ResultTable(ctk.CTkScrollableFrame):
    def __init__(self, master, headers, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.headers = headers
        self.command = command # Callback function(data)
        self.rows = []
        
        self.grid_columnconfigure(0, weight=1)
        
        # Header Row
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        for i, header in enumerate(headers):
            lbl = ctk.CTkLabel(self.header_frame, text=header, font=("Roboto", 12, "bold"))
            lbl.grid(row=0, column=i, padx=5, sticky="ew")
            self.header_frame.grid_columnconfigure(i, weight=1)

    def add_row(self, values, full_data=None):
        row_idx = len(self.rows) + 1
        
        row_frame = ctk.CTkFrame(self, fg_color=("gray85", "gray25"))
        row_frame.grid(row=row_idx, column=0, sticky="ew", padx=5, pady=2)
        
        line_widgets = []
        for i, val in enumerate(values):
            # Truncate long values
            if len(str(val)) > 50:
                 val = str(val)[:47] + "..."
            
            lbl = ctk.CTkLabel(row_frame, text=str(val), anchor="w", cursor="hand2")
            lbl.grid(row=0, column=i, padx=5, pady=2, sticky="ew")
            row_frame.grid_columnconfigure(i, weight=1)
            
            if self.command and full_data:
                lbl.bind("<Button-1>", lambda e, d=full_data: self.command(d))
            
            line_widgets.append(lbl)
            
        self.rows.append(row_frame)
        
        # Limit rows to avoid lag (keep last 200)
        if len(self.rows) > 200:
            old = self.rows.pop(0)
            old.destroy()

class LogConsole(ctk.CTkTextbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(state="disabled", font=("Consolas", 12))

    def log(self, message):
        self.configure(state="normal")
        self.insert("end", message + "\n")
        self.see("end")
        self.configure(state="disabled")
