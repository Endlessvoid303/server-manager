from __future__ import annotations

import enums
import exceptions
import mcs.mcsapi
from classes.databaseconnection import DatabaseConnection


class User:
    def __init__(self,user_id:int,discord_id:int,mcs_id:str,name:str):
        self.user_id = user_id
        self.discord_id = discord_id
        self.mcs_id = mcs_id
        self.name = name

    @classmethod
    def load_user(cls,user_id:int) -> User:
        connection = DatabaseConnection()
        data = connection.find("SELECT mcsID,discordID,name FROM users WHERE id = %s",[user_id])
        connection.complete()
        if len(data) == 0:
            raise Exception("user not found")
        if len(data) > 1:
            raise Exception("multiple users found")
        userdata = data[0]
        return cls(user_id=user_id, discord_id=userdata[1], mcs_id=userdata[0],name=userdata[2])

    @classmethod
    def load_user_by_name(cls,name:str) -> User:
        connection = DatabaseConnection()
        data = connection.find("SELECT mcsID,discordID,id,name FROM users WHERE name = %s", [name])
        connection.complete()
        if len(data) == 0:
            raise Exception("user not found")
        if len(data) > 1:
            raise Exception("multiple users found")
        userdata = data[0]
        return cls(user_id=userdata[2], discord_id=userdata[1], mcs_id=userdata[0],name=userdata[3])

    @classmethod
    def create_user(cls,discord_id:int,username:str,password:str) -> User:
        response = mcs.mcsapi.add_user(username,password,enums.Permission.BANNED.value)
        if response["data"] == "Username is already in use":
            raise exceptions.UserExistsError
        mcs_id = response["data"]["uuid"]
        connection = DatabaseConnection()
        user_id = connection.add("INSERT INTO users (name,mcsID,discordID,permission,isReviewed) VALUES (%s,%s,%s,%s,%s)",[username,mcs_id,discord_id,enums.Permission.BANNED.value,False])
        connection.complete()
        return cls(user_id=user_id,discord_id=discord_id,mcs_id=mcs_id,name=username)

    def delete(self) -> None:
        mcs.mcsapi.delete_user(self.mcs_id)
        connection = DatabaseConnection()
        rowcount = connection.execute("DELETE FROM users WHERE id = %s",[self.user_id])
        if rowcount == 0:
            raise exceptions.UserDoesNotExistError
        elif rowcount > 1:
            raise Exception("multiple users found")
        else:
            connection.complete()
        # Unfortunatly we can't remove the class instance.
        # class instance is removed when not used, wich is after the user is deleted

    def has_user_been_reviewed(self) -> bool:
        connection = DatabaseConnection()
        data = connection.find("SELECT (isReviewed) FROM users WHERE id = %s", [self.user_id])
        is_reviewed = data[0][0]
        connection.complete()
        return is_reviewed == 1

    def not_reviewed(self):
        if self.has_user_been_reviewed():
            raise exceptions.UserAlreadyReviewedError

    def get_permission(self) -> enums.Permission:
        self.not_reviewed()
        connection = DatabaseConnection()
        permnum = connection.find("SELECT (permission) FROM users WHERE id = %s", [self.user_id])[0][0]
        connection.complete()
        return enums.Permission(permnum)

    def set_permission(self,permission:enums.Permission) -> None:
        connection = DatabaseConnection()
        connection.execute("UPDATE users SET permission = %s WHERE id = %s",[permission.value, self.user_id])
        connection.complete()

    def allow_user(self) -> None:
        if self.has_user_been_reviewed():
            raise exceptions.UserAlreadyReviewed
        connection = DatabaseConnection()
        self.set_permission(enums.Permission.USER)
        connection.execute("UPDATE users SET isReviewed = TRUE WHERE id = %s",[self.user_id])
        connection.complete()

    def block_user(self) -> None:
        connection = DatabaseConnection()
        self.set_permission(enums.Permission.BANNED)
        if not self.has_user_been_reviewed():
            connection.execute("UPDATE users SET isReviewed = TRUE WHERE id = %s", [self.user_id])
        connection.complete()

    def unblock_user(self) -> None:
        self.not_reviewed()
        if not self.get_permission() == enums.Permission.BANNED:
            raise exceptions.UserNotBlocked
        self.set_permission(enum.Permission.USER)
