from consts import Consts 
import requests
import json
from collections import Counter
from spellcheck import Spellcheck 

class Data:
    def __init__(self):
        self.Refresh()
    
    def Refresh(self):
        self.pokemon = []
        self.items = []
        self.emblems = []
        self.uniqueNames = []
        self.uniqueItems = []
        self.uniqueEmblems = []
        self.autocompleteNames = []
        self.autocompleteItems = []
        self.autocompleteEmblems = []
        try:
            print(f"Getting Pokemon...")
            url = Consts.URI + "/pokemonunite/pokemon"
            response = requests.request("GET", url)
            self.pokemon = json.loads(response.text.encode('utf8'))
            self.uniqueNames = self.GetUniqueNames()
            self.autocompleteNames = self.GetAutoCompleteNames()
            
            print(f"Getting Items...")
            url = Consts.URI + "/pokemonunite/items"
            response = requests.request("GET", url)
            self.items = json.loads(response.text.encode('utf8'))
            self.uniqueItems = self.GetUniqueItems()
            self.autocompleteItems = self.GetAutoCompleteItems()

            print(f"Getting Emblems...")
            url = Consts.URI + "/pokemonunite/emblems"
            response = requests.request("GET", url)
            self.emblems = json.loads(response.text.encode('utf8'))
            self.uniqueEmblems = self.GetUniqueEmblems()
            self.autocompleteEmblems = self.GetAutoCompleteEmblems()
            
            print(f"Gathered Data!")
        except Exception as e:
            self.pokemon = []
            self.items = []
            self.emblems = []
            print(f"Failed to gather data! Exception: {e}")
    
    def GetUniqueNames(self):
        uniqueNames = []
        for val in self.pokemon:
            if(val["name"] not in uniqueNames):
                uniqueNames.append(val["name"].lower())
        
        return uniqueNames
    
    def GetUniqueItems(self):
        uniqueItems = []
        for val in self.items:
            if(val["name"] not in uniqueItems):
                uniqueItems.append(val["name"].lower())        
        
        return uniqueItems

    def GetUniqueEmblems(self):
        uniqueEmblems = []
        for val in self.emblems:
            if(val["name"] not in uniqueEmblems):
                uniqueEmblems.append(val["name"].lower()) 
        
        return uniqueEmblems

    def GetAutoCompleteNames(self):
        autocompleteNames = []
        for val in self.pokemon:
            if(val["name"] not in autocompleteNames):
                autocompleteNames.append(val["name"]) 
        
        return autocompleteNames

    def GetAutoCompleteItems(self):
        autoCompleteItems = []
        for val in self.items:
            if(val["name"] not in autoCompleteItems):
                autoCompleteItems.append(val["name"]) 
        
        return autoCompleteItems

    def GetAutoCompleteEmblems(self):
        autocompleteEmbs = []
        for val in self.emblems:
            if(val["name"] not in autocompleteEmbs):
                autocompleteEmbs.append(val["name"]) 
        
        return autocompleteEmbs
    
    def C(self, word): 
        names = Counter(self.uniqueNames)
        N = sum(names.values())
        return names[word] / N

    def nameCorrection(self, word): 
        return max(self.nameCandidates(word), key=self.C)

    def nameKnown(self, words): 
        return set(w for w in words if w in self.uniqueNames)
    
    def nameCandidates(self, word): 
        return (self.nameKnown([word]) or self.nameKnown(Spellcheck.edits1(word)) or self.nameKnown(Spellcheck.edits2(word)) or [word])

    def I(self, word): 
        names = Counter(self.uniqueItems)
        N = sum(names.values())
        return names[word] / N

    def itemCorrection(self, word): 
        return max(self.itemCandidates(word), key=self.I)

    def itemKnown(self, words): 
        return set(w for w in words if w in self.uniqueItems)
    
    def itemCandidates(self, word): 
        return (self.itemKnown([word]) or self.itemKnown(Spellcheck.edits1(word)) or self.itemKnown(Spellcheck.edits2(word)) or [word])

    def emblemCorrection(self, word): 
        return max(self.emblemCandidates(word), key=self.I)

    def emblemKnown(self, words): 
        return set(w for w in words if w in self.uniqueEmblems)
    
    def emblemCandidates(self, word): 
        return (self.emblemKnown([word]) or self.emblemKnown(Spellcheck.edits1(word)) or self.emblemKnown(Spellcheck.edits2(word)) or [word])
