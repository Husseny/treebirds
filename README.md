# treebirds

## Installation

[1] http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/
	https://www.sitepoint.com/virtual-environments-python-made-easy/

pip install virtualenv
virtualenv --version
pip install virtualenvwrapper
export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv treebirds

workon treebirds

pip install -r requirements.txt


[2] http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-mysql-for-django
	https://www.digitalocean.com/community/tutorials/how-to-use-mysql-or-mariadb-with-your-django-application-on-ubuntu-14-04
	https://docs.djangoproject.com/en/1.11/ref/databases/


export PATH=$PATH:/usr/local/mysql/bin

sudo /usr/local/mysql/support-files/mysql.server start
mysql -u root -p
CREATE DATABASE treebirds CHARACTER SET UTF8;
CREATE USER 'username'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON treebirds.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
quit


pip install mysqlclient


settings.py:
'ENGINE': 'django.db.backends.mysql',
'OPTIONS': {
    'read_default_file': '/path/to/my.cnf',
},


python manage.py check
python manage.py migrate
python manage.py createsuperuser

python manage.py runserver 0.0.0.0:8000

visit /admin

## Raw Sql with django
https://docs.djangoproject.com/en/1.11/topics/db/sql/


pip install -r requirements.txt
python manage.py migrate

