# BevScan Setup Guide

BevScan is a smart invoice parser for beverage teams, powered by OCR and LLMs. This guide covers all system, Python, and Node.js setup steps for local development on macOS (with Homebrew). For Linux, see notes below.

---

## 1. System Requirements
- macOS (Intel or Apple Silicon)
- Homebrew (https://brew.sh/)
- Python 3.11 (via conda recommended)
- Node.js 18+ (via nvm or brew)
- PostgreSQL

---

## 2. System Dependencies (Homebrew)

Run these commands in your terminal:

```bash
# Core dependencies
brew install tesseract
brew install libtiff
brew install poppler
brew install postgresql
brew install git
brew install ffmpeg  # (optional, for image/video support)

# (Optional) For Python/conda management
brew install --cask anaconda

# (Optional) For Node.js management
brew install nvm
```

---

## 3. Python Environment (Backend)

**Recommended:** Use conda for Python 3.11 and dependency isolation.

```bash
# Create and activate conda environment
conda create -n bevscan python=3.11 -y
conda activate bevscan

# Install Python dependencies
pip install -r backend/requirements.txt
```

---

## 4. Database Setup (PostgreSQL)

```bash
# Start PostgreSQL (if not already running)
brew services start postgresql

# Create database (if not already created)
createdb bevscan
```

---

## 5. Environment Variables

Copy `.env.example` to `.env` in the backend directory and fill in your settings:

```bash
cp backend/.env.example backend/.env
# Edit backend/.env as needed
```

---

## 6. Alembic Migrations (Database Schema)

```bash
# From backend directory
alembic upgrade head
```

---

## 7. Initial Data (Default Vendor)

```bash
# From backend directory
python setup_initial_data.py
```

---

## 8. Frontend Setup (Next.js)

```bash
cd frontend
npm install
npm run dev
```

---

## 9. Backend Setup (FastAPI)

```bash
cd backend
conda activate bevscan
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 10. Testing End-to-End

```bash
cd backend
python test_end_to_end.py
```

---

## 11. Troubleshooting

- **PDF parsing errors:**
  - Ensure `libtiff` and `poppler` are installed (`brew install libtiff poppler`).
  - Restart the backend server after installing system libraries.
- **PostgreSQL errors:**
  - Ensure the service is running: `brew services start postgresql`
  - Ensure your user has permission to create databases.
- **OCR issues:**
  - Ensure `tesseract` is installed and in your PATH.
- **LLM API keys:**
  - Set your Gemini, OpenAI, or other API keys in `.env` as needed.

---

## 12. Linux Notes
- Use `apt-get` or `yum` to install `tesseract-ocr`, `libtiff-dev`, `poppler-utils`, `postgresql`, etc.
- Adjust paths and service commands as needed for your distro.

---

## 13. Useful Commands

```bash
# Start backend (from backend/)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (from frontend/)
npm run dev

# Run Alembic migrations (from backend/)
alembic upgrade head

# Create sample invoice PDF (from backend/)
python create_sample_invoice.py

# Run end-to-end test (from backend/)
python test_end_to_end.py
```

---

## 14. References
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Poppler PDF Tools](https://poppler.freedesktop.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [ReportLab (PDF)](https://www.reportlab.com/)

---

## 15. Support
If you run into issues, check the logs in your terminal and review the troubleshooting section above. For further help, open an issue or contact the maintainer. 
=======
# bevscan
