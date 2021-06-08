from storage.logic import *

# 测试
#a = repository()
#a.creat_repo('newplace1',log=True)


# 创建新数据仓库
creat_new_repository(name='datalist')
creat_new_repository(name='bedelete')

# 拷贝数据仓库
creat_copy_repository(name='copy_bedelete',old_name='bedelete')
creat_copy_repository(name='copy_datalist',old_name='datalist')
creat_copy_repository(name='copy_datalist2',old_name='datalist')
creat_copy_repository(name='copy_datalist3.1',old_name='datalist')
creat_copy_repository(name='copy_datalist3.2',old_name='copy_datalist3.1')
