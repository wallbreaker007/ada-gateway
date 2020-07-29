FROM python:2.7-alpine

ENV_CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0

ENV HOST 0.0.0.0
ENV PORT 58120

ENV FLASK_APP adaGateway.py
ENV FLASK_CONFIG production

copy .. /home/adaGateway
WORKDIR /home/adaGateway

# install requirements
RUN pip install -r requirements.txt

# run the app server
CMD ["gunicorn", "--bind", "0.0.0.0:58120", "--workers", "3", "app:app"]
