import wx
import bus as bus_module
import weakref
import bus as bus_module


class BusView(wx.Frame):
    def __init__(self, parent=None, *args, **kw):
        super().__init__(parent, *args, **kw)

        self.SetTitle("Bus Viewer")

        self.__messages = wx.ListView(self)
        self.__messages.AppendColumn("Topic", wx.LIST_FORMAT_LEFT)
        self.__messages.AppendColumn("RawJSON", wx.LIST_FORMAT_LEFT)
        self.__messages.AppendColumn("Repr", wx.LIST_FORMAT_LEFT)

        self.Bind(bus_module.EVT_NEW_MESSAGE, self.__on_new_message)

    def __on_new_message(self, evt):
        self.__messages.Append(
            (evt.topic_str(), evt.payload_str(), repr(evt.payload_obj()))
        )
        self.__messages.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.__messages.SetColumnWidth(2, wx.LIST_AUTOSIZE)


def attach_debugger(bus, busview):
    cb = _make_bus_callback(busview)
    bus.subscribe_pid(pid=None, topic=["pid", "+", "#"], callback=cb)


def _make_bus_callback(widget):
    widget = weakref.ref(widget)

    def _callback(client, userdata, message):
        ev = bus_module.BusMessageEvent(message=message)
        w = widget()
        wx.PostEvent(w, ev)

    return _callback
