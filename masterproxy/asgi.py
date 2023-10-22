from uvicorn import run
from argparse import ArgumentParser
from .app import app


argparser = ArgumentParser()

argparser.add_argument(
    '--port',
    action='store',
    help='Select the port to run on (default 80)',
    default=80
)
args = argparser.parse_args()

def main():
    HOST = "127.0.0.1"
    PORT = int(args.port)
    run(app, host=HOST, port=PORT)
