import paho.mqtt.client as mqtt
import threading
import pid
import json
import wx

_busMessage = wx.NewEventType()
EVT_NEW_MESSAGE = wx.PyEventBinder(_busMessage, 1)


class Bus:
    def __init__(self, addr="127.0.0.1", port=1883):
        busPID = pid.random_pid()
        self.__buspid = busPID

        self.__mqc = mqtt.Client(client_id=str(busPID), clean_session=False)
        self.__mqc.connect(addr, port)
        self.__mqc.on_connect = self.__bus_connected
        self.__mqc.on_disconnect = self.__bus_disconnected
        self.__mqc.on_message = self.__bus_new_message
        self.__connected = False
        self.__connected_lock = threading.Lock()

    def publish_json(self, topic, payload_object):
        self.__mqc.publish(topic, json.dumps(payload_object))

    def watch_all_pids(self, callback):
        self.__mqc.message_callback_add("pid/#", callback)

    def watch_pid(self, pid, callback=None):
        if callback:
            self.__watch_pid_msg_callback(pid, callback)
        else:
            self.__mqc.subscribe(pid.topic(["#"]), qos=0)

    def __watch_pid_msg_callback(self, pid, callback):
        self.__mqc.message_callback_add(pid.topic(["#"]), callback)

    def __bus_new_message(self, client, userdata, message):
        print(f"Got: {message}")

    def __bus_connected(self, *args):
        self.__connected_lock.acquire()
        self.__connected = True

    def __bus_disconnected(self, *args):
        self.__connected_lock.release()
        self.__connected = False

    def start_loop(self):
        self.__mqc.loop_start()

    def end_loop(self, timeout=60):
        msg = self.__mqc.disconnect()
        if self.__connected_lock.acquire():
            self.__connected_lock.release()
        self.__mqc.loop_stop()


class BusMessageEvent(wx.PyCommandEvent):
    def __init__(self, etype=None, eid=None, message=None):
        if not eid:
            eid = -1

        if not etype:
            etype = _busMessage

        if not message:
            raise ValueError("Message cannot be None")

        super().__init__(etype, eid)
        self.__message = message

    def message(self):
        return self.__message

    def topic_str(self):
        return str(self.__message.topic)

    def payload_str(self):
        return self.__message.payload.decode("utf-8")

    def payload_obj(self):
        return json.loads(self.__message.payload.decode("utf-8"))
