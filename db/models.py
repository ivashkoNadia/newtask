from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from json import loads

Base = declarative_base()
class Node(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String)
    port = Column(Integer)
    status = Column(String)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    password = Column(String)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    node_id = Column(Integer)
    status = Column(String, default="pending")
    error = Column(String, default=None)
    progress = Column(Integer, default=0)
    input_data = Column(String)
    output_data = Column(String, default=None)

    def get_input_data(self):
        return loads(self.input_data)

    def get_output_data(self):
        return loads(self.output_data)
    #
    # @property
    # def input_data(self):
    #     # Deserialize the JSON string to a Python object
    #     return json.loads(self.input_data_json)
    #
    # @input_data.setter
    # def input_data(self, value):
    #     # Serialize the Python object to a JSON string
    #     self.input_data = json.dumps(value)
    #
    # @property
    # def output_data(self):
    #     # Deserialize the JSON string to a Python object
    #     return json.loads(self.output_data_json)
    #
    # @output_data.setter
    # def output_data(self, value):
    #     # Serialize the Python object to a JSON string
    #     self.output_data = json.dumps(value)