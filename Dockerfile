FROM python:3.7
RUN pip install kopf kubernetes
ADD templates /src/templates
ADD nibbler.py /src/nibbler.py
CMD kopf run /src/nibbler.py --verbose