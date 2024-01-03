import tkinter as tk
import os
from tkinter import scrolledtext
from tkinter import font as tkfont
from tkinter import TclError
from tkmacosx import Button
from llama_cpp import Llama


class NoHighlightButton(Button):
    def __init__(self, master=None, **kwargs):
        try:
            Button.__init__(self, master, **kwargs)
            self.config(borderless=1, activebackground=self['bg'], highlightthickness=0)
            self.bind("<FocusIn>", self.remove_focus_highlight)
        except TclError:
            pass 

    def remove_focus_highlight(self, event):
        self.master.focus()


class Model:
    def __init__(self, path, tokens):
        self.llm = Llama(model_path=path)
        self.tokens = tokens
    
    def llm_ask(self, question):
        output = self.llm.create_completion(max_tokens=self.tokens, prompt=question)
        return output['choices'][0]['text']


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LLM Interface")
        self.height = 700
        self.width = 900
        self.root.geometry("900x700")  

        self.path = None
        self.tokens = None

        with open('settings.txt', 'r') as file:
            for line in file:
                key, value = line.strip().split(': ')
                if key == 'path':
                    path = value
                elif key == 'token':
                    tokens = int(value)

        self.model = Model(path, tokens)

        self.noto_sans_font = ("Noto Sans", 14)

        for i in range(10):
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(0, weight=1)  
        self.root.grid_rowconfigure(1, weight=9)  
        self.root.grid_rowconfigure(2, weight=0)  

        self.search_icon = tk.PhotoImage(file="search.png").subsample(2)
        self.send_icon = tk.PhotoImage(file="send.png").subsample(2)

        img_size = 20

        self.send_button = tk.Label(root, image=self.send_icon, bg="#41424E", width=img_size, height=img_size)
        self.send_button.image = self.send_icon
        self.send_button.bind("<Button-1>", lambda event: self.send_message())
        self.send_button.grid(row=2, column=9, padx=0, pady=0, sticky="nsew")

        self.history_font = tkfont.Font(family="Noto Sans", size=17)
        self.chat_history = scrolledtext.ScrolledText(root, width=90, height=20, font=self.history_font, wrap=tk.WORD, bg="#343541", padx=20, pady=10)
        self.chat_history.grid(row=1, column=0, padx=0, pady=0, columnspan=10, sticky="nsew")
        self.chat_history.grid_propagate(False)  

        self.search_frame = tk.Frame(root, bg="#41424E", padx=0, pady=0)  
        self.search_frame.grid(row=0, column=0, columnspan=10, sticky="nsew", padx=0, pady=0)
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_frame.grid_columnconfigure(1, weight=0)
        self.search_frame.grid_rowconfigure(0, weight=1)  

        search_input_font = tkfont.Font(family="Noto Sans", size=14)  

        self.search_input = tk.Entry(self.search_frame, font=search_input_font, bd=0, highlightthickness=0, bg="#41424E", fg="white")
        self.search_input.grid(row=0, column=0, padx=(40, 10), pady=2, sticky="nsew") 

        self.search_button = tk.Label(self.search_frame, image=self.search_icon, width=img_size, height=img_size, bg="#41424E")
        self.search_button.image = self.search_icon
        self.search_button.bind("<Button-1>", lambda event: self.search_message())
        self.search_button.grid(row=0, column=1, padx=(0, 20), pady=0, sticky="nsew")

        self.chat_history.grid(padx=0, pady=0)
        self.load_chat_history()

        self.user_input_frame = tk.Frame(root, bg="#2f2d29") 
        self.user_input_frame.grid(row=2, column=0, columnspan=9, padx=(40, 40), pady=25, sticky="nsew")

        self.settings_icon = tk.PhotoImage(file="settings.png").subsample(2)
        self.settings_button = tk.Label(self.search_frame, image=self.settings_icon, width=img_size, height=img_size, bg="#41424E")
        self.settings_button.image = self.settings_icon
        self.settings_button.bind("<Button-1>", lambda event: self.open_settings_popup())  
        self.settings_button.grid(row=0, column=2, padx=(0, 20), pady=0, sticky="nsew")  

        self.custom_font = tkfont.Font(family="Noto Sans", size=16)
        self.user_input = tk.Entry(self.user_input_frame, font=self.custom_font, bd=0, bg="#41424E", fg="white")
        self.user_input.pack(fill="both", expand=True)

        x = (self.root.winfo_screenwidth() // 2) - (self.width // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.height // 2)

        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

        self.user_input.bind("<Return>", lambda event: self.send_message())
        self.search_input.bind("<Return>", lambda event: self.search_message())

        self.add_response("Hello! How can I help you?")

        self.search_occurrences = []
        self.current_search_index = 0

        self.search_input.config(highlightthickness=0, highlightbackground="#444444")
        self.user_input.config(highlightthickness=0, highlightbackground="#444444")
        self.chat_history.config(highlightthickness=0, highlightbackground="#444444")

    def open_settings_popup(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")

        window_width = 400
        window_height = 150 
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        settings_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        model_label = tk.Label(settings_window, text="Model path:")
        model_label.grid(row=0, column=0, padx=10, pady=5)  
        model_entry = tk.Entry(settings_window, width=30)
        model_entry.grid(row=0, column=1, padx=10, pady=5)  

        max_tokens_label = tk.Label(settings_window, text="Max tokens:")
        max_tokens_label.grid(row=1, column=0, padx=10, pady=5)  
        max_tokens_entry = tk.Entry(settings_window, width=30)
        max_tokens_entry.grid(row=1, column=1, padx=10, pady=5)  

        with open('settings.txt', 'r') as file:
            for line in file:
                key, value = line.strip().split(': ')
                if key == 'path':
                    model_entry.insert(0, value)  
                elif key == 'token':
                    max_tokens_entry.insert(0, value)  

        def save_settings():
            path = model_entry.get()
            tokens = max_tokens_entry.get()

            # Write to settings.txt
            with open('settings.txt', 'w') as settings_file:
                settings_file.write(f"path: {path}\ntoken: {tokens}")

            settings_window.destroy() 

        save_button = tk.Button(settings_window, text="Save", command=save_settings)
        save_button.grid(row=2, columnspan=2, pady=5)  

        settings_window.grab_set() 
        settings_window.focus_force() 

    def send_message(self):
        user_text = self.user_input.get()
        self.add_message("You", user_text)
        self.save_to_history("You", user_text)
        self.user_input.delete(0, tk.END)

        response = self.model.llm_ask(user_text)

        self.add_response(response)
        self.save_to_history("LLM", response)

    def save_to_history(self, sender, message):
        with open('chat_history.txt', 'a') as file:
            if sender == "LLM":
                file.write(f"{sender}:\n{message}\n\n")
            else:
                file.write(f"{sender}: {message}\n")

    def search_message(self):
        search_text = self.search_input.get()
        self.chat_history.tag_remove('search', '1.0', tk.END)
        self.search_occurrences = []
        if search_text:
            pos = '1.0'
            while True:
                pos = self.chat_history.search(search_text, pos, tk.END, count=tk.ALL, nocase=1, regexp=True)
                if not pos:
                    break
                end = f"{pos}+{len(search_text)}c"
                self.search_occurrences.append((pos, end))
                pos = end

            self.highlight_search_occurrence()

    def highlight_search_occurrence(self):
        if self.search_occurrences:
            start, end = self.search_occurrences[self.current_search_index]
            self.chat_history.tag_add('search', start, end)
            self.chat_history.tag_config('search', background='#149520') 
            self.chat_history.see(start)
            self.current_search_index = (self.current_search_index + 1) % len(self.search_occurrences)
            self.root.after(1000, lambda: self.remove_highlight(start, end))

    def remove_highlight(self, start, end):
        self.chat_history.tag_remove('search', start, end)

    def update_highlight_color(self, start, end, alpha):
        color = f'#{int(255 * alpha):02x}{int(255 * alpha):02x}00'
        self.chat_history.tag_config('search', background=color)
        if alpha >= 1:
            self.chat_history.tag_remove('search', start, end)

    def add_initial_greeting(self, response):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"LLM:\n{response}\n")
        self.chat_history.see(tk.END)
        self.chat_history.config(state=tk.DISABLED)

    def add_message(self, sender, message):
        self.chat_history.config(state=tk.NORMAL)
        lines = message.strip().split('\n')

        if sender == "You":
            self.chat_history.insert(tk.END, f"You:\n", "right_align")
            self.chat_history.tag_config("right_align", justify="right")

        for line in lines:
            if line.strip():
                if sender == "You":
                    self.chat_history.insert(tk.END, f"{line}\n", "right_align")
                else:
                    self.chat_history.insert(tk.END, f"{sender}:\n{line}\n")
                    self.chat_history.tag_config("left_align", justify="left")
            else:
                self.chat_history.insert(tk.END, '\n')

        self.chat_history.insert(tk.END, '\n')  
        self.chat_history.see(tk.END)
        self.chat_history.config(state=tk.DISABLED)

    def load_chat_history(self):
        if os.path.exists('chat_history.txt'):
            with open('chat_history.txt', 'r') as file:
                sender = None
                message = ""

                for line in file:
                    if line.startswith("LLM:"):
                        if sender == "You":
                            self.add_message(sender, message)
                            message = ""
                        sender = "LLM"
                        message += line[4:]  
                    elif line.startswith("You:"):
                        if sender == "LLM":
                            self.add_response(message)
                            message = ""
                        sender = "You"
                        message += line[4:]  
                    else:
                        message += line

                if sender == "LLM":
                    self.add_response(message)
                elif sender == "You":
                    self.add_message(sender, message)
        else:
            self.add_response("Hello! How can I help you?")

    def process_message(self, sender, message):
        if sender == "You":
            self.add_message(sender, message)
        elif sender == "LLM":
            self.add_response(message)

    def add_response(self, response):
        self.chat_history.config(state=tk.NORMAL)

        lines = response.strip().split('\n')  

        for index, line in enumerate(lines):
            if line.strip():  
                if index == 0:
                    self.chat_history.insert(tk.END, f"LLM:\n{line}\n", "llm_align")
                else:
                    self.chat_history.insert(tk.END, f"{line}\n", "llm_align")
            else:
                self.chat_history.insert(tk.END, '\n')

        copy_button = NoHighlightButton(self.chat_history, text="Copy", bg="#46485F", fg="#E3E3E3",
                                        command=lambda resp=response: self.copy_message(resp))
        copy_button_window = self.chat_history.window_create(tk.END, window=copy_button)
        self.chat_history.insert(tk.END, '\n')  
        self.chat_history.see(tk.END)
        self.chat_history.config(state=tk.DISABLED)

    def copy_message(self, response):
        self.root.clipboard_clear()
        self.root.clipboard_append(response)
        self.root.update() 


def run_chat_app():
    root = tk.Tk()
    app = ChatApp(root)
    root.iconbitmap('logo.ico')
    root.configure(bg="#41424E")
    root.mainloop()


if __name__ == "__main__":
    run_chat_app()
