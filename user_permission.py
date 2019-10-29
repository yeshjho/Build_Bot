import pickle
from texts import TEXT


DEVELOPER_ID = 353886187879923712


class UserPermission:
    DEFAULT_PERMISSION_LEVEL = 5
    DEVELOPER_LEVEL = 10
    BLACKLIST_LEVEL = 0

    def __init__(self, bot):
        self.permissions = {
            DEVELOPER_ID: self.DEVELOPER_LEVEL
        }
        self.bot = bot

    def get_permission_level(self, user_id):
        return self.permissions.get(user_id, self.DEFAULT_PERMISSION_LEVEL)

    def set_permission_level(self, user_id, level):
        self.permissions[user_id] = level

        with open('permissions.pickle', 'wb') as permission_file:
            pickle.dump(self.bot.user_permission.permissions, permission_file)


class PERMISSIONS:
    COMMAND = {
        TEXT.COMMAND.COMMAND_COOLTIME: UserPermission.DEVELOPER_LEVEL,
        TEXT.COMMAND.COMMAND_VERSION: 1,
        TEXT.COMMAND.COMMAND_PERMISSION: UserPermission.DEVELOPER_LEVEL
    }

    COOLTIME_IN_MIN = {
        UserPermission.DEVELOPER_LEVEL: 0,
        9: 0,
        8: 1,
        7: 3,
        6: 5,
        4: 13,
        3: 20,
        2: 30,
        1: 60
    }
