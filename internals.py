import wx
import bus as bus_module
import weakref
import bus as bus_module
from theme import Default

class _MessagePanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super().__init__(parent, *args, **kw)

        self.__sizer = wx.BoxSizer(wx.VERTICAL)
        self.__count = 0
        self.__rawEvents = {}

        self.__messages = wx.ListView(self)
        self.__messages.AppendColumn("Topic", wx.LIST_FORMAT_LEFT)
        self.__messages.AppendColumn("RawJSON", wx.LIST_FORMAT_LEFT)

        self.__sizer.Add(self.__messages, 1, wx.EXPAND, 0)
        self.__sizer.SetSizeHints(self)
        self.SetSizer(self.__sizer)
    
    def autofit(self):
        self.__messages.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.__messages.SetColumnWidth(2, wx.LIST_AUTOSIZE)
    
    def append_event(self, evt):
        self.__count += 1
        itemId = self.__messages.Append(
            (evt.topic_str(), evt.payload_str())
        )
        self.__messages.SetItemData(itemId, self.__count)
        self.__rawEvents[self.__count] = evt.raw_dict()
        return (itemId, self.__count)
    
    def event_by_id(self, id):
        try:
            return self.__rawEvents[id]
        except KeyError:
            return None

class _EventViewer(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super().__init__(parent, *args, **kw)
        self.SetBackgroundColour(Default.AltBackground)
        self.__sizer = wx.BoxSizer(wx.VERTICAL)
        self.__tree = wx.TreeCtrl(self)
        self.__sizer.Add(self.__tree, 1, wx.EXPAND, 0)
        self.__sizer.SetSizeHints(self)
        self.SetSizer(self.__sizer)
    
    def display(self, busDict):
        self.__tree.DeleteAllItems()
        root = self.__tree.AddRoot('MessageBus')
        self.__append_dict(root, busDict)
        self.__tree.ExpandAll()
    
    def __append_dict(self, treeParent, pyDict):
        for k in pyDict:
            value = pyDict[k]
            if isinstance(value, dict):
                subTree = self.__tree.AppendItem(treeParent, str(k))
                self.__append_dict(subTree, value)
            else:
                self.__tree.AppendItem(treeParent, f'{k}: {value}')


class BusView(wx.Frame):
    def __init__(self, parent=None, *args, **kw):
        super().__init__(parent, *args, **kw)

        self.SetTitle("Bus Viewer")

        self.__manager = wx.aui.AuiManager(self)
        self.__messages = _MessagePanel(self)
        self.__manager.AddPane(self.__messages, wx.CENTER, "Messages")

        self.__event_viewer = _EventViewer(self)
        info = wx.aui.AuiPaneInfo().BestSize(wx.Size(500, 600)).Caption("Event viewer")
        info = info.Right().CloseButton(0)
        self.__manager.AddPane(self.__event_viewer, info)
        self.__manager.Update()

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.__message_selected)

        self.Bind(bus_module.EVT_NEW_MESSAGE, self.__on_new_message)

    def __on_new_message(self, evt):
        itemId = self.__messages.append_event(evt)
        self.__messages.autofit()
    
    def __message_selected(self, evt):
        self.__event_viewer.display(self.__messages.event_by_id(evt.GetData()))


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
