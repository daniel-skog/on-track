FROM python:3-onbuild
CMD [ "python", "server/main.py" ]

ENV PYTHONPATH /usr/src/app/server

EXPOSE 8080
