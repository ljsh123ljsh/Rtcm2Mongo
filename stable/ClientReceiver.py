from stable.Tool import bin2ascii as ba
class ClientReceiver:
    def __init__(self, data):
        self.data = data
        try:
            self.amount = int(data[:12], base=2)
        except ValueError:
            self.amount = 0
    def Getcontent(self):
        self.__end = 12 + self.amount * 8
        content_b = self.data[12: self.__end]
        content = ba(content_b)
        return content
    def Restcontent(self):
        return self.data[self.__end:]