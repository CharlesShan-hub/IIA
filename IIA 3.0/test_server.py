'''
import uuid
def get_mac_address(): 
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
    return ":".join([mac[e:e+2] for e in range(0,11,2)])
print(get_mac_address())
'''
import json

def load_json(path,encoding='UTF-8'):
    ''' 获取数据
    :param path: 数据集路径
    :param encoding(optional): 编码类型
    :return data: 获取的数据
    '''
    with open(path, 'r', encoding='UTF-8') as f:
        data = json.loads(f.read()[8:])
        #data = json.load(f)    #此时a是一个字典对象
    #logger.info("Load json - "+path)
    return data

print(load_json("./server/setting.json"))
