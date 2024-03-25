FROM python:3.8-slim as base
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG PORT 
ARG ID
ENV PORT=$PORT ID=$ID

FROM base as logging-service
COPY ./base /base
COPY ./logging-service /logging-app 
WORKDIR /logging-app
CMD sh -c "python app.py $PORT $ID"

FROM base as facade-service
COPY ./base /base
COPY ./facade-service /facade-app
WORKDIR /facade-app
CMD sh -c "python app.py $PORT"

FROM base as messages-service
COPY ./base /base
COPY ./messages-service /message-app
WORKDIR /message-app
CMD sh -c "python app.py $PORT $ID"
