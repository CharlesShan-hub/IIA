import ui
# UI测试仅用于测试布局, 外观等问题, 无法进行数据交互

# Login page
ui.test_run('/ui/html/login.html',TEST_MODE=False,CON_OPEN_WIN=True)

# Main page
#ui.test_run('/ui/html/main/glxy.html')

# Test page
#ui.test_run('/ui/html/index.html')