import threading
import server
import ui

class ServerThread(threading.Thread):
    def __init__(self,daemon=False):
        threading.Thread.__init__(self,daemon=daemon)
    def run(self):
        server.run()


''' IIA - Intelligent Information Assistant
    This is the main file.
'''
# Local Mode - Run as a Local software
#SERVER_MODE = 'Local'
# Server Mode - Run server only
SERVER_MODE = 'Server'
# Client Mode - Run client only
#SERVER_MODE = 'Client'

if __name__ == "__main__":
    if SERVER_MODE == 'Local':
        server_thread = ServerThread(daemon=True)
        server_thread.start()
    if SERVER_MODE == 'Server':
        server_thread = ServerThread()
        server_thread.start()
    if SERVER_MODE == 'Local' or SERVER_MODE == 'Client':
        ui.run()

    