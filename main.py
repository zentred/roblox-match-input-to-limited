import requests

class Info:
    def __init__(self, item):
        self.input = item.lower()
        self.items = self.returnItems()
        self.nameToAcro = {}
        self.acroToName = {}
        self.fakeAcroToName = {}
        self.singleWord = {}
        self.idsToName = {}
        self.createDicts()
        self.findItem()

    def returnItems(self):
        return requests.get(
            'https://www.rolimons.com/itemapi/itemdetails'
        ).json()['items']

    def createDicts(self):
        toDelete = []
        for item in self.items:
            data = self.items[item]
            self.idsToName[item] = data[0].lower()
            if data[1] != '':
                self.nameToAcro[data[0].lower()] = data[1].lower()
                self.acroToName[data[1].lower()] = data[0].lower()
            else:
                if not data[0].count(' '):
                    self.singleWord[data[0].lower()] = None
                else:
                    name = data[0].lower()
                    for i in '`~!@#$%^&*()_-=+[]}{\/|;:,.<>?':
                        name = name.replace(i, '')
                    words = name.split(' ')
                    fakeAcro = ''
                    for word in words:
                        if word.isalpha() or word.isnumeric():
                            fakeAcro += word[0]
                    if fakeAcro in self.fakeAcroToName:
                        if fakeAcro not in toDelete:
                            toDelete.append(fakeAcro)
                    self.fakeAcroToName[fakeAcro] = data[0]
        for fakeAcro in toDelete:
            del self.fakeAcroToName[fakeAcro]

    def findItem(self):
        itemName, itemAcronym = None, None
        if self.idsToName.get(self.input) != None:
            itemName = self.idsToName[self.input]
            if self.nameToAcro.get(itemName) != None:
                itemAcronym = self.nameToAcro.get(itemName)
        else:
            if self.acroToName.get(self.input) != None:
                itemAcronym = self.input
                itemName = self.acroToName.get(self.input)
            elif self.nameToAcro.get(self.input) != None:
                itemName = self.input
                itemAcronym = self.nameToAcro.get(self.input)
            elif self.singleWord.get(self.input) != None:
                itemName = self.singleWord.get(self.input)
            elif self.fakeAcroToName.get(self.input) != None:
                itemName = self.fakeAcroToName.get(self.input)
            else:
                inputWords = self.input.split(' ')
                for item in self.items:
                    nameWords = self.items[item][0].lower().split(' ')
                    if len(set(inputWords)&set(nameWords)) == len(inputWords):
                        print(f'possible match: {self.items[item][0]}')
        
        if not itemName and not itemAcronym:
            print('unable to find a definite match')
        else:
            print(f'name: {itemName}    |    acronym: {itemAcronym}')


Info('rbm')
