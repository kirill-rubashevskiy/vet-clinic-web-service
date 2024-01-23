FROM python:3.11

WORKDIR /vet_clinic

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR ./app

COPY ./app .

CMD ["python3", "main.py"]