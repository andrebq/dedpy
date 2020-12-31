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

    def pid_conn(self, pid):
        return PidConn(self, pid)

    def duplicate(self):
        """returns a new Bus object connected to the same address/port
        of the current one.

        Useful when you want to have multiple subscriptions to the same
        topic but their handlers should be independent of each other.

        Each bus runs on its own thread"""
        return Bus(addr=self.__addr, port=self.__port)

    def _broadcast_json(self, pid, payload=None, meta={}):
        meta["sender"] = str(pid)
        self.__mqc.publish(
            pid.topic(["broadcast"]),
            json.dumps(
                {
                    "payload": payload,
                    "meta": meta,
                }
            ),
        )

    def _unicast_json(self, fromPid, toPid, payload=None, meta={}):
        meta["sender"] = str(fromPid)
        self.__mqc.publish(
            toPid.topic(["input"]),
            json.dumps(
                {
                    "payload": payload,
                    "meta": meta,
                }
            ),
        )

    def subscribe_pid(self, pid, topic, callback):
        if not pid:
            topic_str = "/".join(topic)
            self.__mqc.message_callback_add("/".join(topic), callback)
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


class PidConn:
    def __init__(self, bus, pid):
        self.__bus = bus
        self.__pid = pid

    def broadcast(self, payload=None, meta={}):
        self.__bus._broadcast_json(self.__pid, payload, meta)

    def unicast(self, pid, payload=None, meta={}):
        self.__bus._unicast_json(
            fromPid=self.__pid, toPid=pid, payload=payload, meta=meta
        )

    def pid(self):
        return self.__pid

    def bus(self):
        return self.__bus


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
        self.__sender = None
        self.__obj = None

    def message(self):
        return self.__message

    def topic_str(self):
        return str(self.__message.topic)

    def payload_str(self):
        return self.__message.payload.decode("utf-8")

    def payload_obj(self):
        self.__parse_payload()
        return self.__obj['payload']
    
    def __parse_payload(self):
        if self.__obj:
            return self.__obj
        self.__obj = json.loads(self.__message.payload.decode("utf-8"))
    
    def meta_obj(self):
        self.__parse_payload()
        return self.__obj['meta']
    
    def raw_dict(self):
        self.__parse_payload()
        return self.__obj

    def sender(self):
        if self.__sender:
            return self.__sender

        obj = self.payload_obj()
        try:
            self.__sender = pid.try_parse_pid(obj["meta"]["sender"])
        except KeyError:
            pass

        return self.__sender

    def is_valid_pid_msg(self):
        return self.sender() != None


def connect_to_widget(bus, widget, pid):
    """Configures the widget so that whenever a new message is published
    in the given pid input box the widget will receive a BusMessageEvent
    with the information from that specific message.

    The callback will ensure that
    """
    cb = _make_bus_callback(widget)
    topic = pid.topic(["inbox"])
    bus.subscribe_pid(pid, topic, cb)


def _make_bus_callback(widget):
    widget = weakref.ref(widget)

    def _callback(client, userdata, message):
        ev = BusMessageEvent(message=message)
        if not ev.is_valid_pid_msg():
            print("Invalid message: ", ev.payload_str())
            return

        w = widget()
        wx.PostEvent(w, ev)

    return _callback
