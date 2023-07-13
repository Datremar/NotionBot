FROM python:3.10

WORKDIR /NotionBot

COPY /requirements.txt .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "./src/init_db.py"]
CMD ["python", "./src/main.py"]