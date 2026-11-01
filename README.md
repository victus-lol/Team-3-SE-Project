# Team-3-SE-Project
 Problem statament -- Task Manager Application  
PES2UG25CS804 -- Balaji Gowda S R  
PES2UG24CS016	-- AARYAN DUBEY  
PES2UG24CS006	-- AADI KORE  
PES2UG24CS041 -- AKASH PAWAR

# Task Manager Application

A modern, robust, layered full-stack task management application developed following Agile methodology.

## Tech Stack
- **Frontend:** React 18, Vite, React Router, Vitest, React Testing Library
- **Backend:** Python 3.12, Flask 3.1, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF
- **Database:** SQLite with strict Foreign Keys and WAL mode
- **Quality & Testing:** Pytest, Ruff, ESLint, Prettier, Playwright E2E

---

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 22 LTS & npm
- Git

### Backend Setup (PowerShell / Windows)
```powershell
cd server
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt

# Run migrations to initialize the database
flask db upgrade

# Run tests
pytest

# Start Flask development server
flask run
```

### Backend Setup (Bash / macOS / Linux)
```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
flask db upgrade
pytest
flask run
```

### Frontend Setup
```bash
cd client
npm install
npm test
npm run dev
```

---

## Project Structure
```
task-manager/
├── .github/          # CI/CD Workflows, templates, CODEOWNERS
├── client/           # React + Vite frontend
├── server/           # Flask backend & Alembic migrations
├── tests/            # Playwright E2E & performance tests
├── scripts/          # Database seeding, reset, and check tools
└── docs/             # Comprehensive architectural & process documentation
```

