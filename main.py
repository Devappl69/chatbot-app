import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from groq import Groq
import json
import time
import ast

groq_client = Groq()

# Basic App Setup
app = ctk.CTk()
app.title("Chatbot App")
app.wm_title("Chatbot App")
photo = ImageTk.PhotoImage(Image.open('assets/logo.png'))
bitmap = ImageTk.PhotoImage(Image.open('assets/logo.ico'))
app.wm_iconphoto(False, photo) # type: ignore
app.wm_iconbitmap(bitmap)
app.tkraise()
app.focus_force()

# Custom Fonts
side_font = ("Arial",14)
prompt_font = ("Arial",18)
send_font = ("Arial",18,"bold")
history_font = ("Arial",18,"underline")
message_font = ("Arial",16)

# Window Setup
app.state("zoomed")
app.geometry("+0+0")
app.minsize(width=720, height=480)
app.resizable(width=True, height=True)

# Grid Setup
app.grid_columnconfigure(0, weight=0)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(1, weight=1)

# Functions
def ask_assistant(prompt: str):
    global current_messages
    try:
        completion = groq_client.chat.completions.create(
            model="compound-beta-mini",     # default model: meta-llama/llama-4-scout-17b-16e-instruct # qwen/qwen3-32b # deepseek-r1-distill-llama-70b
            messages=current_messages + [{"role": "user", "content": prompt}], # type: ignore
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            stream=False,
            stop=None,
        ) # type: ignore
        response = completion.choices[0].message.content
        current_messages.append({"role": "user", "content": prompt})
        current_messages.append({"role": "assistant", "content": response})
        return response, False
    except Exception as e:
        print(f"Encountered error: {e}")
        return f"Error: {e}", True

def send_message() -> None:
    global messages
    text = prompt_entry.get("0.0", "end").strip()
    if len(text)==0: 
        prompt_entry.delete("0.0", "end")
        return
    visible_messages.append(UserMessage(text=text, row=len(visible_messages)))
    prompt_entry.delete("0.0", "end")
    app.after(10) # type: ignore # needs to wait at least 10 ms so the user message can be shown before the ai request freezes the gui
    response, error = ask_assistant(prompt=text)
    visible_messages.append(BotMessage(text=response, row=len(visible_messages), error=error))
    chat_frame._parent_canvas.yview_moveto(1.0)
    
    print("\nMESSAGE HISTORY UPDATED:")
    for message in current_messages:
        print(message)
    print()

# Preset Classes
class ChatButton(ctk.CTkButton):
    def __init__(self, text="placeholder", row=0):
        super().__init__(master=side_frame, width=200, font=side_font, fg_color="transparent", hover_color="#444444", anchor="w", text=text)
        self.grid(row=row, column=0, sticky="ew", padx=5, pady=5)

class BotMessage(ctk.CTkTextbox):
    def __init__(self, text="PLACEHOLDER BOT MESSAGE", row=0, error=False):
        if error:
            super().__init__(master=chat_frame, wrap="word", fg_color="#C00000", corner_radius=25, bg_color="#181818", width=1000, font=message_font)
        else:
            super().__init__(master=chat_frame, wrap="word", fg_color="#202021", corner_radius=25, bg_color="#181818", width=1000, font=message_font)
        self.insert("0.0", text)
        self.configure(state="disabled")
        self.grid(row=row, column=0, sticky="w", padx=15, pady=15)

class UserMessage(ctk.CTkTextbox):
    def __init__(self, text="PLACEHOLDER BOT MESSAGE", row=0):
        super().__init__(master=chat_frame, wrap="word", fg_color="#2f2e2e", corner_radius=25, bg_color="#181818", width=1000, font=message_font)
        self.insert("0.0", text)
        self.configure(state="disabled")
        self.grid(row=row, column=0, sticky="e", padx=15, pady=15)


# Frames Setup
top_frame = ctk.CTkFrame(master=app, border_width=2, corner_radius=5, height=50)
top_frame.grid(row=0, column=0, columnspan=2, sticky="new", padx=10, pady=10)
side_frame = ctk.CTkScrollableFrame(master=app, border_width=2, corner_radius=5, width=200)
side_frame.grid(row=1, column=0, sticky="nsw", padx=10, pady=(0, 10))
main_frame = ctk.CTkFrame(master=app, border_width=2, corner_radius=5)
main_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 10), pady=(0, 10))
chat_frame = ctk.CTkScrollableFrame(master=main_frame, height=10000, width=10000, fg_color="transparent", border_width=2, bg_color="#181818")
chat_frame.pack()
input_frame = ctk.CTkFrame(master=main_frame, fg_color="transparent", bg_color="transparent")
input_frame.place(relx=0.5, rely=1.0, anchor="s", y=-35)

input_frame.grid_columnconfigure(0, weight=1)
prompt_entry = ctk.CTkTextbox(master=input_frame, wrap="word", font=prompt_font, width=1000, height=150, corner_radius=10, state="normal", border_width=1, bg_color="transparent")
prompt_entry.grid(row=0, column=0, padx=(0,3), sticky="nw")
prompt_button = ctk.CTkButton(master=input_frame, text="Send", font=send_font,width=10, height=50, corner_radius=100, bg_color="transparent", fg_color="white", hover_color="#CCCCCC", text_color="black", command=send_message)
prompt_button.grid(row=0, column=1, sticky="e", padx=(10,10))

chat_frame.grid_columnconfigure(0, weight=1)

input_spacer = ctk.CTkFrame(master=chat_frame, height=0, width=0)
input_spacer.grid(row=999, column=0, pady=(200,0)) # Spacer to add space at the bottom to scroll further and reveal all messages

history_label = ctk.CTkLabel(master=side_frame, text="Chat History", font=history_font)
history_label.grid(row=0, column=0)


# Demo Widgets
visible_messages = []
current_messages = [{"role": "system", "content": "You are a helpful assistant."}]
buttons = []
for i in range(50):
    button = ChatButton(text=f"placeholder {i}...", row=i+1)
    buttons.append(button)


chat_frame._parent_canvas.yview_scroll(1000, "units") # Autoscroll to bottom (doesn't work with the spacer)

app.mainloop()
