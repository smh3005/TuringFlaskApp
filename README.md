# Overview

# Production Notes

We deploy this project using gunicorn inside a docker container specified by the dockerfile. (We map port 443 to exposed port 8000 in the docker container). The deployment process is handled by the docker-compose.yaml file. To deploy, run 
```
docker-compose up
```

Note. You'll need a signed ssl certificate (.crt) file and ssl key (.key) file in the project directory in order to run gunicorn in https mode. If you don't want to generate those files and/or run gunicorn in http mode, change 

```
    command: sh -c "pip install -r requirements.txt && gunicorn --certfile=theturinggames.crt --keyfile=theturinggames.key -b 0.0.0.0:8000 -w 4 app.wsgi:app"
``` 
in docker-compose.yaml to 
```
    command: sh -c "pip install -r requirements.txt && gunicorn -b 0.0.0.0:8000 -w 4 app.wsgi:app"
```

and change 
```
ports:
    - "443:8000"
```
to 
```
ports:
    - "80:8000"
```