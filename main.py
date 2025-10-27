import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from encryption import AESEncryption
from database import ChatDatabase

class SafeSpaceChat:
    def __init__(self, root):
        self.root = root
        self.root.title("SafeSpace - Encrypted Chat")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        
        
        self.encryption = AESEncryption()
        self.database = ChatDatabase()
        
        self.setup_ui()
        self.load_message_history()
    
    def setup_ui(self):
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        
        title_label = ttk.Label(main_frame, text="🔒 SafeSpace - Encrypted Chat", 
                               font=('Arial', 16, 'bold'), foreground='#3498db')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        
        self.chat_display = scrolledtext.ScrolledText(
            main_frame, 
            width=70, 
            height=20, 
            state='disabled',
            bg='#ecf0f1',
            font=('Arial', 10)
        )
        self.chat_display.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        
        ttk.Label(input_frame, text="Your message:").grid(row=0, column=0, sticky=tk.W)
        self.message_entry = ttk.Entry(input_frame, width=50, font=('Arial', 12))
        self.message_entry.grid(row=1, column=0, padx=(0, 10), sticky=(tk.W, tk.E))
        self.message_entry.bind('<Return>', lambda e: self.send_message())
        
        
        self.send_button = ttk.Button(input_frame, text="Send Encrypted", 
                                     command=self.send_message)
        self.send_button.grid(row=1, column=1)
        
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        input_frame.columnconfigure(0, weight=1)
    
    def send_message(self):
        message = self.message_entry.get().strip()
        if not message:
            return
        
        try:
            
            encrypted_message = self.encryption.encrypt_message(message)
            
            
            self.database.save_message("You", encrypted_message)
            
            
            self.display_message("You", message, encrypted_message)
            
            
            self.message_entry.delete(0, tk.END)
            
            
            self.root.after(2000, self.simulate_response)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {str(e)}")
    
    def simulate_response(self):
        """Simulate receiving an encrypted response (for demo purposes)"""
        responses = [
            "Hello! This is an encrypted response.",
            "How are you doing today?",
            "This message is securely encrypted!",
            "Nice to chat with you securely!"
        ]
        import random
        response = random.choice(responses)
        
        encrypted_response = self.encryption.encrypt_message(response)
        self.database.save_message("Friend", encrypted_response)
        self.display_message("Friend", response, encrypted_response)
    
    def display_message(self, sender, decrypted_msg, encrypted_msg):
        self.chat_display.config(state='normal')
        
        
        if sender == "You":
            self.chat_display.insert(tk.END, f"🔷 You: {decrypted_msg}\n", 'you')
        else:
            self.chat_display.insert(tk.END, f"🔶 {sender}: {decrypted_msg}\n", 'friend')
        
        self.chat_display.insert(tk.END, f"   🔐 Encrypted: {encrypted_msg[:50]}...\n\n", 'encrypted')
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
        self.chat_display.tag_config('you', foreground='#2980b9')
        self.chat_display.tag_config('friend', foreground='#27ae60')
        self.chat_display.tag_config('encrypted', foreground='#7f8c8d', font=('Arial', 8))
    
    def load_message_history(self):
        history = self.database.get_message_history()
        for sender, encrypted_msg, timestamp in reversed(history):
            try:
                decrypted_msg = self.encryption.decrypt_message(encrypted_msg)
                if not decrypted_msg.startswith("Decryption error"):
                    self.display_message(sender, decrypted_msg, encrypted_msg)
            except:
                pass  

def main():
    root = tk.Tk()
    app = SafeSpaceChat(root)
    root.mainloop()

if __name__ == "__main__":
    main()