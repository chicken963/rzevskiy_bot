FROM python:3.9-slim

WORKDIR /app
COPY triggers_and_replies.csv venv config.yaml main.py requirements.txt /app/

RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate"
RUN pip install -r requirements.txt
EXPOSE 80

CMD ["python", "main.py"]