
# Odoo Development Environment Setup

This guide covers environment setup for **Odoo 19.0** using modern Python packaging tools.

## Prerequisites

### System Requirements
- **Python 3.10–3.13** - [Download from python.org](https://www.python.org/)
- **PostgreSQL 13+** - [Download from postgresql.org](https://www.postgresql.org/download/)
- **Git** - For version control
- **uv** (Recommended) - Modern Python package manager - [Installation guide](https://docs.astral.sh/uv/getting-started/installation/)
- **Visual Studio C++ Build Tools** (Windows only) - For compiling native extensions:
  - [Download from Visual Studio](https://visualstudio.microsoft.com/downloads/)
  - Select "Desktop development with C++"

### Platform-Specific Notes
- **Linux/macOS:** Full support including async I/O (`gevent`, `greenlet`) and LDAP
- **Windows:** Async features use threading; LDAP unavailable (use WSL for LDAP)

---

## Quick Start with uv (Recommended)

### 1. Install uv Package Manager
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative: via pip
pip install uv
```

### 2. Create Virtual Environment
```bash
# uv creates and manages venv automatically
uv venv

# Activate the environment
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### 3. Install Odoo + Dependencies
```bash
# Install all core dependencies (recommended)
uv pip install -e .

# Or install with development tools (ruff, pytest, freezegun)
uv pip install -e ".[dev]"

# Or install with LDAP support (Linux/macOS only)
uv pip install -e ".[ldap]"

# Or all extras combined
uv pip install -e ".[dev,ldap,test]"
```

### 4. Verify Installation
```bash
python -c "import odoo; print(f'Odoo {odoo.release.version} installed successfully')"
```

---

## Alternative: Setup with pip (Legacy)

If you prefer the traditional pip workflow:

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

---

## PostgreSQL Database Setup (All Methods)

### Create Database User
```bash
# Via PostgreSQL command line
createuser -P odoo  # Enter password when prompted

# Or via PostgreSQL console (psql)
CREATE USER odoo WITH PASSWORD 'odoo';
CREATE DATABASE odoo_local OWNER odoo;
GRANT ALL PRIVILEGES ON DATABASE odoo_local TO odoo;
```

### Initialize Odoo Database
```bash
# Ensure virtual environment is activated first
# Windows: .venv\Scripts\activate or env\Scripts\activate
# Linux/macOS: source .venv/bin/activate or source env/bin/activate

# Initialize database with base module
python odoo-bin \
  --db-filter=odoo_local \
  -r odoo \
  -w odoo \
  --addons-path=addons \
  -d odoo_local \
  -i base
```

**Parameters explained:**
- `-r` / `--db_user`: PostgreSQL username
- `-w` / `--db_password`: PostgreSQL password
- `--db-filter`: Only load matching database names
- `--addons-path`: Path to addon modules directory
- `-d`: Database name to create/use
- `-i`: Comma-separated list of modules to install

---

## Running Odoo

### Start Development Server
```bash
# Simple start (uses default config)
python odoo-bin -d odoo_local

# With explicit configuration
python odoo-bin \
  --db-filter=odoo_local \
  -r odoo \
  -w odoo \
  --addons-path=addons \
  -d odoo_local
```

**Access at:** http://localhost:8069

### Install Additional Modules
```bash
# Install CRM, Sales, and Accounting modules
python odoo-bin -r odoo -w odoo -d odoo_local -i crm,sale,account

# Upgrade existing module after code changes
python odoo-bin -r odoo -w odoo -d odoo_local -u crm --stop-after-init
```

### Run Tests
```bash
# Run all tests for a module
python odoo-bin -r odoo -w odoo -d test_db --test-enable --stop-after-init

# Run tests with specific tags
python odoo-bin -d test_db --test-tags=/crm --stop-after-init
```

---

## Code Quality & Linting

Odoo uses **ruff** for code style enforcement (see [ruff.toml](ruff.toml)).

```bash
# Format code
ruff format addons/my_addon

# Check for violations
ruff check addons/my_addon

# Auto-fix issues
ruff check --fix addons/my_addon
```

---

## Troubleshooting

### uv-specific Issues

#### "uv: command not found"
```bash
# Verify uv is installed
uv --version

# If not, reinstall
pip install uv
```

#### Can't resolve dependencies with uv
```bash
# Clear uv cache
uv cache clean

# Reinstall with verbose output
uv pip install -e . -v
```

### Common Installation Issues

#### "psycopg2" Installation Fails (Windows)
**Error:** `error: Microsoft Visual C++ 14.0 or greater is required`

**Solutions:**
1. Install Visual Studio C++ Build Tools (see Prerequisites)
2. Use pre-compiled binary: `uv pip install psycopg2-binary` (instead of psycopg2)

#### "Database does not exist" Error
```bash
# Create and initialize database
python odoo-bin -r odoo -w odoo --addons-path=addons -d odoo_local -i base
```

#### PostgreSQL Connection Refused
- Verify PostgreSQL is running: `psql -U odoo -d postgres`
- Check credentials match PostgreSQL user
- **Windows:** Check if PostgreSQL service is running (Services app)
- **Linux:** `sudo systemctl status postgresql`

#### Port 8069 Already in Use
```bash
# Use different port
python odoo-bin --xmlrpc-port=8070 -d odoo_local
```

#### "No module named 'odoo'" Error
```bash
# Activate virtual environment
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

# Reinstall in editable mode
uv pip install -e .
```

---

## Project Structure

```
odoo/
├── .github/
│   └── copilot-instructions.md  # AI agent development guide
├── odoo/                         # Core framework (ORM, HTTP, models, fields)
├── addons/                       # Business modules (CRM, Sales, Accounting, etc.)
├── setup/                        # Installation scripts
├── odoo-bin                      # CLI entry point
├── pyproject.toml               # Modern dependency management (recommended)
├── requirements.txt             # Legacy pip dependencies
├── ruff.toml                    # Code style rules
├── setup.py                     # Legacy setuptools config
└── SETUP.md                     # This file
```

---

## Development Workflow

### Useful Commands

```bash
# List installed modules
python odoo-bin -d odoo_local --list

# Upgrade module after code changes
python odoo-bin -r odoo -w odoo -d odoo_local -u crm --stop-after-init

# Database shell (PostgreSQL)
psql -U odoo -d odoo_local

# Clear cache and restart
python odoo-bin --invalidate-cache -d odoo_local

# Generate requirements.txt from pyproject.toml (if needed)
uv pip compile pyproject.toml -o requirements.txt
```

### Working with Dependencies

```bash
# Add new dependency to pyproject.toml, then:
uv pip install -e .

# Update all dependencies to latest compatible versions
uv pip install --upgrade -e .

# Check outdated packages
uv pip list --outdated
```

---

## Next Steps

1. **Read Development Guide:** [.github/copilot-instructions.md](.github/copilot-instructions.md)
2. **Explore Sample Addons:** Check `addons/crm/` or `addons/sale/` for patterns
3. **Run Tests:** Each addon has a `tests/` directory
4. **Official Docs:** [Odoo Developer Documentation](https://www.odoo.com/documentation/master/developer/)

---

## Commit Tags Convention

Tags prefix your commits for categorization:

- **[FIX]** - Bug fixes (stable or recent dev bugs)
- **[REF]** - Refactoring (heavy feature rewrites)
- **[ADD]** - Adding new modules
- **[REM]** - Removing resources (dead code, views, modules)
- **[REV]** - Reverting commits
- **[MOV]** - Moving files (use `git mv`, preserve history)
- **[REL]** - Release commits (major/minor versions)
- **[IMP]** - Improvements (most dev changes)
- **[MERGE]** - Merge commits (forward ports, multi-commit features)
- **[I18N]** - Translation file changes
- **[PERF]** - Performance patches
- **[CLN]** - Code cleanup
- **[LINT]** - Linting passes