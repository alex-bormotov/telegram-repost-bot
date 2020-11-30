FROM python:3.9.0-slim-buster
ENV LD_LIBRARY_PATH /usr/local/lib
WORKDIR /telegram-repost-bot
COPY . /telegram-repost-bot
RUN pip3 install -r requirements.txt --no-cache-dir
CMD [ "python3", "./app.py" ]
