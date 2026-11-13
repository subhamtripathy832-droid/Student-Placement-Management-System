# Installation Guide

This guide assumes Python 3.10+ and MySQL 8+ are installed.

## Windows / PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env`, create the `placement_db` database in MySQL, then run:

```powershell
python init_db.py
python create_admin.py
python app.py
```

## Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`, create the MySQL database, then run:

```bash
python init_db.py
python create_admin.py
python app.py
```

## Database URL format

```text
mysql+pymysql://USERNAME:PASSWORD@HOST/DATABASE?charset=utf8mb4
```

If your password contains special URL characters, URL-encode those characters in the connection string.

## Common problems

- **Access denied:** check the MySQL username/password and the user's permissions.
- **Unknown database:** create `placement_db` before running `init_db.py`.
- **Module not found:** activate the virtual environment and run `pip install -r requirements.txt`.
- **Port 5000 already in use:** stop the other local server or adjust the development port in `app.py`.
