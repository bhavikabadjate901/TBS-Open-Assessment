import random
import bcrypt
from . import config
def RandomQuestions(QIDs, totalQuestions, reqNoQuestions):
    randomset = set()
    while(len(randomset) != reqNoQuestions):
        n = random.randint(0, totalQuestions - 1)
        l = QIDs[n]
        randomset.add(l)
    return list(randomset)

   
def encode_msg(msg):
    if type(msg) == str:
        msg = bytes(msg,'utf-8')
        return bcrypt.hashpw(msg,config.SALT).decode("utf-8")
    else:
        l = []
        for item in msg:
            msg1 = bytes(item,'utf-8')
            msg2 = bcrypt.hashpw(msg1,config.SALT).decode("utf-8")
            l.append(msg2)
        return l
    