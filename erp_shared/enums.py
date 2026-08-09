from enum import StrEnum


class RoleName(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class Action(StrEnum):
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    CHANGE_STATUS = "change_status"
