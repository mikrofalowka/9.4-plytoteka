import json


class Plytoteka:
    def __init__(self):
        ''' przy tworzeniu instancji, probuje odczytac dane z pliku plytoteka.json i przypisac je do atrybutu self.plytoteka
        jesli nie ma takiego pliku to tworzy pusta liste w atrybucie'''
        try:
            with open("plytoteka.json", "r") as f:
                self.plytoteka = json.load(f)
        except FileNotFoundError:
            self.plytoteka = []

    def all(self):
        '''zwraca liste'''
        return self.plytoteka

    def get(self, id):
        '''zwraca element o indeksie id'''
        plyta = [plyta for plyta in self.all() if plyta['id']==id]
        if plyta:
            return plyta[0]
        return []

    def create(self, data):
        '''najpierw zrzuca z data klucz csrf_token
        a reszte do self.plytoteka'''
        self.plytoteka.append(data)
        self.save_all()
    
    def delete(self, id):
        plyta = self.get(id)
        if plyta:
            self.plytoteka.remove(plyta)
            self.save_all()
            return True
        return False

    def save_all(self):
        '''zrzuca liste do formatu json '''
        with open("plytoteka.json", "w") as f:
            json.dump(self.plytoteka, f)

    def update(self, id, data):
        '''nadpisuje w liscie element <id> a nastepnie wywoluje metode save_all()'''
        plyta = self.get(id)
        if plyta:
            index = self.plytoteka.index(plyta)
            self.plytoteka[index] = data
            self.save_all()
            return True
        return False


plytoteka = Plytoteka()