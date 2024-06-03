FROM python:3.9

WORKDIR /app

COPY requirements.txt .

COPY resources /app/resources

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]

