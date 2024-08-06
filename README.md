# **Medallo Oculto**
## **Descripcion of the problem**
In the city of Medellín tourism has grown exponentially in recent years; the information that the tourists receive about some touristic places is fake and this information is desorganized.
The problem not only affects a those who visit Medellín, it also affects tour guides or people who organize cultural events because some places or events are not so popular and many don´t know about those, sometimes people want to know new places of the city but they don´t know where to go or what plan to make
## Solution the Problem: ##

## How to Run the project Option #1 ##

1. First you need to clone the project from the repository and configure the .env file, we have a template of how to do it, on **.env_template** with the instructions.

2. You need have the docker daemon runing and up the compose with. `docker compose up -d`

3. Make the respective project migrations with `python manage.py migrate && python manage.py makemigration`.

4. Finally you can run the Django aplication with `python manage.py runserver`.

