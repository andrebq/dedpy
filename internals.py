import wx
import bus as bus_module


class BusView(wx.Frame):
    def __init__(self, parent=None, bus=None, *args, **kw):
        super().__init__(parent, *args, **kw)

        self.SetTitle("Bus Viewer")

        self.__messages = wx.ListView(self)
        self.__messages.AppendColumn("Topic", wx.LIST_FORMAT_LEFT)
        self.__messages.AppendColumn("RawJSON", wx.LIST_FORMAT_LEFT)
        self.__messages.AppendColumn("Repr", wx.LIST_FORMAT_LEFT)

        self.Bind(bus_module.EVT_NEW_MESSAGE, self.__on_new_message)

    def got_new_message(self, client, userdata, msg):
        wx.PostEvent(self, bus_module.BusMessageEvent(message=msg))

    def __on_new_message(self, evt):
        self.__messages.Append(
            (evt.topic_str(), evt.payload_str(), repr(evt.payload_obj()))
        )
        self.__messages.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.__messages.SetColumnWidth(2, wx.LIST_AUTOSIZE)
