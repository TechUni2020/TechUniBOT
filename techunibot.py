import discord
from flask import Flask, request, jsonify
from multiprocessing import Process

from techuni_flask import app as flask_app

app = Flask(__name__)
app.register_blueprint(flask_app)

def run_flask():
    app.run()

def run_discord():
    pass

if __name__ == "__main__":
    flask_process = Process(target=run_flask)
    discord_process = Process(target=run_discord)

    # process start
    flask_process.start()
    discord_process.start()

    # process join(終了待ち)
    flask_process.join()
    discord_process.join()
