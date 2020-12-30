import wx
import bus as bus_module
import os
from theme import Default


class LocalDirList(wx.Panel):
    def __init__(self, parent, bus=None, pid=None, *args, **kw):
        if not pid:
            raise ValueError("pid is required")
        if not bus:
            raise ValueError("bus is required")
        super().__init__(parent, *args, **kw)
        self.__bus = bus
        self.__pid = pid

        self.SetBackgroundColour(Default.AltBackground)

        self.__dirlist = wx.GenericDirCtrl(
            self,
            dir=os.path.abspath("."),
            style=wx.DIRCTRL_SHOW_FILTERS | wx.DIRCTRL_MULTIPLE,
        )
        self.__dirlist.SetDefaultPath(os.path.abspath("."))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.__dirlist, 1, wx.EXPAND, 0)
        sizer.SetSizeHints(self)
        self.SetSizer(sizer)

        self.Bind(bus_module.EVT_NEW_MESSAGE, self.__on_new_message)

    def __on_new_message(self, evt):
        pass
