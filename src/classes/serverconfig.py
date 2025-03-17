from classes.databaseconnection import DatabaseConnection
from enums import Software, Version
from classes import port
from classes.server import Server
class ServerConfig:
    def __init__(self, server_id:int, name:str, memory:int, software:Software, version:Version, ports:list[port]):
        self.memory = memory
        self.type = software
        self.version = version
        self.name = name
        self.ports = ports
        self.id = server_id

    @classmethod
    def load_config(cls,server:Server):
        connection = DatabaseConnection()
        data = connection.find("SELECT (memory,servertype,version) FROM serverconfig WHERE id = %s",[server.id])
        connection.complete()
        return cls(server_id=server.id, name=server.name, memory=data[0], software=data[1], version=data[2], ports=server.get_ports())

    @classmethod
    def create_config(cls, name:str, memory:int, software:Software, version:Version, ports:list[port]):
        connection = DatabaseConnection()
        server_id = connection.add("INSERT INTO serverconfig (memory,software,version) VALUES (%s,%s,%s)", [memory, software, version])
        connection.complete()
        return cls(server_id=server_id, name=name, memory=memory, software=software, version=version, ports=ports)

    def get_config(self):
        env_vars = [
            "EULA=TRUE",
            F"MAX_MEMORY={self.memory}g",
            "ENABLE_AUTOSTOP=TRUE",
            "AUTOSTOP_TIMEOUT_EST=300",
            "AUTOSTOP_TIMEOUT_INIT=600",
            "TZ=CET",
            F"TYPE={self.type}",
            F"VERSION={self.version}"
        ]
        data = {
            "nickname" :self.name,
            "startCommand": "",
            "stopCommand": "stop",
            "cwd": ".",
            "ie": "utf-8",
            "oe": "utf-8",
            "processType": "docker",
            "type": "minecraft/java",
            "tag": ["hosted"],
            "endTime": "",
            "docker": {
                "containerName": "",
                "image": "itzg/minecraft-server",
                "ports": self.ports,
                "extraVolumes": [],
                "networkMode": "bridge",
                "networkAliases": [],
                "cpusetCpus": "",
                "maxSpace": 0,
                "workingDir": "/data/",
                "env": env_vars
            }
        }
        return data