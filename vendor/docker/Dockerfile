FROM		python:3.5.3-slim
MAINTAINER	David Sanders
RUN			apt-get update && \
			groupadd -r cowbull_g && \
			mkdir /cowbull && \
			useradd -r -G cowbull_g -d /cowbull cowbull && \
			chown cowbull /cowbull
WORKDIR		/cowbull
COPY		requirements.txt /cowbull
RUN		    pip install -q -r /cowbull/requirements.txt
USER		cowbull
ENV			PYTHONPATH="/cowbull"
COPY		Controller /cowbull/Controller/
COPY        InitializationPackage /cowbull/InitializationPackage/
COPY        app.py  /cowbull/
COPY        LICENSE /cowbull/
CMD			["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "app:app"]
EXPOSE		5000
