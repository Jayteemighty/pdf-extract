##  **pdf-extract**

Simple app to extract nouns and verbs from pdf files


This backend is a Django REST Framework web application.

**Core Technologies:**

* Python
* Django REST Framework
* MongoDB

**Prerequisites:**

* Python 3.x ([https://www.python.org/downloads/](https://www.python.org/downloads/))
* pip (usually comes bundled with Python)

**Installation:**

1. Clone this repository:

```
git clone https://github.com/Jayteemighty/pdf-extract.git
```
2. Navigate to the project directory:

```
cd 'backend'
```
3. Create a virtual environment (recommended):

```
python -m venv venv
source venv/bin/activate  # For Linux/macOS
source venv/Scripts/activate  # For Windows
```
4. Install project dependencies:

```
pip install -r requirements.txt
```

**Development Setup:**

1. Run database migrations: (connect MongoDB Database)

```
python manage.py migrate
```
2. Create a superuser account (for initial admin access):

```
python manage.py createsuperuser
```
3. Start the development server:

```
python manage.py runserver
```

**Branching Strategy:**

**Do not push feature development directly to the main branch.**

* Develop new features on dedicated feature branches named descriptively (e.g., `feature/add-search`).
* Once a feature is complete and tested, create a pull request from the feature branch to the main branch for review and merging.

**Additional Notes:**

* This project uses a `.env` file for environment variables (database connection etc.). Configure this file locally following the `.env.example` template.