FROM python3.10.0a6-alpine3.13

ADD . /app

RUN pip install -r requirements.txt

CMD ["python", "./app/git_leaks.py"]