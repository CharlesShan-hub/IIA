import logger
import storage

LOG_MODULE = 'Warehouse'

if storage.exist_repository("Warehouse")==False:
    storage.creat_repository(name='Warehouse',user_id='System')
    # 高结构数据仓库存储信息表：数据仓库名称(数据仓库名称与仓库名称相同)-用户
    con_table = '''CREATE TABLE SheetWarehouse (NAME TEXT PRIMARY KEY NOT NULL, MAIL TEXT)'''
    storage.add_info(name='Warehouse',con=con_table)

class Warehouse(object):
    """面向具体功能的存储模块
    """
    def __init__(self, *arg):
        super(Warehouse, self).__init__()
        self.arg = arg
        # 检查仓库信息
        #...
        self.init_info_repo()

    def init_info_repo(self):
        pass

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
