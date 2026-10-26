FROM python:3.12-slim

# Install dependencies.
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

CMD python ./nowplay.py