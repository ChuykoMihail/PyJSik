class Token:
    def __init__(self, val, type, pos):
        self.value = val
        self.type = type
        self.position = pos

    def setPosition(self, mposition):
        self.position = mposition

    def setType(self, mtype):
        self.type = mtype

    def setValue(self, mvalue):
        self.value = mvalue


