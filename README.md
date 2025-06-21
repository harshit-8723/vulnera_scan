
---

# VulneraScan

**VulneraScan** is a lightweight web vulnerability scanning tool that helps users perform basic reconnaissance and identify common security issues like **SQL Injection** and **Cross-Site Scripting (XSS)**. It integrates with **Google Gemini AI** to generate markdown-formatted security summaries based on scan results.

---

## What It Does

VulneraScan checks for:

- Basic **reconnaissance** data (WHOIS, DNS, headers)
- **SQL injection** vulnerabilities by testing simple payloads
- **XSS vulnerabilities** using reflected payload detection
- AI-generated **summary reports** in Markdown format using Google Gemini API

---

## Tech Stack

### Backend

- **Python** (FastAPI)
- **Google Gemini API** for AI summarization

### Frontend

- **React (Vite)**
- **Chakra UI**
- **Appwrite** (for authentication only)

---

## Features

- Reconnaissance data collection (WHOIS, DNS, headers)
- SQLi testing with basic payloads
- XSS reflected input testing
- AI-generated security summary reports (`.md` format)
- Downloadable summary file
- Clean UI with Chakra UI
- No database dependency
- Appwrite authentication (optional)

---

## Getting Started

> This project is currently running **locally**.

###  Backend

```bash
cd backend
pip install -r requirements.txt
python run.py
```


### Frontend

```bash
cd frontend
npm install
npm run dev
```

> Configure your `.env` file based on `.env.sample` inside the `backend/` and `frontend/` directory.

---

## License

This project is open-source and available under the **MIT License**.

---

## Notes

* Target testing site: [testphp.vulnweb.com](http://testphp.vulnweb.com/)
* No database is used in this version
* AI summary uses Google Gemini API — ensure your API key is set in `.env`

---