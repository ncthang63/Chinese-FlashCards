import tkinter as tk
from tkinter import messagebox
import json
import os
import random

DATA_FILE = "flashcards.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chinese Flashcard App 🌙")
        self.data = load_data()
        self.current_index = 0
        self.front_side = True
        self.dark_mode = False

        # === Giao diện mặc định ===
        self.colors = {
            "bg": "#f4f4f4",
            "fg": "#000000",
            "flash_bg": "#FFECB3",
            "flash_fg": "#4E342E",
            "button_bg": "#e0e0e0",
            "entry_bg": "white",
        }

        self.root.configure(bg=self.colors["bg"])

        # ========== FLASHCARD ==========
        self.flashcard_frame = tk.Frame(root, bg=self.colors["flash_bg"], padx=20, pady=20, relief="raised", bd=3)
        self.flashcard_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.hanzi_label = tk.Label(self.flashcard_frame, text="", font=("Helvetica", 48, "bold"),
                                    bg=self.colors["flash_bg"], fg=self.colors["flash_fg"])
        self.hanzi_label.pack(pady=(10, 0))

        self.pinyin_label = tk.Label(self.flashcard_frame, text="", font=("Helvetica", 20),
                                     bg=self.colors["flash_bg"], fg=self.colors["flash_fg"])
        self.pinyin_label.pack()

        self.flashcard_frame.bind("<Button-1>", self.flip_card)
        self.hanzi_label.bind("<Button-1>", self.flip_card)
        self.pinyin_label.bind("<Button-1>", self.flip_card)

        # ========== FORM ==========
        self.form_frame = tk.LabelFrame(root, text="Add New Word", bg=self.colors["bg"],
                                        fg=self.colors["fg"], padx=10, pady=10, font=("Helvetica", 12, "bold"))
        self.form_frame.pack(padx=20, pady=5, fill="x")

        self._create_entry_field("Hanzi", "hanzi")
        self._create_entry_field("Pinyin", "pinyin")
        self._create_entry_field("English", "english")
        self._create_entry_field("Vietnamese", "vietnamese")

        # ========== BUTTONS ==========
        self.button_frame = tk.Frame(root, bg=self.colors["bg"])
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="➕ Add", command=self.add_word, width=12)
        self.add_button.pack(side="left", padx=5)

        self.delete_button = tk.Button(self.button_frame, text="🗑️ Delete", command=self.delete_word, width=12)
        self.delete_button.pack(side="left", padx=5)

        self.next_button = tk.Button(self.button_frame, text="➡️ Next", command=self.show_next, width=12)
        self.next_button.pack(side="left", padx=5)

        # ========== DARK MODE TOGGLE ==========
        self.toggle_button = tk.Button(root, text="🌙 Toggle Dark Mode", command=self.toggle_dark_mode)
        self.toggle_button.pack(pady=5)

        self.update_flashcard()
        self._apply_styles()

    def _create_entry_field(self, label_text, attr_name):
        label = tk.Label(self.form_frame, text=label_text, bg=self.colors["bg"], fg=self.colors["fg"])
        label.pack(fill="x")
        entry = tk.Entry(self.form_frame, bg=self.colors["entry_bg"], fg=self.colors["fg"])
        entry.pack(fill="x", pady=2)
        setattr(self, f"{attr_name}_entry", entry)

    def _apply_styles(self):
        bg = self.colors["bg"]
        fg = self.colors["fg"]
        flash_bg = self.colors["flash_bg"]
        flash_fg = self.colors["flash_fg"]

        self.root.configure(bg=bg)
        self.flashcard_frame.configure(bg=flash_bg)
        self.hanzi_label.configure(bg=flash_bg, fg=flash_fg)
        self.pinyin_label.configure(bg=flash_bg, fg=flash_fg)

        self.form_frame.configure(bg=bg, fg=fg)
        for child in self.form_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(bg=bg, fg=fg)
            elif isinstance(child, tk.Entry):
                child.configure(bg=self.colors["entry_bg"], fg=fg, insertbackground=fg)

        self.button_frame.configure(bg=bg)
        for btn in [self.add_button, self.delete_button, self.next_button, self.toggle_button]:
            btn.configure(bg=self.colors["button_bg"], fg=fg, activebackground="#cccccc")

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.colors = {
                "bg": "#2E2E2E",
                "fg": "#FFFFFF",
                "flash_bg": "#424242",
                "flash_fg": "#FFECB3",
                "button_bg": "#555555",
                "entry_bg": "#616161"
            }
        else:
            self.colors = {
                "bg": "#f4f4f4",
                "fg": "#000000",
                "flash_bg": "#FFECB3",
                "flash_fg": "#4E342E",
                "button_bg": "#e0e0e0",
                "entry_bg": "white"
            }
        self._apply_styles()
        self.update_flashcard()

    def update_flashcard(self):
        if not self.data:
            self.hanzi_label.config(text="No Data", fg="gray")
            self.pinyin_label.config(text="")
            return

        card = self.data[self.current_index]
        if self.front_side:
            self.hanzi_label.config(text=card["hanzi"])
            self.pinyin_label.config(text=card["pinyin"])
        else:
            self.hanzi_label.config(text=card["english"])
            self.pinyin_label.config(text=card["vietnamese"])

    def flip_card(self, event):
        self.front_side = not self.front_side
        self.update_flashcard()

    def add_word(self):
        hanzi = self.hanzi_entry.get().strip()
        pinyin = self.pinyin_entry.get().strip()
        english = self.english_entry.get().strip()
        vietnamese = self.vietnamese_entry.get().strip()

        if not all([hanzi, pinyin, english, vietnamese]):
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
            return

        self.data.append({
            "hanzi": hanzi,
            "pinyin": pinyin,
            "english": english,
            "vietnamese": vietnamese
        })
        save_data(self.data)

        # Clear
        for field in ["hanzi", "pinyin", "english", "vietnamese"]:
            getattr(self, f"{field}_entry").delete(0, tk.END)

        self.current_index = len(self.data) - 1
        self.front_side = True
        self.update_flashcard()

    def delete_word(self):
        if not self.data:
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this word?")
        if confirm:
            self.data.pop(self.current_index)
            self.current_index = max(0, len(self.data) - 1)
            save_data(self.data)
            self.front_side = True
            self.update_flashcard()

    def show_next(self):
        if self.data:
            if len(self.data) > 1:
                next_index = self.current_index
                while next_index == self.current_index:
                    next_index = random.randint(0, len(self.data) - 1)
                self.current_index = next_index
            self.front_side = True
            self.update_flashcard()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x680")
    root.resizable(False, False)
    app = FlashcardApp(root)
    root.mainloop()
