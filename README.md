# treebirds
## Reddit like nested comments project using a stack of Mysql, Django & AngularJS

##### [Demo](https://husseny.xyz/nestedcomments/demo/)

## Installation

[1] Setup your django project

* Open a temrinal window and install virtualenv along with virtualenvwrapper:

```pip install virtualenv```

```pip install virtualenvwrapper```

```source /usr/local/bin/virtualenvwrapper.sh```

* Choose a folder for your virtual environment files:

```export WORKON_HOME=~/Envs```

* Create your virtual environment:

```mkvirtualenv treebirds```

* Activate your env:

```workon treebirds```

* Clone the repository, cd to its root and install the requirements:

```pip install -r requirements.txt```


[2] Connect to  your mysql datbase


* Install & run mysql server
* Create a database for your project along with a privileged user to work on the database:
* You can do it through the terminal:

```mysql -u root -p```

```CREATE DATABASE treebirds CHARACTER SET UTF8;```

```CREATE USER 'username'@'localhost' IDENTIFIED BY 'your_password';```

```GRANT ALL PRIVILEGES ON treebirds.* TO 'username'@'localhost';```

```FLUSH PRIVILEGES;```

```quit```

* Open database.cnf file and edit the paramaters according to your mysql settings

* Open treebirds/settings.py and edit the path to the absolute database.cnf file:
```python
'ENGINE': 'django.db.backends.mysql',
'OPTIONS': {
    'read_default_file': '/path/to/database.cnf',
}
```

* your django app should be able to connect to the database now.
* Through the terminal, cd to the project's root and run the following:

```python manage.py makemigrations```

```python manage.py migrate```

```python manage.py runserver 0.0.0.0:8000```

* On your browser, visit localhost:8000/nestedcomments/demo

### Helpful links and references:
	http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/
	https://www.sitepoint.com/virtual-environments-python-made-easy/
	http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-mysql-for-django
	https://www.digitalocean.com/community/tutorials/how-to-use-mysql-or-mariadb-with-your-django-application-on-ubuntu-14-04
	https://docs.djangoproject.com/en/1.11/ref/databases/
	https://bootsnipp.com/snippets/featured/collapsible-nested-comments