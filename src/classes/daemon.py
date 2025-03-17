from exceptions import DaemonNotFound
from databaseconnection import DatabaseConnection


class Daemon:
    def __init__(self,daemon_id:int,uuid:str,ip:str,name:str):
        self.id = daemon_id
        self.uuid = uuid
        self.ip = ip
        self.name = name

    @classmethod
    def load_daemon(cls,daemon_id:int):
        connection = DatabaseConnection()
        data = connection.find("SELECT (uuid,ip,name) FROM daemons WHERE id = %s",[daemon_id])
        if data is None:
            raise DaemonNotFound("daemon not found")
        if len(data) > 1:
            raise exception("multiple daemons found")
        return cls(daemon_id,data[0][0],data[0][1],data[0][2])

    @classmethod
    def create_daemon(cls,uuid:str,ip:str,name:str):
        connection = DatabaseConnection()
        daemon_id = connection.add("INSERT INTO daemons (uuid,ip,name) VALUES (%s,%s,%s)",[uuid,ip,name])
        connection.complete()
        return cls(daemon_id,uuid,ip,name)