FROM python:3.9
ADD main.py .
RUN pip install aiogram==2.25.2
RUN pip install requests
RUN pip install validators
RUN sudo apt install python3-dev libpq-dev
RUN pip3 install psycopg2
CMD [ "python","./main.py" ]