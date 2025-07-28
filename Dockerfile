FROM python:3.13-slim

WORKDIR /code

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

RUN chmod +x /code/entrypoint-web.sh

EXPOSE 8000

ENTRYPOINT ["/code/entrypoint-web.sh"]
CMD ["uvicorn", "settings.asgi:application", "--host", "0.0.0.0", "--port", "8000"]