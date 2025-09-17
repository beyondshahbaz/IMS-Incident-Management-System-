FROM python

WORKDIR /app

COPY . . 

RUN pip install django
EXPOSE 8080

CMD ["python","manage.py","runserver"]



