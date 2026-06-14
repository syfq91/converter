import re
import tkinter as tk
from tkinter import ttk

class UnitConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")
        self.root.geometry("750x300")
        
        # Variables
        self.mm_var = tk.StringVar()
        self.inch_var = tk.StringVar()
        self.feet_var = tk.StringVar()
        
        # Conversion factors
        self.MM_PER_INCH = 25.4
        self.INCH_PER_FOOT = 12
        
        # Create GUI
        self.setup_ui()
        
        # Flag to prevent recursive updates
        self.updating = False
        
        # Trace variables
        self.mm_var.trace_add("write", lambda *args: self.convert("mm"))
        self.inch_var.trace_add("write", lambda *args: self.convert("inch"))
        self.feet_var.trace_add("write", lambda *args: self.convert("feet"))
        
        # Bind Escape key to clear all
        self.root.bind("<Escape>", lambda e: self.clear_all())
    
    def setup_ui(self):
        # Configure larger font
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # MM row
        ttk.Label(main_frame, text="mm:").grid(row=0, column=0, sticky=tk.W, padx=(0, 15), pady=8)
        ttk.Entry(main_frame, textvariable=self.mm_var, width=25, font=("Arial", 12), justify="right").grid(row=0, column=1, pady=8)
        ttk.Button(main_frame, text="Copy", command=lambda: self.copy_value(self.mm_var)).grid(row=0, column=2, padx=5, pady=8)
        
        # Inch row
        ttk.Label(main_frame, text="in:").grid(row=1, column=0, sticky=tk.W, padx=(0, 15), pady=8)
        ttk.Entry(main_frame, textvariable=self.inch_var, width=25, font=("Arial", 12), justify="right").grid(row=1, column=1, pady=8)
        ttk.Button(main_frame, text="Copy", command=lambda: self.copy_value(self.inch_var)).grid(row=1, column=2, padx=5, pady=8)
        
        # Feet row
        ttk.Label(main_frame, text="ft:").grid(row=2, column=0, sticky=tk.W, padx=(0, 15), pady=8)
        ttk.Entry(main_frame, textvariable=self.feet_var, width=25, font=("Arial", 12), justify="right").grid(row=2, column=1, pady=8)
        ttk.Button(main_frame, text="Copy", command=lambda: self.copy_value(self.feet_var)).grid(row=2, column=2, padx=5, pady=8)
        
        # Clear button
        ttk.Button(main_frame, text="Clear", command=self.clear_all).grid(row=3, column=1, pady=15)
    
    def parse_feet_input(self, text):
        if not text:
            return 0
        text = text.strip()
        # Try decimal format first (e.g., 7.23)
        try:
            return float(text)
        except ValueError:
            pass
        # Try feet format with fraction inches (e.g., 7' 3 1/2" or 7' 3/4")
        match = re.match(r"(\d+)['\u2032\u2019]\s*(\d+)?\s*(\d+)/(\d+)[\u201d\u2033\"]?", text)
        if match:
            feet = int(match.group(1))
            whole_inches = int(match.group(2)) if match.group(2) else 0
            numerator = int(match.group(3))
            denominator = int(match.group(4))
            fraction = numerator / denominator
            return feet + (whole_inches + fraction) / self.INCH_PER_FOOT
        # Try feet format with decimal inches (e.g., 7' 3.5" or 7' 3.5)
        match = re.match(r"(\d+)['\u2032\u2019]\s*(\d+\.?\d*)[\u201d\u2033\"]?", text)
        if match:
            feet = int(match.group(1))
            inches = float(match.group(2))
            return feet + inches / self.INCH_PER_FOOT
        # Try feet only (e.g., 7' or 7')
        match = re.match(r"(\d+)['\u2032\u2019][\u201d\u2033\"]?$", text)
        if match:
            return int(match.group(1))
        # Try fraction format without feet (e.g., 3 1/2")
        match = re.match(r"(\d+)\s+(\d+)/(\d+)[\u201d\u2033\"]?", text)
        if match:
            inches = int(match.group(1))
            numerator = int(match.group(2))
            denominator = int(match.group(3))
            fraction = numerator / denominator
            return (inches + fraction) / self.INCH_PER_FOOT
        return 0
    
    def convert(self, source):
        if self.updating:
            return
            
        self.updating = True
        try:
            if source == "mm":
                value = float(self.mm_var.get()) if self.mm_var.get() else 0
                self.inch_var.set(f"{value / self.MM_PER_INCH:.4f}")
                self.feet_var.set(f"{value / (self.MM_PER_INCH * self.INCH_PER_FOOT):.4f}")
            elif source == "inch":
                value = float(self.inch_var.get()) if self.inch_var.get() else 0
                self.mm_var.set(f"{value * self.MM_PER_INCH:.4f}")
                self.feet_var.set(f"{value / self.INCH_PER_FOOT:.4f}")
            elif source == "feet":
                value = self.parse_feet_input(self.feet_var.get())
                self.mm_var.set(f"{value * self.MM_PER_INCH * self.INCH_PER_FOOT:.4f}")
                self.inch_var.set(f"{value * self.INCH_PER_FOOT:.4f}")
        except ValueError:
            pass
        finally:
            self.updating = False
    
    def copy_value(self, var):
        self.root.clipboard_clear()
        self.root.clipboard_append(var.get())
    
    def clear_all(self):
        self.updating = True
        self.mm_var.set("")
        self.inch_var.set("")
        self.feet_var.set("")
        self.updating = False

if __name__ == "__main__":
    root = tk.Tk()
    app = UnitConverter(root)
    root.mainloop()
