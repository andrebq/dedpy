import paho.mqtt.client as mqtt
import threading

class Bus:
    def __init__(self, rootPID=None, addr="127.0.0.1", port=1883):
        if not rootPID:
            raise ValueError('rootPID is required for any BUS instance')

        self.__mqc = mqtt.Client(client_id=rootPID, clean_session=False)
        self.__mqc.connect(addr, port)
        self.__mqc.on_connect = self.__bus_connected
        self.__connected = False
    
    def __bus_connected(self, *args):
        self.__connected = True
        print("Got connected", *args)
    
    
    def start_loop(self):
        self.__mqc.loop_start()
    
    def end_loop(self, timeout=60):
        msg = self.__mqc.disconnect()
        msg.wait_for_publish()
        self.__mqc.loop_end()
