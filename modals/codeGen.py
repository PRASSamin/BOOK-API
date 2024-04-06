import uuid

class UUIDGenerator:

    def __init__(self):
        self.uuid = uuid.uuid4()
    
    def __repr__(self):
        uuid_value = self.uuid
        uuid_string = str(uuid_value).replace('-', '')
        uid = ''.join(filter(str.isdigit, uuid_string))
        return uid
