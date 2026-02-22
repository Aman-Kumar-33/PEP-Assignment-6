# 📘 Ivy Intelligence Hub & Student Competency Network

---

## 🎯 Project Purpose

The **Ivy Intelligence Hub** is a centralized, AI-driven aggregator designed to solve the problem of information fragmentation across elite academic institutions.

By monitoring real-time data feeds from 8 Ivy League universities, the system extracts, classifies, and ranks opportunities — saving students from manual search fatigue.

---

## 🔑 Key Objectives

### 1. Intelligence Aggregation

Automatically crawl and normalize news and research data from institutions like Harvard and Yale.

### 2. AI Domain Classification

Use Natural Language Processing (NLP) to categorize opportunities into domains (e.g., AI, Law, Engineering).

### 3. Competency Benchmarking

Provide an **InCoScore engine** that ranks student achievements (Research, Hackathons) on a global leaderboard.

### 4. Application Assistance

Generate AI-augmented application drafts pre-filled with student competency data.

---

## ⚙️ How the Code Works

The project follows a **Modular Full-Stack Architecture**:

---

### 🖥️ 1. Backend (FastAPI & Python)

#### 📌 Scraper Service (`scraper.py`)

* Uses **BeautifulSoup4** and `requests` to traverse the DOM of university news sites.
* Utilizes a **Base URL Map** to convert relative paths into absolute URLs.
* Prevents common `404` errors during scraping.

#### 🤖 AI Engine (`ai.py`)

* Leverages the **Hugging Face Inference API** (BART model).
* Performs zero-shot text classification.
* Labels headlines automatically without manual tagging.

#### 🗄️ Database ORM (`models.py`)

* Uses **SQLAlchemy**.
* Manages a MySQL database containing:

  * `User`
  * `Opportunity`
  * `Application`

---

### 🎨 2. Frontend (HTML5 / Vanilla JS / CSS3)

#### 🌐 Dynamic Hub (`index.html`)

* Single Page Application (SPA).
* Switches between:

  * Opportunity Feed
  * Leaderboard
  * Profile Settings
* No page reload required.

#### 🏆 InCoScore Engine

```math
InCoScore = (Research × 50) + (Hackathons × 30) + (Internships × 20)
```

---

### 🔄 3. Integration Logic

The **"Sync Intelligence"** button:

1. Sends a `POST` request to the FastAPI backend.
2. Initiates scraping + AI classification pipeline.
3. Updates the MySQL database.
4. Returns a status report to the UI.

---

## 🚀 How to Run the Program

---

### ✅ Prerequisites

* Python 3.10+
* MySQL Server (local or cloud)
* Hugging Face API Token (for AI classification)

---

### 1️⃣ Setup Environment

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/yourusername/ivy-intel-hub.git
cd ivy-intel-hub
python -m venv .venv
```

Activate environment:

**Mac/Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Configuration (`.env`)

Create a `.env` file in the root directory:

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/ivy_db
HF_API_KEY=your_huggingface_token_here
```

---

### 3️⃣ Initialize Database

Ensure MySQL server is running and create the database:

```sql
CREATE DATABASE ivy_db;
```

---

### 4️⃣ Run the Application

Start FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

Open browser and navigate to:

```
http://127.0.0.1:8000
```

---

## 📈 Project Roadmap & Future Scope

### ✅ Phase 1–4

* Core Scraper
* AI Engine
* InCoScore Leaderboard

### 🔄 Phase 5 (Current)

* Application Tracking
* Auto-Fill Assistance

### 🔮 Future Enhancements

* Integration of **OpenCV** for automated document verification
  (e.g., verifying research certificates)
