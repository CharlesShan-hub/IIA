import threading
import server
import ui

class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        server.run()

if __name__ == "__main__":
	server_thread = ServerThread()
	server_thread.start()
	ui.run()