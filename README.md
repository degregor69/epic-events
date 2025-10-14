# Epic Events - OpenClassrooms Project

Epic Events is a CRM application developed as part of the OpenClassrooms Python Developer course. It uses **Python 3.13**, **SQLAlchemy**, and **PostgreSQL** to manage events and participants.

---

## Prerequisites

- Python 3.13 (installed via [pyenv](https://github.com/pyenv/pyenv))
- PostgreSQL 14 or higher
- pip (Python package manager)
- A terminal or IDE to run Python code

---

## Installation

1. **Clone the project:**

```bash
git clone <REPO_URL>
cd epic-events
```

2. **Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate
```

## Database Setup

1. **Create PostgreSQL database**

```sql
CREATE DATABASE epic_events;
CREATE USER epic_user WITH PASSWORD 'epic_password';
ALTER ROLE epic_user SET client_encoding TO 'utf8';
ALTER ROLE epic_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE epic_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE epic_events TO epic_user;
```

2. **Configure environment variables**
   In the project root, create a .env file or copy paste the .env.example file in your .env

```bash
DATABASE_URL=postgresql+psycopg2://epic_user:epic_password@localhost:5432/epic_events
```

## Initialize the Database

Once your .env file is ready, run:

```bash
python -m app.init_db
```

This script will :

- Drop the existing tables
- Recreate all tables based on the models
- Seed the db with initial data

## Verify installation

You can check by running this command

```bash
psql -U epic_user -d epic_events
\dt
SELECT * FROM users;
```
