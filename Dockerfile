FROM python:3.10

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./label_approved /app/label_approved

ENV PYTHONPATH=/app

CMD ["python", "-m", "label_approved"]
