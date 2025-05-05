'''
    Check Path and File existence
'''
# Folders
if os.path.exists('./show') == False:
    os.makedirs('./show')
# Files
#if os.path.exists("./show/setting.json") == False:
#    import setting
#    setting.initialize("./show/setting.json",content)


class Block():
	def __init__(self):
		# 展示框长度与高度
		self.width = None
		self.heigth= None

class Number(Block):
	def __init__(self):
		super(Number,self).__init__()
		self.

a = Number()
a.width = 3
a.heigth = 4
print(a.width)

'''
<div class="col-xl-3 col-md-6">
    <div class="card mini-stat bg-primary text-white">
        <div class="card-body">
            <div class="mb-4">
                <div class="float-left mini-stat-img mr-4">
                    <img src="assets/images/services-icon/01.png" alt="">
                </div>
                <h5 class="font-size-16 text-uppercase mt-0 text-white-50">Orders</h5>
                <h4 class="font-weight-medium font-size-24">1,685 <i
                        class="mdi mdi-arrow-up text-success ml-2"></i></h4>
                <div class="mini-stat-label bg-success">
                    <p class="mb-0">+ 12%</p>
                </div>
            </div>
            <div class="pt-2">
                <div class="float-right">
                    <a href="#" class="text-white-50"><i class="mdi mdi-arrow-right h5"></i></a>
                </div>

                <p class="text-white-50 mb-0 mt-1">Since last month</p>
            </div>
        </div>
    </div>
</div>
'''