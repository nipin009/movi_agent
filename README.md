# 🚍 MoviSync Admin – AI-Powered Transport Management Dashboard

A full-stack application built with **React**, **FastAPI**, **LangGraph**, and **SQLite**, featuring an intelligent AI assistant capable of answering transport-related queries, generating SQL dynamically, and safely modifying the database.

---

## ✔️ Features

### 🖥️ Frontend (React + Vite)
- Clean UI with pages: **Bus Dashboard** & **Manage Routes**
- Floating Movi Assistant chat widget
- Axios integration with backend API
- Real-time dashboard values

### 🤖 Movi Assistant (LangGraph + GPT-4o)
- Tool calling for DB queries (read & write)
- SQL generation fallback for complex questions
- SQL execution through SQLAlchemy
- Confirmation flow for DB-modifying actions
- Natural-language summarization of SQL results
- Short-term memory for better accuracy

### 🗄️ Backend (FastAPI)
- Endpoints for: `/trips`, `/routes`, `/stops`, `/ask-movi`
- Clean message-based agent invocation
- CORS enabled for React environment

### 💾 SQLite Database
- Tables: Stops, Paths, Routes, Trips, Vehicles, Drivers, Deployments
- Pre-populated via `populate_db.py`

---

## 📌 Table of Contents

- [Features](#️-features)
- [Project Architecture](#project-architecture)
- [Setup & Installation](#setup--installation)
- [Database Schema](#database-schema)
- [Frontend (React UI)](#frontend-react-ui)
- [Backend (FastAPI)](#backend-fastapi)
- [AI Agent Architecture](#ai-agent-architecture)
  - [Basic Graph Agent](#1-basic-graph-agent)
  - [Advanced Graph Agent](#2-advanced-graph-agent)
- [Tools & Capabilities](#tools--capabilities)
- [Screenshots](#screenshots)

---

# 🏗️ Project Architecture

React Frontend (Vite)
↓
FastAPI Backend (Python)
↓
LangGraph Agent (State Machine with Tools + SQL Generation)
↓
SQLite Database (SQLAlchemy ORM)


The system supports:
- Natural-language queries from UI  
- Backend routing and agent orchestration  
- Tool calling for known DB operations  
- SQL generation for complex/free-form questions  
- Safe SQL execution with confirmation for write operations  

---

# ⚙️ Setup & Installation

## 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/movisync-admin.git
cd movisync-admin

2️⃣ Backend Setup (FastAPI)
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt

Populate the SQLite Database
python populate_db.py

Run FastAPI
uvicorn api_server:app --reload

3️⃣ Frontend Setup (React)
cd movi_ui
npm install
npm run dev



1️⃣ Basic Graph Agent
__start__
   |
   ↓
 agent ----→ tools
   |
   ↓
 __end__



2️⃣ Advanced Graph Agent (Full System)
                    __start__
                        |
                       agent
                   /     |       \
                  |      |        \
                  |      |         \
           confirm_tool  |        sql_gen
                |        |            |
                |        |         sql_check
                |        |        /         \
                |        |  confirm_sql    sql_exec
                |        |      |              |
                |        |      |           sql_interpret
                |        |      |              |
                ↓        |      ↓              |
            end_cancel   |      tools ----------/
                         |       |
                         |    post_tool
                         |       |
                         \---- end_success
                                 |
                               __end__



🎉 Conclusion

This project demonstrates:

Full-stack production-style architecture

Intelligent agent orchestration with LangGraph

Safe DB operations via LLM
