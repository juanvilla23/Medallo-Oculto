# **Medallo Oculto**
## How to Run the project Option #1 ##

1. First you need to clone the project from the repository and configure the .env file, we have a template of how to do it, on **.env_template** with the instructions.

2. You need have the docker daemon runing and up the compose with. `docker compose up -d`

3. Make the respective project migrations with `python manage.py migrate && python manage.py makemigration`.

4. Finally you can run the Django aplication with `python manage.py runserver`.

