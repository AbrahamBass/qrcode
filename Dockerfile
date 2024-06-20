FROM python:3.9-slim

RUN apt-get update -y
RUN apt-get install -y libzbar0

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .  

CMD ["fastapi", "run", "app/main.py", "--port", "80"]