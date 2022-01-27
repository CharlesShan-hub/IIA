def reply_maker(code):
    return '{"reply":"'+str(code)+'"}'


def get_host_ip():
    """
    get host ip
    :return: ip
    """
    import socket
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    except:
        ip='127.0.0.1'
    finally:
        s.close()

    return ip

def get_host_port():
    import os
    import random
    pscmd = "netstat -ntl |grep -v Active| grep -v Proto|awk '{print $4}'|awk -F: '{print $NF}'"
    procs = os.popen(pscmd).read()
    procarr = procs.split("\n")
    tt= random.randint(1024,49151)#服务端口号
    #tt = 12345
    if tt not in procarr:
        return tt
    else:
        return get_host_port()


def write_json(path, content, encoding='UTF-8'):
    ''' json写入数据
    '''
    import json
    #logger.info("Write json - "+path)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(content, indent=4, ensure_ascii=False))
