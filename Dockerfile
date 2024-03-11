FROM python:3.8-slim as base
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG PORT
ENV PORT=$PORT

FROM base as logging-service
COPY ./logging-service /logging-app
COPY ./base /base
WORKDIR /logging-app
CMD python app.py $PORT


FROM base as facade-service
COPY ./facade-service /facade-app
COPY ./base /base
WORKDIR /facade-app
CMD python app.py $PORT


FROM base as messages-service
COPY ./messages-service /message-app
COPY ./base /base
WORKDIR /message-app
CMD python app.py $PORT
