# 🎓 Student Marks Predictor — React + FastAPI ML

A full-stack Supervised Machine Learning web application that predicts a student's expected examination marks based on daily study hours using **Ordinary Least Squares (OLS) Linear Regression**.

Engineered with a **FastAPI** Python backend and a modern **React (Vite + Tailwind CSS + Recharts)** frontend.

---

## 📌 1. Project Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                 React Frontend (Port 5173)                  │
│   • Vite • Tailwind CSS (Dark Glassmorphism) • Recharts     │
│   • Slider & Quick Presets (2h, 5h, 8h, 11h) • Score Card   │
└──────────────────────────────▲──────────────────────────────┘
                               │ JSON REST API (fetch/axios)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 FastAPI Backend (Port 8000)                 │
│   • Pydantic Request/Response Models • CORS Middleware      │
│   • Endpoints: /api/predict, /api/metrics, /api/dataset     │
└──────────────────────────────▲──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              scikit-learn Linear Regression                 │
│   • 80% Training Set / 20% Unseen Test Set (Zero Leakage)   │
│   • Metrics: MAE, RMSE, R² Score (~98.9% accuracy)          │
│   • Clamping: Enforces real-world [0, 100%] exam boundaries │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 2. Technology Stack

### Frontend
- **React 19 with Vite:** Ultra-fast reactive single-page frontend.
- **Tailwind CSS v4:** Premium dark-mode palette (`#090d16`), glassmorphism panels, and smooth micro-interactions.
- **Recharts:** Responsive composed charts rendering scatter plots (train vs. test) and the fitted regression line.
- **Lucide React:** Modern icons for cards, metrics, and navigation.
- **Axios:** Centralized API client with timeouts and error handling.

### Backend
- **Python 3.10+ / 3.14:** Core server runtime.
- **FastAPI & Uvicorn:** High-performance asynchronous REST API framework.
- **Pydantic v2:** Input validation and response schema serialization.
- **scikit-learn:** Ordinary Least Squares Linear Regression (`LinearRegression`), `train_test_split`, and metric evaluation.
- **pandas & NumPy:** Data wrangling, array mathematics, and statistical summaries.

---

## 📁 3. Project Directory Structure

```text
project/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI server with CORS & API endpoints
│   │   ├── model.py            # scikit-learn training, evaluation & inference
│   │   ├── schemas.py          # Pydantic request & response validation schemas
│   │   └── data.py             # Dataset loader, validation & descriptive stats
│   ├── data/
│   │   └── student_marks.csv   # Reproducible 40-record student study dataset
│   ├── test_backend.py         # Automated API & ML unit test suite (7 tests)
│   └── requirements.txt        # Backend dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx          # Navigation & live backend connection pill
│   │   │   ├── WelcomeBanner.jsx    # Hero banner with R² & student statistics
│   │   │   ├── StudyHoursForm.jsx   # Slider, 2/5/8/11h presets & predict button
│   │   │   ├── PredictionCard.jsx   # Score display, category badge & study tips
│   │   │   ├── RegressionChart.jsx  # Recharts scatter plot & regression line
│   │   │   ├── MetricsSection.jsx   # MAE, RMSE, R², equation & residual chart
│   │   │   ├── DatasetTable.jsx     # Searchable records & CSV export
│   │   │   └── AlgorithmGuide.jsx   # Beginner ML guide & Viva Voce Q&A
│   │   ├── services/
│   │   │   └── api.js               # Centralized Axios API service
│   │   ├── App.jsx                  # Main application state & responsive layout
│   │   ├── main.jsx                 # React root DOM mount
│   │   └── index.css                # Tailwind CSS v4 & custom glassmorphism
│   ├── index.html                   # HTML template with Google Fonts
│   ├── vite.config.js               # Vite config with @tailwindcss/vite
│   └── package.json                 # Frontend dependencies
│
└── README.md                        # Complete project documentation
```

---

## ⚙️ 4. Installation & Setup Instructions

### Prerequisites
- **Python 3.10+**
- **Node.js v18+ and npm**

---

### Step 1: Set Up and Start the FastAPI Backend

Open a terminal in the project directory:

```bash
# Navigate to the backend folder
cd backend

# Install required Python packages
pip install -r requirements.txt

# Start the FastAPI server on port 8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The backend server is live at:
- **API URL:** `http://127.0.0.1:8000`
- **Interactive Swagger Docs:** `http://127.0.0.1:8000/docs`

---

### Step 2: Set Up and Start the React Frontend

Open a **second terminal** in the project directory:

```bash
# Navigate to the frontend folder
cd frontend

# Install npm dependencies
npm install

# Start the Vite development server on port 5173
npm run dev
```

Open **`http://localhost:5173`** in your web browser.

---

## 🔌 5. Backend REST API Endpoints

| Method | Endpoint | Description | Request Body / Response |
| :---: | :--- | :--- | :--- |
| `GET` | `/` | Health check & API status | Returns server status and version |
| `POST` | `/api/predict` | Predict marks from study hours | `{"study_hours": 7.5}` → `PredictionResponse` |
| `GET` | `/api/metrics` | Model evaluation metrics | Returns MAE, RMSE, R², equation, test comparisons |
| `GET` | `/api/dataset` | Dataset records and statistics | Returns summary and 40 student data points |
| `GET` | `/api/chart-data` | Visualization points for Recharts | Returns scatter points and regression fit line |

---

## 🧠 6. Machine Learning Workflow Explained

1. **Consistent Dataset (`data.py`):**
   - 40 reproducible student records (`seed=42`).
   - Reflects continuous positive correlation ($r \approx 0.99$) with natural variance.

2. **Zero Data Leakage:**
   - 80% of data is used solely to fit the line.
   - 20% of data is strictly reserved for evaluating accuracy on unseen cases.

3. **Ordinary Least Squares (OLS) Training (`model.py`):**
   - Learns the optimal slope ($m$) and intercept ($c$) in:
     $$\text{Marks} = (m \times \text{Hours}) + c$$
   - Achieves $R^2 \approx 0.989$ (explaining ~98.9% of variance).

4. **Physical Boundary Enforcement [0, 100%]:**
   - Standard linear equations can extrapolate to negative numbers or scores over 100%.
   - The backend applies:
     $$\text{final\_prediction} = \min(\max(\text{raw}, 0.0), 100.0)$$
   - It also returns `clamping_note` to remind students that clipping does not guarantee model validity at extreme hours.

---

## 🧪 7. Test Execution & Verification

### 1. Backend Test Suite (`backend/test_backend.py`)
Tested using FastAPI `TestClient`:
- Health check endpoint verification (HTTP 200).
- Predictions across normal hours (`2h`, `5h`, `8h`, `11h`).
- Clamping of excessive hours (`16h` clamped to `100%` with notice).
- Input validation (rejecting negative hours and hours $> 24$).
- Metrics endpoint validation ($R^2 > 0.7$, MAE, RMSE, equation).
- Dataset and Recharts chart-data endpoint integrity.

```text
Ran 7 tests in 0.067s
OK
```

### 2. Frontend Production Build (`npm run build`)
```text
vite v8.3.4 building client environment for production...
✓ 2536 modules transformed.
dist/index.html                   1.11 kB
dist/assets/index-DkpuajVD.css   46.75 kB
dist/assets/index-kTbVi5_l.js   731.48 kB
✓ built in 427ms
```

---

## 🎓 8. College Viva Voce Questions & Answers

**Q1: Why did you separate the React frontend from the Python backend?**  
*Answer:* A decoupled client-server architecture separates concerns: Python and scikit-learn handle mathematical model training and inference via an API, while React provides high-performance, responsive UI rendering.

**Q2: What is the significance of the $R^2$ score?**  
*Answer:* $R^2$ is the coefficient of determination. An $R^2 = 0.989$ means that approximately 98.9% of the variation in exam marks can be explained by daily study hours.

**Q3: How does the app avoid displaying raw HTML or security vulnerabilities?**  
*Answer:* All data is transferred as structured JSON and rendered using native React components, avoiding raw HTML injections or `dangerouslySetInnerHTML`.
