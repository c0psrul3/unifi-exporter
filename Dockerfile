FROM python:3.7

RUN addgroup prometheus
RUN adduser --disabled-password --no-create-home --home /app  --gecos '' --ingroup prometheus prometheus

COPY requirements.txt /app/
COPY unifi/ /app/unifi/
COPY unifi_dump.py unifi_exporter.py /app/

RUN /usr/local/bin/pip3.7 install -r /app/requirements.txt

EXPOSE 9108

CMD ["/usr/local/bin/python",  "/app/unifi_exporter.py"]
