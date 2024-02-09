###########################################################
#
# ---%%%  Class SnptoolDbIterator: Handling sqlite3 functionality  %%%---
#

class SnptoolDbIterator(object):
    def __init__(self, cursor):
        self.c = cursor

    def __iter__(self):
        return self

    def __next__(self):
        if result := self.c.fetchone():        
            return [result[0], result[1], result[1]]
        else:
            raise StopIteration


