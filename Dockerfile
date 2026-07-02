FROM python:3.14-slim

RUN mkdir ./1ChatsDefender
COPY requirements.txt /1ChatsDefender

RUN python3 -m pip install --no-cache-dir --no-warn-script-location --upgrade pip \
&& python3 -m pip install --no-cache-dir --no-warn-script-location --user -r /1ChatsDefender/requirements.txt

COPY . /1ChatsDefender

WORKDIR /1ChatsDefender
CMD ["python3", "main.py"]
