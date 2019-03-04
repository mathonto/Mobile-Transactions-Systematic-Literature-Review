FROM python:3

WORKDIR /app
COPY . .

RUN pip install pipenv
RUN python -m pipenv install

CMD ["python", "-m", "pipenv", "run", "python", "src/main.py"]