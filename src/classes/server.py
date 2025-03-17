from daemon import Daemon
from databaseconnection import DatabaseConnection
from exceptions import ServerNotFoundError
import config.port


class Server:
    def __init__(self,daemon:Daemon,server_id:int,server_uuid:str,name:str):
        self.daemon = daemon
        self.id = server_id
        self.uuid = server_uuid
        self.name = name

    @classmethod
    def load_server(cls,daemon:Daemon,server_id:int):
        connection = DatabaseConnection()
        data = connection.find("SELECT (daemon,uuid,name) FROM daemons WHERE id = %s",[server_id])
        if data is None:
            raise ServerNotFoundError("Server not found")
        if len(data) > 1:
            raise Exception("multiple servers found")
        if daemon.id != data[0][0]:
            raise Exception(f"deamons do not match: {data[0][0]}")
        connection.complete()
        return cls(daemon=daemon,server_id=server_id,server_uuid=data[0][1],name=data[0][2])

    @classmethod
    def create_server(cls,daemon:Daemon,server_uuid:str,name:str):
        connection = DatabaseConnection()
        server_id = connection.add("INSERT INTO servers (daemon,uuid,name) VALUES (%s,%s,%s)",[daemon,server_uuid,name])
        connection.complete()
        return cls(daemon,server_id,server_uuid,name)

    def get_ports(self):
        connection = DatabaseConnection()
        data = connection.find("SELECT (hostport) FROM ports WHERE deamon = %s", [self.daemon.id])
        ports:list[Port] = []
        for port in data:
            ports.append(Port.load_port(daemon=self.daemon,hostport=port[0]))
        return ports