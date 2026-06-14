import re
from fractions import Fraction
import tkinter as tk
from tkinter import ttk

# Conversion factors (Module-level constants per PEP 8)
MM_PER_INCH = 25.4
INCH_PER_FOOT = 12

class UnitConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")
        self.root.geometry("750x300")
        # Set a sensible minimum size to prevent the UI from collapsing
        self.root.minsize(600, 250)
        
        # Make the window layout responsive
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Variables
        self.mm_var = tk.StringVar()
        self.inch_var = tk.StringVar()
        self.feet_var = tk.StringVar()
        self.always_on_top_var = tk.BooleanVar(value=False)
        
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
        # Configure larger font in ttk styles
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TCheckbutton", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding=40)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)  # Allow Entry widgets to expand
        
        # MM row
        ttk.Label(main_frame, text="mm:").grid(row=0, column=0, sticky=tk.W, padx=(0, 15), pady=8)
        ttk.Entry(main_frame, textvariable=self.mm_var, width=25, font=("Arial", 12), justify="right").grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8)
        self.mm_copy_btn = ttk.Button(main_frame, text="Copy", command=lambda: self.copy_value(self.mm_var, self.mm_copy_btn))
        self.mm_copy_btn.grid(row=0, column=2, padx=5, pady=8)
        
        # Inch row
        ttk.Label(main_frame, text="in:").grid(row=1, column=0, sticky=tk.W, padx=(0, 15), pady=8)
        ttk.Entry(main_frame, textvariable=self.inch_var, width=25, font=("Arial", 12), justify="right").grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8)
        self.inch_copy_btn = ttk.Button(main_frame, text="Copy", command=lambda: self.copy_value(self.inch_var, self.inch_copy_btn))
        self.inch_copy_btn.grid(row=1, column=2, padx=5, pady=8)
        
        # Feet row
        ttk.Label(main_frame, text="ft:").grid(row=2, column=0, sticky=tk.W, padx=(0, 15), pady=8)
        ttk.Entry(main_frame, textvariable=self.feet_var, width=25, font=("Arial", 12), justify="right").grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8)
        self.feet_copy_btn = ttk.Button(main_frame, text="Copy", command=lambda: self.copy_value(self.feet_var, self.feet_copy_btn))
        self.feet_copy_btn.grid(row=2, column=2, padx=5, pady=8)
        
        # Always on top checkbox
        self.always_on_top_cb = ttk.Checkbutton(
            main_frame,
            text="Always on Top",
            variable=self.always_on_top_var,
            command=self.toggle_always_on_top
        )
        self.always_on_top_cb.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=15)
        
        # Clear button
        ttk.Button(main_frame, text="Clear", command=self.clear_all).grid(row=3, column=2, padx=5, pady=15)
    
    def parse_feet_input(self, text):
        text = text.strip() if text else ""
        if not text:
            return 0.0
            
        # Parse sign (allows parsing negative mixed measurements)
        is_negative = False
        if text.startswith("-"):
            is_negative = True
            text = text[1:].strip()
        elif text.startswith("+"):
            text = text[1:].strip()
            
        if not text:
            return 0.0
            
        value = None
        
        # Try decimal format first (e.g., 7.23)
        try:
            value = float(text)
        except ValueError:
            pass
            
        if value is None:
            # Try feet format with fraction inches (e.g., 7' 3 1/2" or 7' 3/4")
            # Added $ to enforce full-string matching and avoid partial matched conversions
            match = re.match(r"(\d+)['\u2032\u2019]\s*(\d+)?\s*(\d+)/(\d+)[\u201d\u2033\"]?$", text)
            if match:
                feet = int(match.group(1))
                whole_inches = int(match.group(2)) if match.group(2) else 0
                numerator = int(match.group(3))
                denominator = int(match.group(4))
                if denominator != 0:
                    fraction = numerator / denominator
                    value = feet + (whole_inches + fraction) / INCH_PER_FOOT
                    
        if value is None:
            # Try feet format with decimal inches (e.g., 7' 3.5" or 7' 3.5)
            match = re.match(r"(\d+)['\u2032\u2019]\s*(\d+\.?\d*)[\u201d\u2033\"]?$", text)
            if match:
                feet = int(match.group(1))
                inches = float(match.group(2))
                value = feet + inches / INCH_PER_FOOT
                
        if value is None:
            # Try feet only (e.g., 7' or 7')
            match = re.match(r"(\d+)['\u2032\u2019][\u201d\u2033\"]?$", text)
            if match:
                value = float(match.group(1))
                
        if value is None:
            # Try fraction format without feet (e.g., 3 1/2")
            match = re.match(r"(\d+)\s+(\d+)/(\d+)[\u201d\u2033\"]?$", text)
            if match:
                inches = int(match.group(1))
                numerator = int(match.group(2))
                denominator = int(match.group(3))
                if denominator != 0:
                    fraction = numerator / denominator
                    value = (inches + fraction) / INCH_PER_FOOT
                    
        if value is None:
            # Try fraction-only format (e.g., 1/2 or 1/2")
            match = re.match(r"^(\d+)/(\d+)[\u201d\u2033\"]?$", text)
            if match:
                numerator = int(match.group(1))
                denominator = int(match.group(2))
                if denominator != 0:
                    is_inches = any(q in text for q in ('"', '\u201d', '\u2033'))
                    fraction = numerator / denominator
                    if is_inches:
                        value = fraction / INCH_PER_FOOT
                    else:
                        value = fraction
                        
        if value is not None:
            return -value if is_negative else value
        return None
    
    def format_feet_fractional(self, decimal_feet):
        if decimal_feet == 0:
            return "0'"
            
        # Extract sign and format the absolute value, prepending the sign at the end
        prefix = "-" if decimal_feet < 0 else ""
        decimal_feet = abs(decimal_feet)
        
        feet = int(decimal_feet)
        total_inches = (decimal_feet - feet) * 12
        whole_inches = int(total_inches)
        fractional_inches = total_inches - whole_inches
        
        if fractional_inches >= 0.999:
            whole_inches += 1
            fractional_inches = 0
            if whole_inches == 12:
                feet += 1
                whole_inches = 0
                
        if fractional_inches > 0:
            frac = Fraction(fractional_inches).limit_denominator(64)
            if frac.numerator == 0:
                if whole_inches == 0:
                    result = f"{feet}'"
                else:
                    result = f"{feet}' {whole_inches}\""
            else:
                result = f"{feet}' {whole_inches} {frac}\"" if whole_inches else f"{feet}' {frac}\""
        else:
            if whole_inches == 0:
                result = f"{feet}'"
            else:
                result = f"{feet}' {whole_inches}\""
                
        result = prefix + result
        if result == "-0'":
            result = "0'"
        return result

    def is_partial_input(self, text, source):
        # Checks if the input is a valid partial state to prevent clear-on-type jarring UI
        text = text.strip()
        if not text:
            return True
        if source in ("mm", "inch"):
            return text in ("-", "+", ".", "-.", "+.")
        else:
            # For feet/fractions, allowed characters include digits, spaces, quotes, and fraction slash
            allowed_chars = set("0123456789 /'.\"-+ \u2032\u2019\u201d\u2033")
            return set(text).issubset(allowed_chars)

    def convert(self, source):
        if self.updating:
            return
            
        self.updating = True
        try:
            if source == "mm":
                text = self.mm_var.get().strip()
                if not text:
                    self.inch_var.set("")
                    self.feet_var.set("")
                else:
                    try:
                        value = float(text)
                        self.inch_var.set(f"{value / MM_PER_INCH:.4f}")
                        self.feet_var.set(self.format_feet_fractional(value / (MM_PER_INCH * INCH_PER_FOOT)))
                    except ValueError:
                        # Only clear the fields if it's not a valid partial typing state
                        if not self.is_partial_input(text, "mm"):
                            self.inch_var.set("")
                            self.feet_var.set("")
            elif source == "inch":
                text = self.inch_var.get().strip()
                if not text:
                    self.mm_var.set("")
                    self.feet_var.set("")
                else:
                    try:
                        value = float(text)
                        self.mm_var.set(f"{value * MM_PER_INCH:.4f}")
                        self.feet_var.set(self.format_feet_fractional(value / INCH_PER_FOOT))
                    except ValueError:
                        if not self.is_partial_input(text, "inch"):
                            self.mm_var.set("")
                            self.feet_var.set("")
            elif source == "feet":
                text = self.feet_var.get().strip()
                if not text:
                    self.mm_var.set("")
                    self.inch_var.set("")
                else:
                    value = self.parse_feet_input(text)
                    if value is not None:
                        # Prevent updating other fields if the text is a single sign character
                        if text not in ("-", "+"):
                            self.mm_var.set(f"{value * MM_PER_INCH * INCH_PER_FOOT:.4f}")
                            self.inch_var.set(f"{value * INCH_PER_FOOT:.4f}")
                    else:
                        if not self.is_partial_input(text, "feet"):
                            self.mm_var.set("")
                            self.inch_var.set("")
        finally:
            self.updating = False
    
    def copy_value(self, var, button):
        self.root.clipboard_clear()
        self.root.clipboard_append(var.get())
        
        # Interactive UI feedback: temporary button text modification
        original_text = button.cget("text")
        button.config(text="Copied!")
        self.root.after(1000, lambda: button.config(text=original_text))
    
    def clear_all(self):
        self.updating = True
        try:
            self.mm_var.set("")
            self.inch_var.set("")
            self.feet_var.set("")
        finally:
            self.updating = False
        
    def toggle_always_on_top(self):
        self.root.attributes("-topmost", self.always_on_top_var.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = UnitConverter(root)
    root.mainloop()
