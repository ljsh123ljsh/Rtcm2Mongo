from re import findall
from re import search
class Map:
    def __init__(self, header, string):
        '''
        :param header: 匹配的标题头
        :param string: 需要匹配的文本
        '''
        self.string = string
        self.header = header
    def map_amount(self):
        '''
        :return: 返回匹配到的个数
        '''
        return len(findall(self.header, self.string))
    def map_first(self):
        '''
        :return: 匹配第一个的位置
        '''
        addr = search(self.header, self.string)
        return addr

    def map_id(self, add=True):
        '''
        :param add: 返回的index列表是否加1
        :return: 返回匹配的位置列表
        '''
        address = find_all(self.header, self.string)
        if add == True:
            return [c + 1 for c in address]
        else:
            return address


def find_all(sub, s):   # 匹配字符串位置
    index_list = []
    index = s.find(sub)
    while index != -1:
        index_list.append(index)
        index = s.find(sub, index + 1)
    if len(index_list) > 0:
        return index_list
    else:
        return [-1 ]