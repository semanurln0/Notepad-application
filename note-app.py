import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, font, simpledialog
from cryptography.fernet import Fernet


class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python NoteApp")
        self.root.geometry("900x600")
        self.root.config(bg="#f0f0f0")

        # Font options
        self.current_font_family = "Arial"
        self.current_font_size = 12
        self.bold_enabled = False
        self.italic_enabled = False
        self.underline_enabled = False

        # Encryption variables
        self.encryption_key = None
        self.is_locked = False

        # Create the styled toolbar
        self.create_toolbar()

        # Create text editor
        self.text_area = tk.Text(root, wrap="word", font=(self.current_font_family, self.current_font_size),
                                 bg="#ffffff", fg="#333333", relief=tk.FLAT)
        self.text_area.pack(expand=1, fill=tk.BOTH, padx=5, pady=5)

        # Lock symbol when locked
        self.lock_label = tk.Label(root, text="🔒", font=("Arial", 50), bg="black", fg="white")
        self.lock_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.lock_label.lower()

    def create_toolbar(self):
        # Toolbar Frame
        toolbar = tk.Frame(self.root, bg="#333333", pady=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Toolbar Buttons Style
        btn_style = {"bg": "#0078d7", "fg": "white", "relief": tk.FLAT,
                     "activebackground": "#005a9e", "activeforeground": "white"}

        # Bold Button
        bold_btn = tk.Button(toolbar, text="B", command=self.toggle_bold, font=("Arial", 12, "bold"), width=3, **btn_style)
        bold_btn.pack(side=tk.LEFT, padx=2)

        # Italic Button
        italic_btn = tk.Button(toolbar, text="I", command=self.toggle_italic, font=("Arial", 12, "italic"), width=3, **btn_style)
        italic_btn.pack(side=tk.LEFT, padx=2)

        # Underline Button
        underline_btn = tk.Button(toolbar, text="U", command=self.toggle_underline, font=("Arial", 12, "underline"), width=3, **btn_style)
        underline_btn.pack(side=tk.LEFT, padx=2)

        # Font Selector
        font_selector = tk.OptionMenu(toolbar, tk.StringVar(value=self.current_font_family),
                                       "Arial", "Times New Roman", "Verdana", command=self.change_font)
        font_selector.config(bg="#0078d7", fg="white", activebackground="#005a9e", activeforeground="white")
        font_selector["menu"].config(bg="white", fg="black")
        font_selector.pack(side=tk.LEFT, padx=2)

        # Font Size Selector
        font_size_selector = tk.Spinbox(toolbar, from_=8, to=72, width=5, command=self.change_font_size,
                                        bg="#f4f4f4", relief=tk.FLAT)
        font_size_selector.pack(side=tk.LEFT, padx=2)

        # Font Color Button
        font_color_btn = tk.Button(toolbar, text="Font Color", command=self.change_font_color, **btn_style)
        font_color_btn.pack(side=tk.LEFT, padx=2)

        # Background Color Button
        bg_color_btn = tk.Button(toolbar, text="Background Color", command=self.change_bg_color, **btn_style)
        bg_color_btn.pack(side=tk.LEFT, padx=2)

        # Save Button
        save_btn = tk.Button(toolbar, text="Save", command=self.save_file, **btn_style)
        save_btn.pack(side=tk.LEFT, padx=2)

        # Load Button
        load_btn = tk.Button(toolbar, text="Load", command=self.open_file, **btn_style)
        load_btn.pack(side=tk.LEFT, padx=2)

        # Encrypt Button
        encrypt_btn = tk.Button(toolbar, text="Lock", command=self.encrypt_note, **btn_style)
        encrypt_btn.pack(side=tk.LEFT, padx=2)

        # Decrypt Button
        decrypt_btn = tk.Button(toolbar, text="Unlock", command=self.decrypt_note, **btn_style)
        decrypt_btn.pack(side=tk.LEFT, padx=2)

    # File operations
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_area.get(1.0, tk.END).strip()
                file.write(content)

    # Text formatting
    def toggle_bold(self):
        self.bold_enabled = not self.bold_enabled
        self.update_font()

    def toggle_italic(self):
        self.italic_enabled = not self.italic_enabled
        self.update_font()

    def toggle_underline(self):
        self.underline_enabled = not self.underline_enabled
        self.update_font()

    def update_font(self):
        font_style = font.Font(family=self.current_font_family, size=self.current_font_size)
        if self.bold_enabled:
            font_style.configure(weight="bold")
        if self.italic_enabled:
            font_style.configure(slant="italic")
        if self.underline_enabled:
            font_style.configure(underline=True)
        self.text_area.configure(font=font_style)

    def change_font(self, font_name):
        self.current_font_family = font_name
        self.update_font()

    def change_font_size(self):
        size = int(self.text_area.cget("font").split()[-1])
        self.current_font_size = size
        self.update_font()

    def change_font_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.configure(fg=color)

    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.configure(bg=color)

    # Encryption and decryption
    def encrypt_note(self):
        if self.is_locked:
            messagebox.showwarning("Warning", "Note is already locked!")
            return
        password = simpledialog.askstring("Set Password", "Enter a password to lock the note:", show="*")
        if not password:
            return
        content = self.text_area.get(1.0, tk.END).strip()
        self.encryption_key = Fernet.generate_key()
        cipher_suite = Fernet(self.encryption_key)
        encrypted = cipher_suite.encrypt(content.encode()).decode()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, encrypted)
        self.is_locked = True
        self.text_area.config(state=tk.DISABLED, bg="black", fg="black")
        self.lock_label.lift()

    def decrypt_note(self):
        if not self.is_locked:
            messagebox.showinfo("Info", "Note is not locked.")
            return
        password = simpledialog.askstring("Unlock Note", "Enter the password to unlock:", show="*")
        if not password:
            return
        try:
            cipher_suite = Fernet(self.encryption_key)
            encrypted_content = self.text_area.get(1.0, tk.END).strip()
            decrypted = cipher_suite.decrypt(encrypted_content.encode()).decode()
            self.text_area.config(state=tk.NORMAL, bg="#ffffff", fg="#333333")
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, decrypted)
            self.is_locked = False
            self.lock_label.lower()
        except Exception:
            messagebox.showerror("Error", "Invalid password or corrupted data!")


if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
