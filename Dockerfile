FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
EXPOSE 5000