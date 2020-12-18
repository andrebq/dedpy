import paho.mqtt.client as mqtt
import threading
import pid
import json
import wx
import weakref

_busMessage = wx.NewEventType()
EVT_NEW_MESSAGE = wx.PyEventBinder(_busMessage, 1)

class Bus:
    def __init__(self, addr="127.0.0.1", port=1883):
        busPID = pid.random_pid()
        self.__buspid = busPID
        self.__addr = addr
        self.__port = port

        self.__mqc = mqtt.Client(client_id=str(busPID), clean_session=False)
        self.__mqc.connect(addr, port)
        self.__mqc.on_connect = self.__bus_connected
        self.__mqc.on_disconnect = self.__bus_disconnected
        self.__mqc.on_message = self.__bus_new_message
        self.__connected = False
        self.__connected_lock = threading.Lock()
    
    def duplicate(self):
        """ returns a new Bus object connected to the same address/port
        of the current one.

        Useful when you want to have multiple subscriptions to the same
        topic but their handlers should be independent of each other.

        Each bus runs on its own thread"""
        return Bus(addr=self.__addr, port=self.__port)

    def publish_json(self, topic, payload_object):
        self.__mqc.publish(topic, json.dumps(payload_object))

    def subscribe_pid(self, pid, topic, callback):
        if not pid:
            topic_str = '/'.join(topic)
            self.__mqc.message_callback_add('/'.join(topic), callback)
            self.__mqc.subscribe(topic_str, qos=1)
            return
        topic_str = pid.topic(topic)
        self.__mqc.message_callback_add(pid.topic(topic), callback)
        self.__mqc.subscribe(topic_str, qos=1)

    def __bus_new_message(self, client, userdata, message):
        pass

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

def connect_to_widget(bus, widget, pid, topic):
    """ returns a closure which implements mqtt on_message callback
    and for each new mqtt message it will publish a BusMessageEvent
    to widget.

    Widget is kept in a weak-ref to avoid having to write dispose methods,
    the callback though is not cleared if the widget is gc'ed
    """
    cb = _make_bus_callback(widget)
    print(bus, widget, pid, topic)
    bus.subscribe_pid(pid, topic, cb)

def _make_bus_callback(widget):
    widget = weakref.ref(widget)

    def _callback(client, userdata, message):
        ev = BusMessageEvent(message=message)
        w = widget()
        wx.PostEvent(w, ev)
    return _callback
