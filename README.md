# APNet
The open source social media application for students.

---

###### To run code
1. Setup Python virtual environment
```sh
python -m venv .venv
```

2. Install the required pip packages
```sh
pip install -r requirements.txt
```

3. Save your secret keys into an .env file
```env
# Database credentials
DBNAME=
USER=
PASSWORD=

# Mailtrap account
MAILTRAP_PASSWORD=

# Session secret key
SECRET_KEY=
```

4. Start up the Flask session
```sh
python main.py
```