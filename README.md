# todoo.

**A lightweight task management web application built with Python, Flask, and PostgreSQL.**

todoo is a personal full-stack development project designed to help users organize their daily activities through a simple and intuitive interface. Users can create an account, manage folders, add tasks, track their completion, and delete items they no longer need.

## About the Project

Beyond building a functional task manager, the primary goal of todoo was to strengthen my understanding of how a web application works from end to end.

Rather than relying on high-level abstractions, I focused on implementing core functionality myself to better understand the interactions between the frontend, backend, and database.

Throughout this project, I gained hands-on experience with:

- **Backend development** — Building HTTP routes, handling requests and responses, and structuring a Flask application using Blueprints.
- **Database management** — Designing relational schemas in PostgreSQL, implementing CRUD operations, and managing database connections with psycopg.
- **Authentication and security** — Implementing user registration, password hashing, login sessions, and protected workflows.
- **Frontend integration** — Connecting HTML, CSS, and JavaScript to backend functionality using forms and asynchronous `fetch()` requests.
- **Software engineering practices** — Organizing reusable functions, managing environment variables, handling exceptions, and using Git for version control.

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Database | PostgreSQL |
| Database Driver | psycopg 3 |
| Frontend | HTML, CSS, JavaScript |
| Authentication | Flask sessions, Werkzeug password hashing |
| Version Control | Git, GitHub |

## Local Installation

Follow these instructions to set up and run todoo on your local machine.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todoo
```

### 2. Create a Python Virtual Environment

It is recommended to create a dedicated Python virtual environment directly inside the repository to isolate the project's dependencies.

From the repository root, run:

```bash
python3 -m venv python_env
```

Activate the environment.

**Linux / macOS**

```bash
source python_env/bin/activate
```

**Windows (PowerShell)**

```powershell
.\python_env\Scripts\Activate.ps1
```

### 3. Install Python Dependencies

With your virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

### 4. Install and Configure PostgreSQL

todoo uses PostgreSQL as its relational database.

Download and install PostgreSQL from the official website:

https://www.postgresql.org/download/

Once installed:

1. Make sure the PostgreSQL server is running.
2. Ensure you have a PostgreSQL role with permission to create databases and schemas.
3. Create a dedicated database for the application.

For example, from the PostgreSQL command-line interface (`psql`):

```sql
CREATE DATABASE todoo_db;
```

Connect to your new database:

```sql
\c todoo_db
```

### 5. Initialize the Database Schema

The repository includes a `schema.sql` file containing the SQL definitions required to initialize the application's database structure.

Execute the script against your newly created database:

```bash
psql -U <postgres_user> -d todoo_db -v ON_ERROR_STOP=1 -f schema.sql
```

Make sure the script executes without errors.

You can then verify that the tables were created successfully by connecting to PostgreSQL:

```bash
psql -U <postgres_user> -d todoo_db
```

If the application uses the `todoo_schema` schema, list its tables with:

```sql
\dt todoo_schema.*
```

You should find the three main tables:

- `users`
- `folders`
- `tasks`

### 6. Configure Environment Variables

For security reasons, local credentials and application secrets are not included in the repository.

Create your own `.env` file at the root of the project, using `.env.example` as a template.

**Linux / macOS**

```bash
cp .env.example .env
```

**Windows (PowerShell)**

```powershell
Copy-Item .env.example .env
```

Update the variables in `.env` with your own PostgreSQL connection details and Flask secret key.

Make sure the environment variables match the configuration expected by the application.

**Important:** Never commit your `.env` file to GitHub, as it may contain sensitive credentials.

### 7. Run the Application

You're ready!

Make sure:

- Your Python virtual environment is activated.
- PostgreSQL is running and properly configured.
- Your `.env` file contains valid configuration values.
- All database tables have been created.

From the root directory of the repository, run:

```bash
flask run
```

By default, the application will be available at:

http://127.0.0.1:5000/

Open the URL in your browser to start using todoo.

---

## Project Status

todoo was developed as a hands-on learning project, with an emphasis on understanding fundamental software engineering concepts and building a complete application from scratch.

The application is intended for local development and educational use.

## Author

Raphaël Dahomay