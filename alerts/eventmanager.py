
class EventManager:
    def __init__(self):
        self.observer = []
    def addObserver(self, observer):
        self.observer.append(observer)
    def removeObserver(self, observer):
        self.observer.remove(observer)
    def notifyObservers(self,event):
        for observer in self.observer:
            observer.update(event)