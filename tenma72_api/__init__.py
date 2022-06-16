from fastapi import FastAPI
import click
from uvicorn import Config

from .api_run import Server

app = FastAPI(docs_url="/")


@app.get("/testing")
def testing():
    return {"Hello": "World"}  # Error message


@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=8000)
@click.command()
def run(host, port):
    # loads the variables into the config
    config = Config("tenma72_api:app", host=host, port=port, log_level="info", workers=1)
    server = Server(config=config)  # calls the api_run files function

    with server.run_in_thread():  # runs the server until a keyboard interrupt
        while 1:
            pass
