import exceptions
from classes.daemon import Daemon
from classes.databaseconnection import DatabaseConnection
from enums import PortMethod
from exceptions import PortNotFound
from classes.server import Server

min_port = 25510
max_port = 25599
def find_free_port(daemon:Daemon) -> int:
    connection = DatabaseConnection()
    ports = connection.find("SELECT (hostport) FROM ports WHERE deamon = %s", [daemon.id])
    connection.complete()
    for port in range(min_port,max_port):
        if not port in ports:
            return port
    raise exceptions.NoFreePorts

class Port:
    def __init__(self,containerport:int,serverport:int,method:PortMethod) -> None:
        self.containerport = containerport
        self.serverport = serverport
        self.method = method

    @classmethod
    def load_port(cls,daemon:Daemon,hostport:int) -> Port:
        connection = DatabaseConnection()
        data = connection.find("SELECT (containerport,method) FROM ports WHERE hostport = %s AND daemon = %s",[hostport,daemon.id])
        connection.complete()
        if data is None:
            raise PortNotFound("port not found")
        return cls(containerport=data[0],method=data[1],serverport=hostport)

    @classmethod
    def create_port(cls,daemon:Daemon,server:Server,containerport:int,method:PortMethod) -> Port:
        hostport = find_free_port(daemon=daemon)
        connection = DatabaseConnection()
        connection.add("INSERT INTO PORTS (daemon,server,containerport,hostport,method) VALUES (%s,%s,%s,%s,%s)",[daemon.id,server.id,containerport,hostport,method])
        connection.complete()
        return cls(containerport=containerport,serverport=hostport,method=method)

    def get_port(self) -> str:
        return F"{self.containerport}:{self.serverport}/{self.method}"