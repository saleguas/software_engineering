# FROM nikolaik/python-nodejs:python3.6-nodejs17
# # We copy just the requirements.txt first to leverage Docker cache
# COPY ./src/requirements.txt /app/requirements.txt

# WORKDIR /app

# RUN pip3 install -r requirements.txt

# ADD ./src/pythonr /app/pythonr
# ADD ./src/coins /app/coins

# ENV PYTHONPATH "${PYTHONPATH}:/app/coins"

# EXPOSE 5000

# RUN cd "/app/pythonr/"


# CMD ["flask", "run", "--host=0.0.0.0" ]

# above is test

FROM python:3.8.12



# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt


# NEED TO CHANGE THIS

ADD ./src /app/src

ENV PYTHONPATH "${PYTHONPATH}:/app/src"

EXPOSE 5000
WORKDIR /app
RUN pip3 install -r requirements.txt


# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000" ]
CMD ["python", "app.py" ]
