# CSCI_5828_WebProject

### Setup Django Environment

> Thanks to [Django Girls Tutorial](https://tutorial.djangogirls.org/en/installation/)

1. Setup Virtual Environment in HOME directory
```
$ mkdir <directory_name>
$ cd <directory_name>
$ python3 -m venv <virtualenv_name>
```

2. Start Virtual Environment
```
$ source <virtualenv_name>/bin/activate
```

3. Install Django using pip
```
(myvenv) ~$ pip install django~=1.11.0
```

### Build database

```bash
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```


### Run on Localhost

**Activate virtual environment before running the service**

```bash
$ python3 manage.py runserver
```

### The public link for this website
https://azurisky.pythonanywhere.com


You can create new recipe and edit them later, and our pivotal tracker link is [this](https://www.pivotaltracker.com/n/projects/2156952).
