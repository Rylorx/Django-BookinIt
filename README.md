[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/bknTyRar)
# Django Practice Assessment

**Live Site:** [https://project-a-13-cs3240-ae8bfcb76eb4.herokuapp.com/](https://project-a-13-cs3240-ae8bfcb76eb4.herokuapp.com/)

__Contributors:__
#
Sam Banjade  Role: Testing
#
Sam Brooks  Role: Software Architext
#
Evelyn Nguyen  Role: Scrum Master
#
Ryan LeKuch  Role: DevOps
#
Jonathan Varghese  Role: Requirements Manager

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd project-a-13_for_github
```

### 2. Create Virtual Environment
```bash
python -m venv myenv
.\myenv\Scripts\activate  # Windows
# source myenv/bin/activate  # Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables Setup
Copy `.env.example` to `.env` and fill in your actual values:
```bash
cp .env.example .env
```

Required environment variables:
- `SECRET_KEY` - Django secret key (generate a new one)
- `DEBUG` - Set to `True` for development, `False` for production
- `GOOGLE_CLIENT_ID` - From Google Cloud Console
- `GOOGLE_CLIENT_SECRET` - From Google Cloud Console
- `AWS_ACCESS_KEY_ID` - From AWS IAM
- `AWS_SECRET_ACCESS_KEY` - From AWS IAM
- `AWS_STORAGE_BUCKET_NAME` - Your S3 bucket name
- `SITE_ID` - Django site ID (2 for local, 4 for production)

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Load Initial Data (Optional)
```bash
python manage.py shell
>>> from books_script import load_books
>>> load_books()
>>> exit()
```

# Super User Account:

To create a superuser for local development, use:
```bash
python manage.py createsuperuser
```

For Heroku deployment:
```bash
heroku run python manage.py createsuperuser
```


Common Problems:

How do I push the latest code to Heroku? Simply use this command below:
# git push heroku main

If I add a new dependency or framework, how can I update the requirements.txt properly? Use the command: 
# pip freeze > requirements.txt

How do I migrate into the Heroku database? Use the command below:
# heroku run python manage.py migrate

How do I make migrations to Django? Use the command below:
# python manage.py migrate

How do I create a superuser? Simply use the command below:
# heroku run python manage.py createsuperuser

NOTE WE CAN USE THE SAME DJANGO COMMANDS WITH HEROKU TO UPDATE OUR LAUNCHED WEBPAGE!!!!

# How to run myenv in case you forget
.\myenv\Scripts\activate





Helpful Resources:

# Deploying Django on Heroku: Good for resolving starting issues:

https://www.youtube.com/watch?v=HgDEFnMV16k


