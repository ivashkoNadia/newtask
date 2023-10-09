import socket


def validate_input_data(input_data) :
    return True


def validate_method(method: str) -> bool:
    return True


def get_external_ip():
    hostname = socket.gethostname()
    external_ip = socket.gethostbyname(hostname)
    return external_ip
