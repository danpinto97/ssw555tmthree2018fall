class Family:
    def __init__(self, id):
        self.id = id
        self.married = ""
        self.divorced = ""
        self.husband_id = ""
        self.husband_name = ""
        self.wife_id = ""
        self.wife_name = ""
        self.children = []

    #set var names
    def setMarried(self, married):
        self.married = married
    
    def setDivorced(self, divorced):
        self.divorced = divorced

    def setHusbandID(self, husband_id):
        self.husband_id = husband_id

    def setHusbandName(self, husband_name):
        self.husband_name = husband_name

    def setWifeID(self, wife_id):
        self.wife_id = wife_id

    def setWifeName(self, wife_name):
        self.wife_name = wife_name

    def addChild(self, child):
        #list in case multiple families, idk
        self.children.append(child)

    #get var names
    def getID(self):
        return self.id
    
    def getMarried(self):
        return self.married

    def getDivorced(self):
        if len(self.divorced) < 1:
            return "N/A"
        return self.divorced
    
    def getHusbandID(self):
        if len(self.husband_id) < 1:
            return "N/A"
        return self.husband_id
    
    def getHusbandName(self):
        if len(self.husband_name) < 1:
            return "N/A"
        return self.husband_name
    
    def getWifeID(self):
        if len(self.wife_id) < 1:
            return "N/A"
        return self.wife_id
    
    def getWifeName(self):
        if len(self.wife_name) < 1:
            return "N/A"
        return self.wife_name

    def getChild(self):
        if len(self.children) < 1:
            return "N/A"
        return self.children