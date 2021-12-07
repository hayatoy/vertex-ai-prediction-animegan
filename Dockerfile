FROM python:3.7-buster

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt 

COPY app.py ./app.py

# Expose port 8080
EXPOSE 8080

ENTRYPOINT ["python3", "app.py"]