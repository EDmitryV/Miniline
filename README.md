# Miniline
Django educational project. Clicker "Writer"
Installation instruction:
1)Prepare venv:
   open cmd
   go to /Miniline directory
   use "python -m venv env"
   use "env\Scripts\activate"
   use "pip install -r requirements.txt" 
2)Prepare db: 
   go to /Miniline/miniline directory 
   use "python manage.py makemigrations" 
   use "python manage.py migrate"
3)Run server
   use "python manage.py runserver"
4)Prepare required languges:
   create superuser
   login in admin panel
   add words_set with "ru" and "en" lang params
