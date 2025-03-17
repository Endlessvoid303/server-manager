from enum import Enum

class Software(Enum):
    VANILLA = "VANILLA"
    PAPER = "PAPER"
    PURPUR = "PURPUR"
    MAGMA = "MAGMA"

class Version(Enum):
    LATEST = "latest"

class PortMethod(Enum):
    TCP = "tcp"
    UDP = "udp"

class Permission(Enum):
    ADMIN = 10
    USER = 1
    BANNED = -1

class Actions(Enum):
    USER_ADD = 1
    USER_REMOVE = 2

class BorderColor(Enum):
    color_green = 65313
    color_red = 16711680
    color_orange = 11625728

class Channels(Enum):
    ACCOUNT_REQUEST_CHANNEL = 1350509785316982815