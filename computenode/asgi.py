from uvicorn import run
from argparse import ArgumentParser
from .app import app
from . import utils


argparser = ArgumentParser()
argparser.add_argument(
    '--proxy',
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
    HOST = "0.0.0.0"
    PORT = int(args.port)
    app.set_ip(utils.get_external_ip())
    app.set_port(PORT)
    if args.proxy:
        app.set_proxy(args.proxy)
    else:
        print("ERROR: Proxy IP not configured")
        return
    run(app, host=HOST, port=PORT)
