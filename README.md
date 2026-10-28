# NoteMind

**NoteMind** is a personal notes and study-material manager built with Flask and PostgreSQL. It helps users upload, organize, search, and revisit their notes from one place.

> Note: This README describes the features and architecture established for the project so far. Update the setup commands and configuration names if your local repository uses different values.

## Features

- **User accounts** — registration, login, and session-based authentication.
- **Upload notes** — upload supported study materials and keep them associated with your account.
- **Text extraction** — extract readable text from:
  - `.txt`
  - `.docx`
  - `.pdf`
- **My Notes** — browse and open uploaded notes.
- **Search** — find notes using their extracted text and related content.
- **Categories and tags** — organize material by subjects and topics.
- **Summaries** — store summaries associated with notes. The current project direction is to support offline functionality rather than require a paid external AI API.
- **PostgreSQL storage** — store user, note, category, tag, summary, and activity metadata in a relational database.
- **Minimal web interface** — a Flask-rendered interface, with UI styling and dark mode intended as part of the frontend improvements.

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Database | PostgreSQL |
| Database access | `psycopg2` |
| Text extraction | Python libraries for TXT, DOCX, and PDF |
| Frontend | HTML, CSS, JavaScript, Jinja templates |
| Authentication | Password hashing and Flask sessions |

## Project Structure

The exact structure may vary as development continues. A typical layout is:

```text
NoteMind/
├── app.py
├── config.py
├── init_db.py
├── schema.sql
├── database/
│   ├── config.py
│   ├── connection.py
│   ├── init_db.py
│   ├── migrations.py
│   └── schema.sql
├── migrations/
│   └── 001_initial_schema.sql
├── models/
│   ├── note_model.py
│   └── user_model.py
├── routes/
│   ├── auth_routes.py
│   └── note_routes.py
├── services/
│   ├── auth_service.py
│   ├── category_assignment.py
│   ├── category_service.py
│   ├── keywords.py
│   ├── note_service.py
│   ├── question_service.py
│   ├── recommendation_service.py
│   ├── summary_service.py
│   ├── tag_assignment.py
│   ├── tag_service.py
│   └── text_extractor.py
├── templates/
├── uploads/
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

- `app.py` — creates/configures the Flask application and registers routes & CLI commands (`flask init-db`, `flask migrate-db`).
- `init_db.py` / `database/init_db.py` — automated database initialization script for new environments.
- `schema.sql` / `database/schema.sql` — PostgreSQL DDL defining all required tables, relations, and indexes.
- `migrations/` — ordered SQL migration scripts managed by `database/migrations.py`.
- `routes/` — request and page-handling logic.
- `models/` — database query and data persistence functions.
- `services/` — business logic for text extraction, categorization, tagging, summarization, and search.
- `templates/` — HTML/Jinja templates.
- `uploads/` — uploaded study materials and documents.

Your repository may contain additional route and service modules; keep the README structure in sync with the actual files.

## Database Design

NoteMind uses PostgreSQL. The planned schema includes the following tables:

| Table | Purpose |
|---|---|
| `users` | User profile, email, password hash, and creation time |
| `notes` | Note metadata, stored file path, file type, and extracted content |
| `categories` | Available subject categories |
| `note_categories` | Many-to-many relationship between notes and categories |
| `summaries` | Summary text associated with a note |
| `tags` | Reusable topic tags |
| `note_tags` | Many-to-many relationship between notes and tags |
| `search_history` | Search queries made by users |
| `note_views` | Note-view activity for usage analytics |

Notes are linked to their owners. Foreign-key relationships use cascading deletion where specified in the schema.

## Getting Started

### 1. Prerequisites

Install or prepare:

- Python 3
- PostgreSQL
- `pip`
- Git

### 2. Clone the repository

```bash
git clone <https://github.com/mohamedfahadlal/NoteMind>
cd NoteMind
```


### 3. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

If the repository contains `requirements.txt`:

```bash
pip install -r requirements.txt
```

If it does not, install the dependencies listed by the project and create a `requirements.txt` so the environment can be reproduced. The database adapter used by this project is `psycopg2` (commonly installed with `psycopg2-binary` for local development).

### 5. Create the PostgreSQL database

Open PostgreSQL:

```bash
sudo -u postgres psql
```

Create the database:

```sql
CREATE DATABASE notemind;
```

Exit with:

```sql
\q
```

If the application connects using a dedicated PostgreSQL role, create that role and grant it access to the database, or configure the application to use an existing role. Use the same database name, username, password, host, and port in your application configuration.

If your project already has a database and schema, do not recreate them unnecessarily.

### 6. Configure environment variables

Use the variable names expected by your application. For example, a local `.env` file might contain:

```env
FLASK_SECRET_KEY=replace-with-a-long-random-secret
DB_NAME=notemind
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

These names are examples; match them to the configuration code in your repository. Do not commit `.env` or real credentials to Git.

### 7. Initialize the database schema

Initialize all required tables, indexes, and default categories:

```bash
python init_db.py
```

Alternatively, you can initialize the database using the Flask CLI:

```bash
flask init-db
```

Or execute the schema SQL directly with `psql`:

```bash
psql -U notemind_user -d notemind -f schema.sql
```

Available database setup commands:

- `python init_db.py` — creates all tables, foreign keys, indexes, and seeds default categories.
- `python init_db.py --check` — verifies connectivity and confirms all required tables are present.
- `python init_db.py --migrate` — discovers and applies any pending migrations in `migrations/`.
- `python init_db.py --drop` — drops and recreates all tables (use with caution: removes all data).
- `python database/migrations.py --status` — displays migration status (applied vs pending).

### 8. Run the application

For a Flask application configured through `app.py`, try:

```bash
python app.py
```

Open the local address printed by Flask in your browser (commonly `http://127.0.0.1:5000/`).

If the project uses a different application entry point or run command, use that instead. For development, keep debug mode limited to your local machine.

## Typical Workflow

1. Register an account and log in.
2. Upload a TXT, DOCX, or PDF study document.
3. Let NoteMind extract the document's text.
4. Open the note from **My Notes**.
5. Search for notes by relevant words or content.
6. Organize notes with categories and tags.
7. Review a note's saved summary, where available.

## Security and Data Handling

- Store password hashes, never plaintext passwords.
- Keep secret keys and database credentials in environment variables.
- Validate uploaded file types and enforce a reasonable upload-size limit.
- Use secure filenames and prevent uploaded files from being served or executed as application code.
- Ensure each user can access only their own notes and uploaded files.
- Do not commit `.env`, local databases, private uploads, or virtual-environment files.

## Current Development Direction

The project has been developed in stages, including authentication, note upload and viewing, text extraction, search, and summary-related functionality. Current and planned improvements include:

- Refining the interface into a polished, minimal design.
- Completing consistent dark-mode support.
- Improving offline note-processing features and automatic categorization.
- Strengthening error handling, validation, and testing.

Features marked as planned or in progress should not be treated as complete until verified in the current codebase.

## Troubleshooting

### PostgreSQL reports that a role does not exist

Check which role the application uses and whether it exists in PostgreSQL. Either create the required role and grant access, or update the application configuration to use the correct role.

### `ModuleNotFoundError: No module named 'psycopg2'`

Activate the project's virtual environment and install the PostgreSQL adapter required by the application.

### Uploaded documents contain no extracted text

Confirm that the file format is supported, the extraction dependency is installed, and the document actually contains selectable text. Scanned PDFs may require OCR, which is separate from ordinary PDF text extraction.

### A page returns 404 Not Found

Check that the route is registered, the URL and HTTP method match the route definition, and the template or redirect points to the correct endpoint.

## Contributing

1. Create a branch for your change.
2. Make a focused change and test the affected workflow.
3. Avoid committing credentials, private documents, or generated upload data.
4. Submit a pull request or merge the change through your normal Git workflow.

## License

No license has been specified yet. Add a `LICENSE` file and update this section if you intend to distribute the project publicly.
