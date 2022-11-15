FROM python:3.10

ADD . /app

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

CMD ["python", "./app/git_leaks.py"]