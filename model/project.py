from sys import maxsize


class Project:

    def __init__(self, id=None, name=None, status="development", enabled="yes", inherit_global="yes",
                 view_status="public", description=None):
        self.id = id
        self.name = name
        self.status = status
        self.enabled = enabled
        self.inherit_global = inherit_global
        self.view_status = view_status
        self.description = description

    def __repr__(self):
        return "%s:%s:%s:%s:%s:%s" % (
            self.id, self.name, self.status, self.enabled, self.inherit_global, self.view_status)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name \
               and self.status == other.status and self.view_status == other.view_status

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
