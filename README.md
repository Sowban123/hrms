# HRMS – Human Resource Management System (Django + React)

A complete Human Resource Management System (HRMS) built using **Django (Backend)** and **React (Frontend)**.  
This system manages employees, attendance, leave requests, payroll, and reports in one centralized platform.

This project is designed to represent a real-world, company-level HR application with a modern frontend and a powerful backend.

---

## 🚀 Features

- 🔐 Authentication & Role-Based Access  
  - Admin  
  - HR  
  - Manager  
  - Employee  

- 👨‍💼 Employee Management  
  - Add, update, delete employees  
  - Upload employee photos  
  - Department-wise organization  

- 🕒 Attendance  
  - Daily check-in / check-out  
  - Monthly attendance reports  

- 🌴 Leave Management  
  - Apply for leave  
  - Approve / reject requests  
  - Leave history tracking  

- 💰 Payroll  
  - Salary calculation  
  - Payroll generation  
  - Salary records  

- 📊 Reports  
  - Attendance reports  
  - Employee reports  
  - Payroll summaries  

- 📈 Dashboard  
  - System overview with charts and statistics  

---

## 🛠 Tech Stack

### Backend
- Django (Python)
- Django REST Framework (for API)
- SQLite (can be upgraded to PostgreSQL)
- Authentication: Django Auth / JWT (future ready)

### Frontend
- React.js
- Axios for API calls
- HTML, CSS, Bootstrap / Tailwind
- Component-based UI

---
🔑 User Roles
Role	Access Level
Admin	Full system control
HR	Employee, payroll, leave approval
Manager	Team attendance & leave approval
Employee	Attendance & leave requests


## 📂 Project Structure

hrms/
├── accounts/ # Authentication & roles
├── attendance/ # Attendance system
├── dashboard/ # Dashboard logic
├── employees/ # Employee management
├── leaves/ # Leave management
├── payroll/ # Payroll system
├── reports/ # Report generation
├── templates/ # Django templates (for backend testing)
├── employee_photos/ # Uploaded employee images
├── db.sqlite3 # Database
├── manage.py
└── requirements.txt

frontend/ (React App)
├── src/
│ ├── components/
│ ├── pages/
│ ├── services/ # API calls
│ └── App.js



🎯 Purpose of This Project

Build a full-stack HRMS application

Show strong Django + React integration

Demonstrate real-world backend logic

...

  

🔮 Future Enhancements

JWT Authentication

Role-based API permissions

Salary slip PDF generation

Charts & analytics using Recharts

Deployment on AWS / Render / Railway

PostgreSQL database

Email & notification system

...



👨‍💻 Author

P.S Mohammed Sowban
Full Stack Developer (Django + React)



