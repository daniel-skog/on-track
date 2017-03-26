FROM python:3-onbuild
CMD [ "python", "server/main.py" ]

EXPOSE 8080
