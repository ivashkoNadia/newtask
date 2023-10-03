class Server:
    def __init__(self, id=None, ip=None, port=None, status=None):
        self.id = id
        self.ip = ip
        self.port = port
        self.status = status

class User:
    def __init__(self, email, password):
        self.id = None
        self.email = email
        self.password = password

   
class Task:
    def __init__(self, id=None, user_id=None, server_id=None, status=None, error=None, progress=None, input_data=None, output_data=None):
        self.id = id
        self.user_id = user_id
        self.server_id = server_id
        self.status = status
        self.error = error
        self.progress = progress
        self.input_data = input_data
        self.output_data = output_data
