# 🧩 Break the Query

**Break the Query** is an interactive SQL-based programming challenge platform designed for technical competitions and hackathons.

The application consists of a **Python/Tkinter desktop client** and a **FastAPI backend server** that records participant activity and performance while they solve SQL challenges.

---

## 📌 Overview

The platform was developed to support a SQL-based technical event, providing participants with an interactive environment to solve queries while allowing the system to track their progress and responses.

The application records relevant information such as:

- Participant name
- Computer/PC number
- Question number
- Time spent on each question
- Submitted responses
- Text entered while attempting questions

This information is communicated between the client application and the backend server for tracking and analysis.

---

## ✨ Features

- 🖥️ Interactive desktop interface built with **Tkinter**
- 🐍 Python-based application
- ⚡ FastAPI backend server
- ⏱️ Tracks time spent on individual questions
- 📝 Tracks participant responses and typed input
- 📊 Records question-level participant activity
- 🔄 Client-server communication through HTTP requests
- 📁 JSON-based question and answer storage
- 🧩 Designed for use in SQL-based technical competitions

---

## 🏗️ System Architecture

The project follows a simple client-server architecture:

```text
┌─────────────────────────┐
│      Participant        │
│      Tkinter Client     │
└────────────┬────────────┘
             │
             │ HTTP Requests
             ▼
┌─────────────────────────┐
│      FastAPI Server     │
│                         │
│  • Receives responses   │
│  • Tracks activity      │
│  • Records results      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│      Data Storage       │
│                         │
│  Questions / Responses  │
│       JSON Data         │
└─────────────────────────┘
```

---

## 🛠️ Technologies Used

- **Python**
- **Tkinter**
- **FastAPI**
- **HTTP / REST-style communication**
- **JSON**
- **Client-Server Architecture**

---

## 📂 Project Structure

```text
breakthequery/
│
├── App/                   # Participant-side desktop application
├── Server/                # FastAPI backend server
├── Guide/                 # Project/event guidance and documentation
├── data/                  # Project data
│
├── checkdb.py             # Database/data checking utility
├── questions.json         # SQL questions and model answers
├── ipaddress.txt          # Network configuration
├── requirements.txt       # Python dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have:

- Python 3.x
- pip

### 1. Clone the repository

```bash
git clone https://github.com/samiyak14/breakthequery.git
cd breakthequery
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the server

Navigate to the server directory and start the FastAPI application according to the project configuration.

```bash
cd Server
```

The server can then be started using the appropriate FastAPI/Uvicorn command configured for the project.

### 4. Start the client

Run the Tkinter application from the `App` directory on the participant machine.

The client communicates with the FastAPI server to submit and track participant activity.

---

## 📊 Activity Tracking

One of the main features of the platform is its ability to track participant interaction with the SQL challenges.

For each question, the system can record information including:

| Data | Purpose |
|---|---|
| Participant Name | Identifies the participant |
| PC Number | Identifies the participant machine |
| Question Number | Identifies the challenge |
| Time Spent | Measures time taken per question |
| Submitted Answer | Records the participant's response |
| Typed Input | Tracks the participant's entered text |

This allows organizers to collect more detailed information about how participants interact with the challenges rather than simply recording the final score.

---

## 🎯 Project Goals

The project was designed to:

- Provide an interactive platform for SQL-based competitions.
- Simplify the management of technical challenges.
- Track participant performance and interaction.
- Create a foundation for analysing question-level performance.
- Demonstrate practical implementation of client-server communication.

---

## 🔮 Future Improvements

Potential improvements include:

- Syntax highlighting for SQL queries
- SQL autocomplete
- Difficulty levels for questions
- Cloud deployment of the backend
- Leaderboards and rankings
- Improved UI/UX
- More robust request handling
- Improved data storage and database integration

---

## 📚 Key Learning Outcomes

This project provided practical experience with:

- Building desktop applications using Python and Tkinter
- Developing backend APIs with FastAPI
- Designing client-server communication
- Tracking and processing user activity
- Structuring a multi-component software project
- Building software for a real technical event

---

## 👩‍💻 Author

**Samiya Budye**

Computer Science Engineering — Artificial Intelligence & Machine Learning

[GitHub](https://github.com/samiyak14)
