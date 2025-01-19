FROM python:3.12.7-alpine3.19

WORKDIR /app

COPY service.py /app/

RUN pip install Flask requests

EXPOSE 8199

CMD [ "python", "service.py" ]