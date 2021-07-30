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
if __name__ == "__main__":
    server_thread = ServerThread(daemon=True)
    server_thread.start()
    ui.run()

    