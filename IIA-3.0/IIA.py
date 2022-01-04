''' Parameter Settings
''' 
# Connect Local Server
#CON_CONNECT_LOCAL = True
CON_OPEN_WIN = True # open IIA in a window
CON_OPEN_WEB = True # open IIA in web browser
CON_SHARE = True # other computer can log in by LAN
CON_TEST_MODE = False # Run in test mode
CON_80_PORT = True # Default run on 80 port
# Related HTML file entry path
HTML_PATH = "/ui/html/login.html"
TEST_PATH = "/ui/html/test.html"

''' Operation Mode
    `sudo python3 IIA.py` - IIA Start
    `sudo python3 /Users/kimshan/workplace/IIA/IIA-3.0/IIA.py` - IIA Start
    `sudo python3 IIA.py test` - IIA test mode
    `sudo python3 IIA.py clear` - clear cache(log.txt)
'''
if __name__ == "__main__":
    import sys
    import os
    # Clear Cache Option
    path_cd = os.path.split(sys.argv[0])[0]
    if path_cd != "":
        os.chdir(os.path.split(sys.argv[0])[0])
    if(len(sys.argv)>1 and sys.argv[1]=='clear'):
        with open("./logger/log.txt",'w'):
            print("Clear log and caches!")
        sys.exit()

    # Test Mode
    if(len(sys.argv)>1 and sys.argv[1]=='test'):
        print("Open Test Mode!")
        CON_TEST_MODE = True

    # Open Server and ShareThread
    import server
    import ui

    server_thread = server.ServerThread(daemon=True)
    server_thread.start()
    
    ui.run(HTML_PATH,TEST_PATH,CON_TEST_MODE,CON_OPEN_WIN,\
        CON_OPEN_WEB, CON_SHARE, CON_80_PORT)
