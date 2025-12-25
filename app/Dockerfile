FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8000
EXPOSE $PORT
CMD ["gunicorn","--workers","2","--bind","0.0.0.0:8000","main:app"]
