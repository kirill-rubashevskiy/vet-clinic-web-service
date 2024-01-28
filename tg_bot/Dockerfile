FROM python:3.11

WORKDIR /code

ENV PYTHONPATH=/code \
    FASTAPI_URL=http://web:5555

COPY ./tg_bot ./tg_bot

RUN pip install --no-cache-dir -r ./tg_bot/requirements.txt

WORKDIR /code/tg_bot

CMD ["python3", "bot.py"]