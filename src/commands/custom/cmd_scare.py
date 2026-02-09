import sys
import os

# Module: scare
# Description: Scare the wife

def run(args):
    print("\n🚀 Running Custom Command: scare...")
    
    # --- USER CODE START ---
    import tkinter as tk
    from tkinter import messagebox
    
    root = tk.Tk()
    root.withdraw() # Hide main window
    messagebox.showwarning("SYSTEM ERROR", "Critical Warning: Virus Detected!")
    # --- USER CODE END ---
    
    print("\n✅ scare finished.")
