FROM python:3.9.16-slim-bullseye
WORKDIR /app
COPY . /app
EXPOSE 8000
#RUN pip install --no-cache-dir kafka-python pymongo
RUN pip install kafka-python pymongo
CMD ["python", "main.py"]
