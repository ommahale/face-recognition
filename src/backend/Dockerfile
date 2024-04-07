FROM python:3.11.3

WORKDIR /app/api

COPY . .
RUN pip --version
RUN pip install --upgrade pip
RUN pip install tensorflow==2.16.1 deepface==0.0.89 fastapi==0.110.1 uvicorn==0.29.0 python-multipart==0.0.9

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["python", "main.py", "0.0.0.0", "8000"]