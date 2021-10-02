from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Myuzik bot is up and running\n\n\n(Bot is currently online)\n[Made by github.com/sighclone and github.com/gud-will]"

def run():
  app.run(host='0.0.0.0',port=8080)

def keepalive():
    t = Thread(target=run)
    t.start()