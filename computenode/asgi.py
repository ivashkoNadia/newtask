from uvicorn import run
from argparse import ArgumentParser
from .app import app
from . import utils


argparser = ArgumentParser()
argparser.add_argument(
    '--local',
    action='store_true',
    help="Select to run on localhost or external NIC"
)
argparser.add_argument(
    '--proxy',
    required=True,
    action='store',
    help='IP address of proxy server'
)
argparser.add_argument(
    '--port',
    action='store',
    help='Select the port to run on (default 80)',
    default=80
)
args = argparser.parse_args()


def main():
    if args.local:
        HOST = "127.0.0.1"
    else:
        HOST = utils.get_external_ip()
    PORT = int(args.port)
    app.set_ip(HOST)
    app.set_port(PORT)
    app.set_proxy(args.proxy)
    run(app, host=HOST, port=PORT)
