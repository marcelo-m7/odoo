
# Odoo Development Environment Setup

## Prerequisites

### System Requirements
- **Python 3.10+** - Download from [python.org](https://www.python.org/) or use `py -3.10` on Windows
- **PostgreSQL 12+** - Download from [postgresql.org](https://www.postgresql.org/download/)
- **Git** - For version control
- **Visual Studio Code C++ Build Tools** (Windows only) - For psycopg2 compilation:
  - Download from [Visual Studio Tools](https://visualstudio.microsoft.com/downloads/)
  - Select "Desktop development with C++"

### Required Tools
- ruff - Python linter/formatter (automatically configured)
- setuptools & wheel - Python packaging tools

---

## Installation Steps

### 1. Create Virtual Environment
```bash
# Windows
py -3.10 -m venv env
env\Scripts\activate

# Linux/macOS
python3.10 -m venv env
source env/bin/activate
```

### 2. Install Dependencies
```bash
pip install setuptools wheel
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL Database
```bash
# Create a database user for Odoo (on PostgreSQL)
createuser -P odoo  # Enter password when prompted

# Or via Windows/PostgreSQL console:
CREATE USER odoo WITH PASSWORD 'odoo';
CREATE DATABASE odoo_local OWNER odoo;
GRANT ALL PRIVILEGES ON DATABASE odoo_local TO odoo;
```

### 4. Initialize Database with Base Module
```bash
# Activate environment first
source env/bin/activate  # or env\Scripts\activate on Windows

# Initialize database (installs base module)
python odoo-bin \
  --db-filter=odoo_local \
  -r odoo \
  -w odoo \
  --addons-path=addons \
  -d odoo_local \
  -i base
```

**Parameters explained:**
- `-r` / `--db_user`: PostgreSQL username (default: odoo)
- `-w` / `--db_password`: PostgreSQL password
- `--db-filter`: Only load matching database names
- `--addons-path`: Path to addon modules
- `-d`: Database name to create/initialize
- `-i`: Modules to install (comma-separated)

---

## Running Odoo

### Development Server
```bash
python odoo-bin \
  --db-filter=odoo_local \
  -r odoo \
  -w odoo \
  --addons-path=addons \
  -d odoo_local
```

**Access the application at:** http://localhost:8069

### Install Additional Modules
```bash
python odoo-bin \
  -r odoo \
  -w odoo \
  -d odoo_local \
  -i crm,sale,account
```

### Run Tests
```bash
python odoo-bin \
  -r odoo \
  -w odoo \
  -d test_db \
  --test-enable \
  --stop-after-init
```

---

## Code Quality

### Linting & Formatting
Odoo uses **ruff** for code style enforcement. Check the [ruff.toml](ruff.toml) for rules.

```bash
# Format code
ruff format addons/my_addon

# Check for violations
ruff check addons/my_addon
```

---

## Troubleshooting

### "psycopg2" Installation Fails (Windows)
**Error:** `error: Microsoft Visual C++ 14.0 or greater is required`
- **Solution:** Install Visual Studio C++ Build Tools (see Prerequisites)
- Alternative: Install pre-compiled wheel: `pip install --only-binary :all: psycopg2-binary`

### "Database does not exist" Error
```bash
# Create and initialize database
python odoo-bin -r odoo -w odoo --addons-path=addons -d odoo_local -i base
```

### PostgreSQL Connection Refused
- Verify PostgreSQL is running: `psql -U odoo -d postgres`
- Check credentials in command match PostgreSQL user
- On Windows, PostgreSQL may run as a service (check Services app)

### Port 8069 Already in Use
```bash
# Use different port
python odoo-bin --xmlrpc-port=8070 -d odoo_local
```

### "No module named 'odoo'" Error
- Ensure virtual environment is activated: `env\Scripts\activate` (Windows) or `source env/bin/activate` (Linux/macOS)
- Verify dependencies are installed: `pip install -r requirements.txt`

---

## Project Structure

```
odoo/
├── odoo/              # Core framework (ORM, HTTP, models, fields)
├── addons/            # Business logic modules (CRM, Sales, Accounting, etc.)
├── setup/             # Installation scripts
├── odoo-bin           # CLI entry point
├── requirements.txt   # Python dependencies
├── ruff.toml         # Code style rules
└── SETUP.md          # This file
```

---

## Useful Commands

```bash
# List installed modules
python odoo-bin -d odoo_local --list

# Upgrade a module (reload after code changes)
python odoo-bin -r odoo -w odoo -d odoo_local -u crm --stop-after-init

# Database shell (PostgreSQL)
psql -U odoo -d odoo_local

# Clear cache and restart
python odoo-bin --db-filter=odoo_local -r odoo -w odoo -d odoo_local --invalidate-cache
```

---

# Commits tags:

Tags are used to prefix your commit. They should be one of the following

[FIX] for bug fixes: mostly used in stable version but also valid if you are fixing a recent bug in development version;

[REF] for refactoring: when a feature is heavily rewritten;

[ADD] for adding new modules;

[REM] for removing resources: removing dead code, removing views, removing modules, …;

[REV] for reverting commits: if a commit causes issues or is not wanted reverting it is done using this tag;

[MOV] for moving files: use git move and do not change content of moved file otherwise Git may loose track and history of the file; also used when moving code from one file to another;

[REL] for release commits: new major or minor stable versions;

[IMP] for improvements: most of the changes done in development version are incremental improvements not related to another tag;

[MERGE] for merge commits: used in forward port of bug fixes but also as main commit for feature involving several separated commits;

[CLA] for signing the Odoo Individual Contributor License;

[I18N] for changes in translation files;

[PERF] for performance patches;

[CLN] for code cleanup;

[LINT] for linting passes;