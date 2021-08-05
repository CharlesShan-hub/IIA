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

# Community Mode - Run as a community server 
#SERVER_MODE = 'Community'

if __name__ == "__main__":
    if SERVER_MODE not in ['Local','Server','Client','Community']:
        exit()

    # Local Mode - Run as a Local software
    if SERVER_MODE == 'Local':
        server_thread = ServerThread(daemon=True)
        server_thread.start()
        ui.run()

    # Server Mode - Run server only
    if SERVER_MODE == 'Server':
        server_thread = ServerThread()
        server_thread.start()

    # Client Mode - Run client only
    if SERVER_MODE == 'Client':
        ui.run()

    # Community Mode - Run as a community server 
    if SERVER_MODE == 'Community':
        pass

    