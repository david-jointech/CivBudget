FROM eorlbruder/gunicorn
MAINTAINER  David Magnus Henriques <eorlbruder@magnus-henriques.de>

RUN mkdir -p /usr/share/webapps/CivBudget
ADD assets/* /usr/share/webapps/CivBudget/

WORKDIR /usr/share/webapps/CivBudget
RUN pip install django-bootstrap3
RUN pip install django
RUN pip install mysqlclient
RUN pip install python-dateutil
RUN pip install gunicorn
RUN pip install django-graphos

ADD assets/fcrontab /etc/fcrontab
RUN fcrontab /etc/fcrontab

ADD assets/start_gunicorn /
