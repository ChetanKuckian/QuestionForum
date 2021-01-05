# QuestionForum
This is an API Endpoints project which can be used to build a Question Answer based website.<br/>
The project is developed using django rest framework.<br/>
The django server is hosted on an AWS EC2 machine and using an AWS RDS MySQL instance database.<br/>
Use this [Swagger link](http://3.131.97.125:8000/swagger/) or [Redoc link](http://3.131.97.125:8000/redoc/) to know more about the endpoints.

- To run this project on local machine and with an SQLite database, one can download this repository and install the necessary libraries using the requirements.txt.
and then run
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```
- To connect to an AWS RDS database instance replace
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
in settings.py with
```
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'RDS_DB_NAME',
            'USER': 'RDS_USERNAME',
            'PASSWORD': 'RDS_PASSWORD',
            'HOST': 'RDS_HOSTNAME',
            'PORT': 'RDS_PORT',
        }
```
