FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y --no-install-recommends && rm -rf /var/lib/apt/lists/* && pip install --upgrade pip
RUN mkdir code
WORKDIR /code
COPY package.txt /code/
COPY . /code/
RUN pip3 install -r package.txt
RUN export LC_ALL=C
EXPOSE 8089
