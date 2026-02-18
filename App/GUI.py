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
import json

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
backup_file = os.path.join(application_path, "backup_log.json")

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
answers = [""]*len(questions)  # store user's answers locally

# ----------- Backup function -----------
def save_backup(data):
    try:
        if os.path.exists(backup_file):
            with open(backup_file, "r") as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(data)
        with open(backup_file, "w") as f:
            json.dump(logs, f, indent=2)
    except:
        pass  # fail silently

# ----------- Window -----------
class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Break The Query!")
        self.geometry("700x650")
        self.resizable(True, True)
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
        title_label = ctk.CTkLabel(self, image=PhotoImage(file=title_path), text="")
        title_label.pack(pady=(50,20))
        description_label = ctk.CTkLabel(
            self,
            text="Welcome to the SQL Challenge!\nAre you ready to break the query?",
            font=ctk.CTkFont(size=18),
            justify="center"
        )
        description_label.pack(pady=20)
        ctk.CTkButton(self, text="START CHALLENGE", width=220, height=50,
                      font=ctk.CTkFont(size=16, weight="bold"),
                      corner_radius=12,
                      hover_color="#2ECC71",
                      command=lambda: master.show_frame(DetailsPage)).pack(pady=30)

# ----------- Details Frame -----------
class DetailsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        title_label = ctk.CTkLabel(self, text="Enter Your Details", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(40, 20))

        form = ctk.CTkFrame(self, corner_radius=15, fg_color="#2b2b2b", width=350)
        form.pack(pady=20)

        ctk.CTkLabel(form, text="Name:", anchor="w").pack(padx=20, pady=(20, 5), fill="x")
        name_input = ctk.CTkEntry(form)
        name_input.pack(padx=20, pady=(0, 10), fill="x")

        ctk.CTkLabel(form, text="PC No.:", anchor="w").pack(padx=20, pady=(10, 5), fill="x")
        pc_no_input = ctk.CTkEntry(form)
        pc_no_input.pack(padx=20, pady=(0, 20), fill="x")

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
        ctk.CTkLabel(self, text="Do You Want To Start The Game?", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(40, 20))

        rules_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#2b2b2b", width=600)
        rules_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Rules text
        ctk.CTkLabel(rules_frame, text="📌 RULES OF THE CHALLENGE", font=ctk.CTkFont(size=16, weight="bold", underline=True)).pack(pady=(20,10))

        ctk.CTkLabel(rules_frame, text="1. You MUST click the 'TRY' button for every question to submit your answer.", font=ctk.CTkFont(size=14), anchor="w", justify="left").pack(padx=20, pady=(0,10), fill="x")
        ctk.CTkLabel(rules_frame, text="2. You can go back to previous questions and update your answers,", font=ctk.CTkFont(size=14), anchor="w", justify="left").pack(padx=20, pady=(0,0), fill="x")
        ctk.CTkLabel(rules_frame, text="but don't forget to click 'TRY' again to register the new answer.", font=ctk.CTkFont(size=14, weight="bold"), text_color="#E74C3C", anchor="w", justify="left").pack(padx=40, pady=(0,10), fill="x")
        ctk.CTkLabel(rules_frame, text="3. Winner selection:", font=ctk.CTkFont(size=14, weight="bold"), anchor="w", justify="left").pack(padx=20, pady=(0,0), fill="x")
        ctk.CTkLabel(rules_frame, text="- The player with the most correct answers wins.", font=ctk.CTkFont(size=14), anchor="w", justify="left").pack(padx=40, fill="x")
        ctk.CTkLabel(rules_frame, text="- If there is a tie, the player with the least total time taken wins.", font=ctk.CTkFont(size=14), anchor="w", justify="left").pack(padx=40, pady=(0,10), fill="x")

        # Emphasis note
        ctk.CTkLabel(rules_frame, text="⚠️ Emphasis:", font=ctk.CTkFont(size=14, weight="bold", underline=True), anchor="w", justify="left").pack(padx=20, pady=(10,0), fill="x")
        ctk.CTkLabel(rules_frame, text="Clicking 'TRY' is mandatory for your answer to count!", font=ctk.CTkFont(size=14, weight="bold"), text_color="#E74C3C", anchor="w", justify="left").pack(padx=40, pady=(0,20), fill="x")

        ctk.CTkButton(self, text="START GAME", width=220, height=50,
                      font=ctk.CTkFont(size=16, weight="bold"),
                      corner_radius=12,
                      hover_color="#2ECC71",
                      command=lambda: start_game(master)).pack(pady=20)

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

        self.qno_var = ctk.StringVar()
        self.question_var = ctk.StringVar()
        self.status_var = ctk.StringVar()

        self.q_label = ctk.CTkLabel(self, textvariable=self.qno_var, font=ctk.CTkFont(size=16, weight="bold"))
        self.q_label.pack(pady=(20,5))
        self.question_label = ctk.CTkLabel(self, textvariable=self.question_var, font=ctk.CTkFont(size=16), wraplength=620, justify="left")
        self.question_label.pack(pady=5)

        # Answer box with placeholder
        self.query_entry = ctk.CTkTextbox(self, width=600, height=180, wrap=WORD)
        self.query_entry.pack(pady=20)
        self.placeholder_text = "Enter your query here..."
        self.query_entry.insert("1.0", self.placeholder_text)
        self.query_entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.query_entry.bind("<FocusOut>", lambda e: self.restore_placeholder())
        self.query_entry.bind("<Key>", lambda e: self.clear_placeholder())

        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, font=ctk.CTkFont(size=14), text_color="white")
        self.status_label.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self, width=500, progress_color="#2ECC71")
        self.progress.pack(pady=10)

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

    # Placeholder handling
    def clear_placeholder(self):
        current_text = self.query_entry.get("1.0", "end-1c")
        if current_text == self.placeholder_text:
            self.query_entry.delete("1.0", END)

    def restore_placeholder(self):
        current_text = self.query_entry.get("1.0", "end-1c").strip()
        if current_text == "":
            self.query_entry.insert("1.0", self.placeholder_text)

    def show_question(self, index):
        global questions, last_time, answers
        self.q_index = index
        self.question_var.set(questions[index]['question'])
        self.qno_var.set(f"Question {index+1} of {len(questions)}")

        # Show previous answer if exists
        self.query_entry.delete('1.0', END)
        self.query_entry.insert('1.0', answers[index] if answers[index] else self.placeholder_text)
        self.status_var.set("")
        self.status_label.configure(text_color="white")
        self.progress.set(self.q_index / len(questions))
        last_time = datetime.now()
        self.next_btn.configure(text="SUBMIT" if self.q_index == len(questions)-1 else "NEXT")

    def check_query_(self):
        global questions, name, pc_no, time_taken, last_time, answers
        user_input = self.query_entry.get('1.0', END).strip()
        if user_input == self.placeholder_text:
            user_input = ""
        answers[self.q_index] = user_input  # save current input
        forbidden = [r"\bDELETE\b", r"\bDROP\b", r"\bTRUNCATE\b", r"\bALTER\b", r"\bUPDATE\b"]
        if any(re.search(pat, user_input, re.IGNORECASE) for pat in forbidden):
            messagebox.showerror("Error", "Forbidden query")
            return

        now = datetime.now()
        time_taken[self.q_index] += (now - last_time).total_seconds()
        last_time = now

        result = check_query(questions[self.q_index], user_input)
        self.status_var.set(result['response'])
        self.status_label.configure(text_color="green" if result['match'] else "red")

        data = {
            "name": name,
            "pc_number": pc_no,
            "question_number": self.q_index + 1,
            "time_taken": time_taken[self.q_index],
            "correct": result['match']
        }

        # Backup locally
        save_backup(data)

        # Send to server in background
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
