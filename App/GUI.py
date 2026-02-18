from tkinter import *
from tkinter import messagebox
from database import get_questions, check_query
import customtkinter as ctk
from datetime import datetime
import os
import sys
import requests
import re
import threading

# ----------- Paths -----------
title_img = 'Title.png'
ip_file = 'ipaddress.txt'
port = '8000'

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(__file__)

title_path = os.path.join(application_path, title_img)
ip_file_path = os.path.abspath(os.path.join(application_path, '..', ip_file))

with open(ip_file_path, 'r') as f:
    server_ip = f.read().strip()

url_local = "http://127.0.0.1:8000/log"
url_server = f"http://{server_ip}:{port}/log"

# ----------- Global State -----------
time_taken = [0]*10
last_time = None
name = ""
pc_no = 0

questions = get_questions()

# ----------- Window -----------
class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Break The Query!")
        self.geometry("700x650")
        self.resizable(True,True)
        self.frames = {}
        for F in (HomeFrame, DetailsPage, StartPage, QuestionPage, FinalPage):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.show_frame(HomeFrame)

    def show_frame(self, cont):
        self.frames[cont].tkraise()

# ----------- Home Frame -----------
class HomeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # Title Image
        title_label = ctk.CTkLabel(self, image=PhotoImage(file=title_path), text="")
        title_label.pack(pady=(50,20))

        # Description
        description_label = ctk.CTkLabel(
            self,
            text="Welcome to the SQL Challenge!\nAre you ready to break the query?",
            font=ctk.CTkFont(size=18),
            justify="center"
        )
        description_label.pack(pady=20)

        # Start button
        ctk.CTkButton(self, text="START CHALLENGE", width=220, height=50,
                      font=ctk.CTkFont(size=16, weight="bold"),
                      corner_radius=12,
                      hover_color="#2ECC71",
                      command=lambda: master.show_frame(DetailsPage)).pack(pady=30)

# ----------- Details Frame -----------
class DetailsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Page title
        title_label = ctk.CTkLabel(self, text="Enter Your Details", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(40, 20))

        # Form frame (fixed width, height adapts)
        form = ctk.CTkFrame(self, corner_radius=15, fg_color="#2b2b2b", width=350)
        form.pack(pady=20)
        # form.pack_propagate(False)  <- REMOVE this line

        # Labels and entry fields with padding
        ctk.CTkLabel(form, text="Name:", anchor="w").pack(padx=20, pady=(20, 5), fill="x")
        name_input = ctk.CTkEntry(form)
        name_input.pack(padx=20, pady=(0, 10), fill="x")

        ctk.CTkLabel(form, text="PC No.:", anchor="w").pack(padx=20, pady=(10, 5), fill="x")
        pc_no_input = ctk.CTkEntry(form)
        pc_no_input.pack(padx=20, pady=(0, 20), fill="x")

        # Submit button
        def submit_info():
            global name, pc_no
            player_name = name_input.get().strip()
            try:
                pc_number = int(pc_no_input.get())
                if not (1 <= pc_number <= 20):
                    raise ValueError
            except:
                messagebox.showerror("Error", "Enter a valid PC number (1-20)")
                return
            if not player_name:
                messagebox.showerror("Error", "Enter your name")
                return
            name = player_name
            pc_no = pc_number
            master.show_frame(StartPage)

        ctk.CTkButton(form, text="SUBMIT", command=submit_info).pack(pady=(0, 20), padx=20, fill="x")

# ----------- Start Frame -----------
class StartPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Do You Want To Start The Game?", font=ctk.CTkFont(size=18)).pack(pady=100)
        ctk.CTkButton(self, text="START GAME", width=220, height=50,
                      font=ctk.CTkFont(size=16, weight="bold"),
                      corner_radius=12,
                      hover_color="#2ECC71",
                      command=lambda: start_game(master)).pack(pady=50)

def start_game(master):
    global last_time
    last_time = datetime.now()
    master.show_frame(QuestionPage)

# ----------- Question Frame -----------
class QuestionPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.q_index = 0

        # Question text
        self.qno_var = ctk.StringVar()
        self.question_var = ctk.StringVar()
        self.status_var = ctk.StringVar()
        self.status_color = ctk.StringVar(value="white")

        self.q_label = ctk.CTkLabel(self, textvariable=self.qno_var, font=ctk.CTkFont(size=16, weight="bold"))
        self.q_label.pack(pady=(20,5))
        self.question_label = ctk.CTkLabel(self, textvariable=self.question_var, font=ctk.CTkFont(size=16), wraplength=620, justify="left")
        self.question_label.pack(pady=5)

        # Input box
        self.query_entry = ctk.CTkTextbox(self, width=600, height=180, wrap=WORD)
        self.query_entry.pack(pady=20)

        # Status label
        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, font=ctk.CTkFont(size=14), text_color="white")
        self.status_label.pack(pady=10)

        # Progress bar
        self.progress = ctk.CTkProgressBar(self, width=500, progress_color="#2ECC71")
        self.progress.pack(pady=10)

        # Buttons frame
        btn_frame = ctk.CTkFrame(self, fg_color=None)
        btn_frame.pack(pady=15)

        self.prev_btn = ctk.CTkButton(btn_frame, text="PREV", width=120, height=40, corner_radius=12,
                                      hover_color="#E67E22", command=self.prev_question)
        self.prev_btn.grid(row=0, column=0, padx=10)

        self.try_btn = ctk.CTkButton(btn_frame, text="TRY", width=120, height=40, corner_radius=12,
                                     hover_color="#3498DB", command=self.check_query_)
        self.try_btn.grid(row=0, column=1, padx=10)

        self.next_btn = ctk.CTkButton(btn_frame, text="NEXT", width=120, height=40, corner_radius=12,
                                      hover_color="#2ECC71", command=self.next_question)
        self.next_btn.grid(row=0, column=2, padx=10)

        self.show_question(0)

    def show_question(self, index):
        global questions, last_time
        self.q_index = index
        self.question_var.set(questions[index]['question'])
        self.qno_var.set(f"Question {index+1} of {len(questions)}")
        self.query_entry.delete('1.0', END)
        self.status_var.set("")
        self.status_label.configure(text_color="white")
        self.progress.set(self.q_index / len(questions))
        last_time = datetime.now()
        self.next_btn.configure(text="SUBMIT" if self.q_index == len(questions)-1 else "NEXT")

    def check_query_(self):
        global questions, name, pc_no, time_taken, last_time
        user_input = self.query_entry.get('1.0', END).strip()
        forbidden = [r"\bDELETE\b", r"\bDROP\b", r"\bTRUNCATE\b", r"\bALTER\b", r"\bUPDATE\b"]
        if any(re.search(pat, user_input, re.IGNORECASE) for pat in forbidden):
            messagebox.showerror("Error", "Forbidden query")
            return

        # Calculate time
        now = datetime.now()
        time_taken[self.q_index] += (now - last_time).total_seconds()
        last_time = now

        # Check query
        result = check_query(questions[self.q_index], user_input)
        self.status_var.set(result['response'])
        self.status_label.configure(text_color="green" if result['match'] else "red")

        # Prepare data
        data = {
            "name": name,
            "pc_number": pc_no,
            "question_number": self.q_index + 1,
            "time_taken": time_taken[self.q_index],
            "correct": result['match']
        }

        # Send in background
        def send_to_server(d):
            try:
                requests.post(url_server, json=d, timeout=2)
            except:
                try:
                    requests.post(url_local, json=d, timeout=2)
                except:
                    pass
        threading.Thread(target=send_to_server, args=(data,), daemon=True).start()

    def next_question(self):
        if self.q_index + 1 < len(questions):
            self.show_question(self.q_index + 1)
        else:
            self.master.show_frame(FinalPage)

    def prev_question(self):
        if self.q_index - 1 >= 0:
            self.show_question(self.q_index - 1)

# ----------- Final Page -----------
class FinalPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="🎉 Congratulations!\nYou completed the game!", font=ctk.CTkFont(size=20), justify="center").pack(pady=100)
        ctk.CTkButton(self, text="OK", width=180, height=50, font=ctk.CTkFont(size=16, weight="bold"),
                      corner_radius=12, hover_color="#2ECC71",
                      command=master.destroy).pack(pady=50)

# ----------- Run App -----------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = Window()
    app.mainloop()
