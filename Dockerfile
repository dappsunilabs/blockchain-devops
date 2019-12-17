# docker build -t blockchain_bot .
#docker run -d -p 5001:5001 blockchain_bot

FROM python:3

WORKDIR /usr/src/app

# Bundle app source
COPY . .

RUN pip install -r requirements.txt

EXPOSE 5001

CMD [ "env", "FLASK_APP=main.py", "flask", "run" ,"--host", "0.0.0.0", "--port", "5001"]
