FROM python:slim-buster


COPY . /application/
RUN pip3 install -r /application/requirements.txt

ENTRYPOINT ["/application/package_statistics.py"]

