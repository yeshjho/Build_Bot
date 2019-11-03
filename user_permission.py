import pickle
from sys import maxsize
from texts import TEXT


DEVELOPER_ID = 353886187879923712


class UserPermission:
    DEFAULT_PERMISSION_LEVEL = 5
    DEVELOPER_LEVEL = maxsize
    BLACKLIST_LEVEL = -maxsize - 1

    def __init__(self, bot):
        self.permissions = {
            DEVELOPER_ID: self.DEVELOPER_LEVEL
        }
        self.bot = bot

    def get_permission_level(self, user_id):
        return self.permissions.get(user_id, self.DEFAULT_PERMISSION_LEVEL)

    def set_permission_level(self, user_id, level):
        if level == "blacklist":
            level = UserPermission.BLACKLIST_LEVEL
        elif level == "dev":
            level = UserPermission.DEVELOPER_LEVEL

        level = int(level)
        self.permissions[user_id] = level

        if level == self.DEFAULT_PERMISSION_LEVEL:
            del self.permissions[user_id]

        with open('permissions.pickle', 'wb') as permission_file:
            pickle.dump(self.bot.user_permission.permissions, permission_file)


class PERMISSIONS:
    COMMAND = {
        TEXT.COMMAND.COMMAND_HELP: UserPermission.BLACKLIST_LEVEL + 1,
        TEXT.COMMAND.COMMAND_COOLTIME: UserPermission.DEVELOPER_LEVEL,
        TEXT.COMMAND.COMMAND_VERSION: UserPermission.BLACKLIST_LEVEL + 1,
        TEXT.COMMAND.PERMISSION_OTHER: UserPermission.DEVELOPER_LEVEL,
        TEXT.COMMAND.COMMAND_ATTRIBUTE: UserPermission.DEVELOPER_LEVEL,
        TEXT.COMMAND.COMMAND_RELOAD: UserPermission.DEVELOPER_LEVEL
    }

    ATTRIBUTES = {}

    current_attribute = None
    with open("permission_attributes.txt", encoding='utf-8') as attribute_file:
        attribute_data = attribute_file.readlines()
    for line in attribute_data:
        line = line.replace('\n', '')
        if not line:
            continue

        if getattr(TEXT.ATTRIBUTES, line, None):
            current_attribute = getattr(TEXT.ATTRIBUTES, line)
            ATTRIBUTES[current_attribute] = {}
        else:
            key, value = line.split(":")
            ATTRIBUTES[current_attribute][int(key)] = int(value)

    ATTRIBUTES[TEXT.ATTRIBUTES.COOLTIME][UserPermission.DEVELOPER_LEVEL] = 0

    @staticmethod
    def set_attribute(attribute, key, value):
        PERMISSIONS.ATTRIBUTES[attribute][key] = value

        to_write = ""
        for attribute, dictionary in PERMISSIONS.ATTRIBUTES.items():
            to_write += attribute + '\n'
            for key, value in dictionary.items():
                to_write += str(key) + ": " + str(value) + '\n'
            to_write += '\n'
        with open("permission_attributes.txt", 'w', encoding='utf-8') as attribute_file:
            attribute_file.write(to_write)
