from storage.logic import *

# 测试
#a = repository()
#a.creat_repo('newplace1',log=True)


# 创建新数据仓库
creat_new_repository(name='datalist',log=True)
creat_new_repository(name='bedelete',log=True)

# 拷贝数据仓库
creat_copy_repository(name='copy_bedelete',old_name='bedelete',log=True)
creat_copy_repository(name='copy_datalist',old_name='datalist',log=True)
creat_copy_repository(name='copy_datalist2',old_name='datalist',log=True)
creat_copy_repository(name='copy_datalist3.1',old_name='datalist',log=True)
creat_copy_repository(name='copy_datalist3.2',old_name='copy_datalist3.1',log=True)

# 删除数据仓库
delete_repositroy(name='bedelete',log=True)

