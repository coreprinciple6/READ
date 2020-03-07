## Installation
* Make sure you have python3 installed
* Create a virtual environment
* Source the virtual environment
* Switch to the directory: `spring2020.cse327.1.6/web_app/`
* Run `pip install -r requirements.txt`
* Switch to `spring2020.cse327.1.6/web_app/mysite/`
* Run `python manage.py runserver --noreload --nothreading`
    * NOTE: running with the `--noreload` and `--nothreading` options means changes are not automatically displayed in the django app, but this is necessary for the facial recognition to work.
* Go to `http://127.0.0.1:8000/read/`
