FROM python:3.7.8-slim-buster

# Create python virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install apt dependencies
RUN apt-get clean
RUN apt-get update -y
RUN apt-get install python3 default-libmysqlclient-dev gcc -y

# Copy files into flask directory
WORKDIR /usr/src/flask_uuid
COPY . .
COPY app/main.py .

# Install pip dependencies
RUN pip install -r requirements.txt

# Run
CMD ["flask", "run", "--host=0.0.0.0"]

EXPOSE 5000

