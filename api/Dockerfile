FROM python:3

WORKDIR /app/

ADD requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt && pip freeze

ADD . .

CMD python app.py
