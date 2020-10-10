FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8025
COPY . .

CMD [ "python", "./mailfixer.py" ]
