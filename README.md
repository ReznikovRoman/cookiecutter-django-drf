# Django cookiecutter template

## Installation
1. Install Cookiecutter
```shell
$ pip install "cookiecutter>=1.7.0"
```

2. Run it against this repository
```shell
$ cookiecutter https://github.com/ReznikovRoman/cookiecutter-django-drf
```

3. You'll be prompted for some values. Provide them, then a Django project will be created for you.

Example:
```shell
full_name [Roman Reznikov]: John Doe
email [romanreznikov2002@yandex.ru]: john@gmail.com
github_username [ReznikovRoman]: JohnDoe
project_name [Django Project]: Reddit
project_slug [reddit]: 
project_short_description []: Reddit - project for ...
timezone [Europe/Moscow]: 
use_sentry [y]: 
use_pycharm [y]: n
use_black [n]:
```

4. New folder (`reddit_app`) will be created, now you can enter the project:
```shell
$ cd reddit_app
$ ls
```

5. Create a git repo:
```shell
$ git init
$ git add .
$ git commit -m "Initial commit"
```

6. Install project requirements:
```shell
$ python -m venv venv
$ source venv/bin/activate
$ pip install pip-tools
$ make compile-requirements
$ make sync-requirements
$ pip install -r requirements.txt
```

7. Build and run docker containers
```shell
$ docker-compose -f docker-compose.yml build
$ docker-compose -f docker-compose.yml up
```
