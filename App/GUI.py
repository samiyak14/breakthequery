from tkinter import *
from tkinter import messagebox
from database import get_questions, check_query
import customtkinter as ctk
from datetime import datetime
import os
import sys
import requests
import re

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
        self.geometry("600x600")
        self.resizable(False, False)
        self.frames = {}
        for F in (HomeFrame, DetailsPage, StartPage, QuestionPage, FinalPage):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.show_frame(HomeFrame)

    def show_frame(self, cont):
        self.frames[cont].tkraise()

# ----------- Frames -----------
class HomeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        title_label = ctk.CTkLabel(self, image=PhotoImage(file=title_path), text="")
        title_label.place(relx=0.5, rely=0.2, anchor="center")

        description_label = ctk.CTkLabel(
            self,
            text="Welcome to the SQL challenge! Are you ready to break the query?",
            wraplength=400
        )
        description_label.place(relx=0.15, rely=0.4, relheight=0.2, relwidth=0.7)

        ctk.CTkButton(self, text="START CHALLENGE",
                      command=lambda: master.show_frame(DetailsPage)).place(relx=0.25, rely=0.7, relheight=0.1, relwidth=0.5)

class DetailsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Enter Your Details").place(relx=0.5, rely=0.2, anchor="center")
        form = ctk.CTkFrame(self)
        form.place(relx=0.5, rely=0.4, anchor="center")

        ctk.CTkLabel(form, text="Name:").grid(row=0, column=0)
        ctk.CTkLabel(form, text="PC No.:").grid(row=1, column=0)

        name_input = ctk.CTkEntry(form)
        name_input.grid(row=0, column=1)
        pc_no_input = ctk.CTkEntry(form)
        pc_no_input.grid(row=1, column=1)

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

        ctk.CTkButton(form, text="SUBMIT", command=submit_info).grid(row=2, column=0, columnspan=2, pady=10)

class StartPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Do You Want To Start The Game?").place(relx=0.5, rely=0.2, anchor="center")
        ctk.CTkButton(self, text="START GAME", command=lambda: start_game(master))\
            .place(relx=0.25, rely=0.7, relheight=0.1, relwidth=0.5)

def start_game(master):
    global last_time
    last_time = datetime.now()
    master.show_frame(QuestionPage)

class QuestionPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.q_index = 0

        self.question_var = ctk.StringVar()
        self.qno_var = ctk.StringVar()
        self.status_var = ctk.StringVar()

        self.query_entry = ctk.CTkTextbox(self, wrap=WORD)
        self.query_entry.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.3)

        ctk.CTkLabel(self, textvariable=self.qno_var).place(relx=0.1, rely=0.05, relwidth=0.8)
        ctk.CTkLabel(self, textvariable=self.question_var, wraplength=380).place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.25)
        ctk.CTkLabel(self, textvariable=self.status_var).place(relx=0.1, rely=0.7, relwidth=0.8)

        self.next_button = ctk.CTkButton(self, text="NEXT", command=self.next_question)
        self.next_button.place(relx=0.65, rely=0.85, relwidth=0.2)
        ctk.CTkButton(self, text="TRY", command=self.check_query_).place(relx=0.4, rely=0.85, relwidth=0.2)
        ctk.CTkButton(self, text="PREV", command=self.prev_question).place(relx=0.15, rely=0.85, relwidth=0.2)

        self.show_question(0)

    def show_question(self, index):
        global questions, last_time
        self.q_index = index
        self.question_var.set(questions[index]['question'])
        self.qno_var.set(f"Question: {index+1}")
        self.query_entry.delete('1.0', END)
        self.status_var.set("")
        last_time = datetime.now()
        # Change NEXT button text if last question
        if self.q_index == len(questions)-1:
            self.next_button.configure(text="SUBMIT")
        else:
            self.next_button.configure(text="NEXT")

    def check_query_(self):
        global questions, name, pc_no, time_taken, last_time
        user_input = self.query_entry.get('1.0', END).strip()
        forbidden = [r"\bDELETE\b", r"\bDROP\b", r"\bTRUNCATE\b", r"\bALTER\b", r"\bUPDATE\b"]
        if any(re.search(pat, user_input, re.IGNORECASE) for pat in forbidden):
            messagebox.showerror("Error", "Forbidden query")
            return

        # Add time taken for this question
        now = datetime.now()
        time_taken[self.q_index] += (now - last_time).total_seconds()
        last_time = now

        # Check the query
        result = check_query(questions[self.q_index], user_input)
        self.status_var.set(result['response'])

        # Send to server with correctness
        correct = result['match']  # True/False
        data = {
            "name": name,
            "pc_number": pc_no,
            "question_number": self.q_index,
            "time_taken": time_taken[self.q_index],
            "correct": correct
        }
        try:
            requests.post(url_server, json=data)
        except:
            try:
                requests.post(url_local, json=data)
            except:
                messagebox.showerror("Error", "Cannot submit result")


    def next_question(self):
        if self.q_index + 1 < len(questions):
            self.show_question(self.q_index + 1)
        else:
            # Last question → go to FinalPage
            self.master.show_frame(FinalPage)

    def prev_question(self):
        if self.q_index - 1 >= 0:
            self.show_question(self.q_index - 1)

class FinalPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Congratulations!\nYou completed the game!").place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.6)
        ctk.CTkButton(self, text="OK", command=master.destroy).place(relx=0.4, rely=0.75, relwidth=0.2)

# ----------- Run App -----------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = Window()
    app.mainloop()
