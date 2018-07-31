# instant-paint-estimate
Instant Paint Estimates is a simple Django web app for instant house painting estimates. It allows a user to get a free online painting quote and also emails the quote to the user and the contractor.

See it in action:

https://fluidestimates.herokuapp.com/instantpaintestimate/

Running locally:

* If cloning the project to run locally you will need to update the database settings, SECRET_KEY settings and EMAIL_PASSWORD in the settings.py file as they are currently set to run on Heroku *
You will also need to comment the: django_heroku.settings(locals()) line

The home page is: http://127.0.0.1:8000/instantpaintestimate/ 

Quick start
clone the git repo into a local folder and transfer the instantpaintestimate folder into your Django project 

Create a virual environment and run: pip install -r requirements.txt from the root of the project

create a file named "secrets.sh"

eg. touch secrets.sh (mac and linux)

obtain a secret from: https://www.miniwebtool.com/django-secret-key-generator/ and add to secrets.sh

export SECRET_KEY='<secret_key>'

add secrets.sh to .gitignore file

Add to your Django project INSTALLED_APPS section of the settings file like this:

INSTALLED_APPS = [
... 'instantpaintestimate.apps.InstantpaintestimateConfig',
    'widget_tweaks',
    'bootstrapform',
    'bootstrap_datepicker',
    'datetimewidget'
]

Include the instantpaintestimate URLconf in your Django project urls.py file like this:

path('instantpaintestimate/', include('instantpaintestimate.urls')),

create a postgres db and add the credentials to settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'estimatesdb',
        'USER': 'name',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

In your Django project directory, run: python manage.py migrate to create the instantpaintestimate models.

The create an admin account:

python manage.py createsuperuser

then:

python manage.py makemigrations instantpaintestimate
to makemigrations for the app

then again run:

python manage.py migrate

Start the development server: python manage.py runserver 

 visit http://127.0.0.1:8000/admin/ to create paint estimate pricing properties.

Visit http://127.0.0.1:8000/instantpaintestimate/ to submit an estimte. 

If you need help with a Django project, please email me at: boris@boriswebappdevelopment.ca or visit my website and fill out the contact form at: https://www.boriswebappdevelopment.ca/
