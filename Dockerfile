FROM python:3

RUN pip3 install redis
COPY ./main.py /

EXPOSE 65432
ENTRYPOINT ["python", "main.py"]