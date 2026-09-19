# ✅ Todo App

A simple full-stack Todo application built with **Python**, **Flask**, **Streamlit**, and **PostgreSQL**.

The application provides a clean interface for managing tasks while using a Flask REST API as the backend and PostgreSQL for persistent data storage.

## 🚀 Features

* ➕ Add new Todo tasks
* ✏️ Edit existing tasks
* 🗑️ Delete tasks
* ✅ Mark tasks as completed
* 🔍 Search Todos by task name
* 🔄 Filter Todos by:

  * All
  * Completed
  * Pending
* 📊 View Todo statistics:

  * Total tasks
  * Completed tasks
  * Pending tasks
* 🔌 REST API powered by Flask
* 🗄️ PostgreSQL database for persistent storage
* 🎨 Streamlit-based user interface

## 🛠️ Tech Stack

| Technology | Purpose                               |
| ---------- | ------------------------------------- |
| Python     | Core programming language             |
| Flask      | Backend REST API                      |
| Streamlit  | Frontend / UI                         |
| PostgreSQL | Database                              |
| psycopg2   | PostgreSQL connection                 |
| Requests   | Frontend-to-backend API communication |

## 📁 Project Structure

```text
Todo-app/
│
├── backend/
│   ├── app.py
│   ├── api.py
│   ├── routes.py
│   ├── database.py
│   └── config.py
│
├── database/
│   └── schema.sql
│
├── frontend/
│   └── app.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ How It Works

The application follows a simple three-layer architecture:

```text
┌─────────────────────┐
│     Streamlit UI    │
│      Frontend        │
└──────────┬──────────┘
           │ HTTP Requests
           ▼
┌─────────────────────┐
│     Flask REST API   │
│       Backend        │
└──────────┬──────────┘
           │ SQL Queries
           ▼
┌─────────────────────┐
│      PostgreSQL      │
│       Database       │
└─────────────────────┘
```

The Streamlit frontend communicates with the Flask backend through HTTP requests. The Flask API handles Todo operations and communicates with PostgreSQL for storing and retrieving data.

## 🔌 API Endpoints

### Get Todos

```http
GET /todos
```

Supports searching and filtering.

Example:

```http
GET /todos?search=python
```

Filter completed tasks:

```http
GET /todos?completed=true
```

Filter pending tasks:

```http
GET /todos?completed=false
```

### Add Todo

```http
POST /todos
```

Request body:

```json
{
  "task": "Learn Flask"
}
```

### Update Todo

```http
PUT /todos/<todo_id>
```

Request body:

```json
{
  "task": "Learn Flask REST API",
  "completed": true
}
```

### Delete Todo

```http
DELETE /todos/<todo_id>
```

### Get Statistics

```http
GET /todos/stats
```

Returns:

```json
{
  "total": 10,
  "completed": 6,
  "pending": 4
}
```

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Indrajith15/Todo-app.git
cd Todo-app
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE todo_db;
```

Then create the required `todos` table using the SQL schema provided in the `database` directory.

### 5. Configure database credentials

Create your database configuration using environment variables rather than committing credentials directly to GitHub.

Example:

```env
DB_HOST=localhost
DB_NAME=todo_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

Make sure `.env` is included in `.gitignore`.

## ▶️ Running the Application

The backend and frontend need to be run separately.

### Start the Flask Backend

From the `backend` directory:

```bash
python app.py
```

The API will run at:

```text
http://localhost:5000
```

### Start the Streamlit Frontend

From the `frontend` directory:

```bash
streamlit run app.py
```

The Streamlit application will open in your browser.

## 📊 Current Functionality

The frontend provides:

* Todo creation
* Todo editing
* Todo deletion
* Completion status management
* Search functionality
* Completed/Pending filtering
* Todo statistics

The backend exposes REST endpoints for all major Todo operations and performs input validation before modifying the database.

## 🔮 Future Improvements

Some possible improvements for future versions:

* 🔐 User authentication
* 👤 Multiple user accounts
* 📅 Todo due dates
* 🏷️ Categories and tags
* ⭐ Task priorities
* 📱 Responsive UI improvements
* 🐳 Docker support
* ☁️ Cloud deployment
* 🧪 Automated tests
* 🔒 Improved secrets and configuration management

## 📚 What I Learned

This project was built to practice:

* Python application structure
* REST API development with Flask
* HTTP methods and API communication
* PostgreSQL database integration
* SQL queries
* CRUD operations
* Streamlit application development
* Frontend-backend communication
* Input validation
* Git and GitHub workflow

## 👨‍💻 Author

**Indrajith Nair**

GitHub: [@Indrajith15](https://github.com/Indrajith15)

---

⭐ If you found this project useful, consider giving it a star!
