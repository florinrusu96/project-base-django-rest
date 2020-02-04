FROM python:3.7-stretch
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app


ADD src /app/
ADD requirements.txt /app/
ADD docker-entrypoint.sh /app/

RUN pip install -r requirements.txt
EXPOSE 8080


RUN mkdir /app/static
RUN chgrp -R 0 /app/static
RUN chmod -R g+rwX /app/static

CMD /app/docker-entrypoint.sh
