import logger
import storage

""" Init
"""

LOG_MODULE = 'Warehouse'


""" Class
"""

class Warehouse():
    """高级仓库
    exist_warehouse:     高级仓库是否被创建
    creat_warehouse:     创建高级仓库
    creat_base_repo:     创建子低级仓库
    exist_base_repo:     是否拥有(可访问)子低级仓库
    add_base_repo:       添加子低级仓库(允许访问已经有的某低级仓库)
    operation_base_repo: 对某子低级仓库进行操作
    """
    def __init__(self, **kwg):
        # 保存初始化变量 # 需要有 name,mail
        self.kwg = kwg
        # 状态变量
        self.real=self.exist_warehouse()
        # 高级仓库的低级仓库包含表
        self.base_list=[]
        # 高级仓库的附加函数包含表
        self.addition_function={}

    def exist_warehouse(self):
        import setting
        return self.kwg['name'] in setting.get(["General",self.kwg['mail'],"repository","high"])

    def creat_warehouse(self):
        if self.real==True:
            return False
        import setting
        setting.add(["General",self.kwg['mail'],"repository","high"],\
            {self.kwg['name']:{
                "visit_list":[self.kwg['mail']],
                "base":[]
            }})
        self.real=True

    def exist_base_repo(self,name):
        if self.real==False: return False
        import setting
        return name in setting.get(["General",self.kwg['mail'],"repository","high",self.kwg['name'],"base"])

    def creat_base_repo(self,name):
        if self.real==False: return False
        storage.creat_repository(name=name,mail=self.kwg['mail'])
        import setting
        setting.add(["General",self.kwg['mail'],"repository","high",self.kwg['name'],"base"],name)
        return True

    def add_base_repo(self,name):
        if self.real==False: return False
        if storage.exist_repository(name=name,mail=self.kwg['mail'])==False:
            return False
        import setting
        setting.add(["General",self.kwg['mail'],"repository","high",self.kwg['name'],"base"],name)
        return True

    def operation_base_repo(self,name,con):
        if self.real==False: return False
        if storage.exist_repository(name=name,mail=self.kwg['mail'])==False:
            return False
        return storage.operation(name=name,mail=self.kwg['mail'],con=con)

    def set_fun(self,fun):
        self.addition_function[fun.__name__]=fun

    def run_fun(self,fun_name,**kwg):
        self.addition_function[fun_name](self,**kwg)

class SheetWarehouse(Warehouse):
    """ 表格仓库
    用于存放数据结构清晰的数据表
    """
    def __init__(self, **arg):
        super(SheetWarehouse, self).__init__()
        self.arg = arg

    # 创建表格仓库
    def creat(self):
        if storage.exist_repository(self.arg['name'])==True:
            logger.warning("Creat - "+self.arg['name']+" - Has Created",LOG_MODULE)
            return False
        storage.creat_repository(name=self.arg['name'],user_id=self.arg['user_id'])
        con = 'INSERT INTO SheetWarehouse (NAME,MAIL) VALUES (\''+self.arg['name']+'\',\''+self.arg['user_id']+'\')'
        storage.add_info(name='Warehouse',con=con)
        logger.info("Creat new SheetWarehouse - "+self.arg['name'],LOG_MODULE)

    # 配置表格仓库
    def config(self):
        pass

    # 删除表格仓库
    def delete(self):
        pass

    # 备份表格仓库
    def copy(self):
        pass

    # 指定仓库覆盖
    def recover(self):
        pass

    # 添加数据表
    def add_sheet(self):
        pass

    # 检查数据表信息
    def info_sheet(self):
        pass

    # 执行具体指令
    def execute(self,con):
        if storage.exist_repository(self.arg['name'])==False:
            logger.warning("Execute - "+self.arg['name']+" - Not Exist",LOG_MODULE)
            return False
        storage.test_add_info(name=self.arg['name'],con=con)
        logger.info("Execute - "+self.arg['name'],LOG_MODULE)
    

class PictureWareHouse(Warehouse):
    """ 图片仓库
    用于存放图片的数据表
    """
    def __init__(self, *arg):
        super(PictureWareHouse, self).__init__()
        #self.arg = arg


class TimeWarehouse(Warehouse):
    """ 时间数据仓库
    用于与时间相关的数据表
    包含子更新功能的数据；任务进度；时间安排等等
    """
    def __init__(self, *arg):
        super(TimeWarehouse, self).__init__()
        #self.arg = arg


def _test_show_info(name,con):
    ''' 查改成员信息
    *没有添加各种容错
    '''
    logger.info("Getting all user info!",LOG_MODULE)
    info=storage.add_info(name=name,con=con)
    return info
