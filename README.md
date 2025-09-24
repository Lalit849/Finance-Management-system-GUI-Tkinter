# 🧾 Finance-Management-System-built-with-Python(Tkinter + SQLite)

A Finance Management System built with Python (Tkinter + SQLite) that helps users manage company-level incomes, expenses, balances, and analyze them with charts.
---

## 📌 Table of Contents
- <a href="#overview">Overview</a>
- <a href="#business-problem">Business Problem</a>
- <a href="#tools--technologies">Tools & Technologies</a>
- <a href="#project-structure">Project Structure</a>
- <a href="#research-questions--key-findings">Research Questions & Key Findings</a>
- <a href="#dashboard">Dashboard</a>
- <a href="#how-to-run-this-project">How to Run This Project</a>
- <a href="#final-recommendations">Final Recommendations</a>
- <a href="#author--contact">Author & Contact</a>
---

<h2><a class="anchor" id="overview"></a>Overview</h2>

This desktop app allows multiple users to register/login, add companies, record transactions, export reports, and visualize financial data using interactive analytics.
---

<h2><a class="anchor" id="business-problem"></a>Business Problem</h2>

Managing multiple companies’ financial transactions manually leads to errors, lack of insights, and difficulty in auditing. Business owners require a centralized platform to:
 - Securely maintain company-wise income, expenses, and balance records.
 - Get real-time financial analytics for decision making.
 - Automate audits and reporting without relying on external software.
 - This system solves the problem by providing a desktop application with secure  authentication, data persistence, and interactive analytics.
---

<h2><a class="anchor" id="tools--technologies"></a>Tools & Technologies</h2>

- Programming Language: Python 3.x
- GUI Framework: Tkinter
- Database: SQLite
- Visualization: Matplotlib
- Libraries:
    - hashlib → Password hashing
    - sqlite3 → Database connection
    - ttk (Tkinter themed widgets)
    - PIL (Pillow) → Image handling
    - csv → Export reports
---

<h2><a class="anchor" id="project-structure"></a>Project Structure</h2>

```
FinanceManagementSystem/
│
├── finance.db              # SQLite Database (auto-created)
├── main.py                 # Main application (your code)
├── requirements.txt        # Dependencies list
├── README.md               # Project documentation
├── screenshots/            # App screenshots
│   ├── login.png
│   ├── dashboard.png
│   └── analytics.png
└── exports/                # CSV reports (user-generated)

```
---
<h2><a class="anchor" id="research-questions--key-findings"></a>Research Questions & Key Findings</h2>

RQ1: How can small businesses efficiently manage company-wise income and expenses?
    ✅ Finding: Automating entry and balance updates reduces manual errors.

RQ2: How to provide meaningful insights for decision making?
    ✅ Finding: Bar charts (Income vs Expense) help compare companies.
    ✅ Finding: Pie charts (Expense distribution) reveal cost-heavy companies.

RQ3: How to ensure security of financial data?
    ✅ Finding: Passwords stored with SHA-256 hashing protect user credentials.

RQ4: How to make audit processes faster?
    ✅ Finding: Instant audit functionality recomputes balances and shows profit/loss status.

---
<h2><a class="anchor" id="dashboard"></a>Dashboard</h2>

- Login / Signup / Forgot Password → Secure authentication.
- Dashboard
   - Add / Delete Companies
   - Add Income & Expense transactions
   - Automatic Balance calculation
   - Audit button for profit/loss report
   - Export CSV reports
   - Analytics
   - Bar Chart (Income vs Expense)
   - Pie Chart (Expense Distribution)

![Finance_management_dashboard](<img width="1915" height="1017" alt="Bar_plot_analytics png" src="https://github.com/user-attachments/assets/83913221-9fb9-46ba-8d09-f52ea1d4789d" />
)
---
<h2><a class="anchor" id="final-recommendations"></a>Final Recommendations</h2>

- Deploy an admin panel for multi-user monitoring.
- Add forecasting (ML models) to predict future cash flow.
- Enhance with role-based access control for larger teams.
- Integrate PDF report generation along with CSV.
- Cloud migration (PostgreSQL + Flask/Django backend) for enterpris

---
<h2><a class="anchor" id="author--contact"></a>Author & Contact</h2>

**Lalit Dhakar**  
📧 Email:lalitdhakar689@gmail.com
🔗 [LinkedIn](www.linkedin.com/in/lalit-dhakar-378101335)  
