import Tkinter as tk
import tkMessageBox as messagebox
import base64
from Crypto.Cipher import AES, DES, Blowfish
from Crypto.Util.Padding import pad, unpad
import os

# Color theme
BG_COLOR = "#2C3E50"
FG_COLOR = "#ECF0F1"
BUTTON_COLOR = "#E74C3C"
ENTRY_BG = "#34495E"
ENTRY_FG = "#ECF0F1"

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptography Algorithms Demonstration")
        self.root.geometry("600x700")
        self.root.configure(bg=BG_COLOR)

        self.algorithm = tk.StringVar()
        self.algorithm.set("AES")
        self.mode = tk.StringVar()
        self.mode.set("CBC")
        self.iv_entry = None
        
        self.key_sizes = {
            "AES": "16, 24, 32 bytes",
            "DES": "8 bytes",
            "Blowfish": "8-56 bytes"
        }
        self.default_keys = {
            "AES": "thisisasecretkey",
            "DES": "8charKey",
            "Blowfish": "blowfishkey12"
        }
        
        self.create_home()
    
    def create_home(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="Select Encryption Algorithm", font=("Arial", 16), bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)
        
        algorithms = ["AES", "DES", "Blowfish"]
        dropdown = tk.OptionMenu(self.root, self.algorithm, *algorithms, command=self.update_iv)
        dropdown.pack(pady=10)
        
        tk.Button(self.root, text="Continue", font=("Arial", 12), bg=BUTTON_COLOR, fg=FG_COLOR, command=self.create_crypto_ui).pack(pady=10)

    def update_iv(self, selection):
        """Update the IV entry field based on the selected algorithm"""
        if selection == "AES":
            self.iv_entry.delete(0, tk.END)
            self.iv_entry.insert(0, "1234567890123456")  # 16-byte default for AES
        elif selection == "DES":
            self.iv_entry.delete(0, tk.END)
            self.iv_entry.insert(0, "12345678")  # 8-byte default for DES
        elif selection == "Blowfish":
            self.iv_entry.delete(0, tk.END)
            self.iv_entry.insert(0, "12345678")  # 8-byte default for Blowfish

    def create_crypto_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        algo = self.algorithm.get()
        tk.Label(self.root, text="{} Encryption".format(algo), font=("Arial", 16), bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        
        tk.Label(self.root, text="Possible Key Lengths: " + self.key_sizes[algo], font=("Arial", 10), bg=BG_COLOR, fg=FG_COLOR).pack()
        
        tk.Label(self.root, text="Select Block Mode:", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR).pack()
        modes = ["CBC", "ECB"]
        mode_dropdown = tk.OptionMenu(self.root, self.mode, *modes)
        mode_dropdown.pack(pady=5)
        
        tk.Label(self.root, text="Initialization Vector (IV):", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR).pack()
        self.iv_entry = tk.Entry(self.root, font=("Arial", 12), width=40, bg=ENTRY_BG, fg=ENTRY_FG)
        self.iv_entry.pack(pady=5)
        self.update_iv(self.algorithm.get())  # Set default IV based on selected algorithm
        
        tk.Label(self.root, text="Enter Text:", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR).pack()
        self.input_text = tk.Entry(self.root, font=("Arial", 12), width=40, bg=ENTRY_BG, fg=ENTRY_FG)
        self.input_text.pack(pady=5)
        
        tk.Label(self.root, text="Enter Key:", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR).pack()
        self.key_entry = tk.Entry(self.root, font=("Arial", 12), width=40, bg=ENTRY_BG, fg=ENTRY_FG, )
        self.key_entry.insert(0, self.default_keys[algo])
        self.key_entry.pack(pady=5)
        
        self.key_info_label = tk.Label(self.root, text="", font=("Arial", 10), bg=BG_COLOR, fg=FG_COLOR)
        self.key_info_label.pack()
        
        tk.Button(self.root, text="Encrypt", font=("Arial", 12), bg=BUTTON_COLOR, fg=FG_COLOR, command=self.encrypt).pack(pady=10)
        tk.Button(self.root, text="Decrypt", font=("Arial", 12), bg=BUTTON_COLOR, fg=FG_COLOR, command=self.decrypt).pack(pady=5)
        tk.Button(self.root, text="Back", font=("Arial", 12), bg=BUTTON_COLOR, fg=FG_COLOR, command=self.create_home).pack(pady=10)
        
        tk.Label(self.root, text="Encrypted Text:", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR).pack()
        self.encrypted_text = tk.Entry(self.root, font=("Arial", 12), width=100, bg=ENTRY_BG, fg=ENTRY_FG)
        self.encrypted_text.pack(pady=5)
        
        tk.Label(self.root, text="Decrypted Text:", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR).pack()
        self.decrypted_text = tk.Entry(self.root, font=("Arial", 12), width=100, bg=ENTRY_BG, fg=ENTRY_FG)
        self.decrypted_text.pack(pady=5)
    
    def encrypt(self):
        text = self.input_text.get().encode('utf-8')
        key = self.key_entry.get().encode('utf-8')
        iv = self.iv_entry.get().encode('utf-8')
        algo = self.algorithm.get()
        
        key_length = len(key)
        self.key_info_label.config(text="Key Length: {} bytes".format(key_length))
        
        try:
            if algo == "AES":
                cipher = AES.new(key, AES.MODE_CBC, iv)
                encrypted = cipher.encrypt(pad(text, AES.block_size))
            elif algo == "DES":
                cipher = DES.new(key, DES.MODE_CBC, iv)
                encrypted = cipher.encrypt(pad(text, DES.block_size))
            elif algo == "Blowfish":
                cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
                encrypted = cipher.encrypt(pad(text, Blowfish.block_size))
            
            encrypted_b64 = base64.b64encode(iv + encrypted)
            self.encrypted_text.delete(0, tk.END)
            self.encrypted_text.insert(0, encrypted_b64)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def decrypt(self):
        encrypted_b64 = self.encrypted_text.get()
        key = self.key_entry.get().encode('utf-8')
        iv = self.iv_entry.get().encode('utf-8')
        algo = self.algorithm.get()
        
        try:
            encrypted = base64.b64decode(encrypted_b64)
            encrypted = encrypted[len(iv):]
            
            if algo == "AES":
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
            elif algo == "DES":
                cipher = DES.new(key, DES.MODE_CBC, iv)
                decrypted = unpad(cipher.decrypt(encrypted), DES.block_size)
            elif algo == "Blowfish":
                cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
                decrypted = unpad(cipher.decrypt(encrypted), Blowfish.block_size)
            
            self.decrypted_text.delete(0, tk.END)
            self.decrypted_text.insert(0, decrypted)
        except Exception as e:
            messagebox.showerror("Error", "Decryption failed: Incorrect data, key, or padding issue.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
