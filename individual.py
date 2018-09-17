class Individual:
    #init
    def __init__(self, id):
        self.id = id
        self.name = "Unknown"
        self.gender = ""
        self.birthday = "Unknown"
        self.age = 0
        self.alive = True
        self.death = "N/A"
        self.child = []
        self.spouse = []
    #set var names
    def setName(self, name):
        self.name = name
    
    def setGender(self, gender):
        self.gender = gender

    def setBirthday(self, birthday):
        print(self.name)
        self.birthday = birthday

    def setAge(self, age):
        self.age = age

    def setAlive(self, alive):
        self.alive = alive

    def setDeath(self, death):
        self.death = death

    def addSpouse(self, spouse):
        #list in case multiple families, idk
        self.spouse.append(spouse)
    
    def addChild(self, child):
        #list in case multiple families, idk
        self.child.append(child)
    #get var names
    def getID(self):
        return self.id

    def getName(self):
        return self.name
    
    def getGender(self):
        return self.gender

    def getBirthday(self):
        return self.birthday
    
    def getAge(self):
        return self.age
    
    def getAlive(self):
        return self.alive
    
    def getDeath(self):
        if len(self.death) < 1:
            return "N/A"
        return self.death
    
    def getChild(self):
        return self.child

    def getSpouse(self):
        return self.spouse