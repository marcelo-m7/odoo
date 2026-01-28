
- Python 3.10 
```bash
py -3.10 -m venv 
# pip install ruff

```
- Install Postgres
- Install Visual Studio Code C++ https://visualstudio.microsoft.com/fr/downloads/

```bash
pip install setuptools wheel
pip install -r requirements.txt

# Start the db and init
 python odoo-bin -r dbuser -w dbpassword --addons-path=addons -d mydb -i base
```