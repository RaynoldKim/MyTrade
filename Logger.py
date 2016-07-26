from Singleton import  Singleton

class Logger(Singleton):

    def setCallback(self, callback):
        self.callback = callback

    def log(self, *varl):
        if self.callback != None:
            self.callback(varl)
        print(varl)