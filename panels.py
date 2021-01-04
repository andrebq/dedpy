import wx
import wx.stc

from theme import Default
import bus as bus_module


INSERT_MODE = "I"
NAVIGATE_MODE = "N"


class CodeEditorPanel(wx.Panel):
    """CodeEditorPanel wraps all the logic to process user input movement and
    interact with the external file manager to write/read data from files
    """

    def __init__(self, parent, bus=None, pid=None, *args, **kwargs):
        if not bus:
            raise ValueError(
                "Cannot construct a Code Editor Panel without a bus connection"
            )

        if not pid:
            raise ValueError("Cannot construct a Code Editor Panel without a PID")

        super().__init__(parent, *args, **kwargs)

        self.__vbox = wx.BoxSizer(wx.VERTICAL)
        self.__pidconn = bus.pid_conn(pid)
        bus_module.connect_to_widget(self.__pidconn.bus(), self, self.__pidconn.pid())

        self.SetBackgroundColour(Default.Background)

        self.__stc = wx.stc.StyledTextCtrl(self)
        self.__stc.StyleSetBackground(
            wx.stc.STC_STYLE_DEFAULT, wx.Colour(Default.Background)
        )

        self.__stc.StyleSetFont(
            wx.stc.STC_STYLE_DEFAULT,
            wx.Font(wx.FontInfo(14).Family(wx.FONTFAMILY_TELETYPE)),
        )
        self.__stc.StyleClearAll()

        self.__mode = INSERT_MODE

        self.__vbox.Add(self.__stc, wx.ID_ANY, wx.EXPAND | wx.ALL, 1)
        self.__stc.Bind(wx.EVT_CHAR, self.__handleChar, id=wx.ID_ANY)
        self.__stc.Bind(wx.EVT_KEY_DOWN, self.__handleKeyDown, id=wx.ID_ANY)
        self.__stc.SetScrollWidth(self.GetSize().width)
        self.__stc.SetScrollWidthTracking(1)
        self.SetSizer(self.__vbox)

        self.__nav_acc = []
        self.__pidconn.broadcast()
        self.Bind(bus_module.EVT_NEW_MESSAGE, self.__on_new_message)

    def pid(self):
        return self.__pid

    def __on_new_message(self, evt):
        pass

    def __publish_bus_event(self, opts={}):
        opts[u"pid"] = str(self.__pid)

    def __handleChar(self, event, *args, **kwargs):
        if self.__mode == INSERT_MODE:
            self.__handleCharInsertMode(event, *args, **kwargs)
        elif self.__mode == NAVIGATE_MODE:
            self.__handleCharNavMode(event, *args, **kwargs)

    def __handleKeyDown(self, event, *args, **kwargs):
        if self.__mode == INSERT_MODE:
            self.__handleKeyDownInsertMode(event, *args, **kwargs)
        elif self.__mode == NAVIGATE_MODE:
            self.__handleKeyDownNavMode(event, *args, **kwargs)

    def __handleKeyDownInsertMode(self, event, *args, **kwargs):
        if event.KeyCode == wx.WXK_ESCAPE:
            self.__enterNavigateMode()
            return
        event.Skip()

    def __handleKeyDownNavMode(self, event, *args, **kwargs):
        event.Skip()

    def __handleCharNavMode(self, event, *args, **kwargs):
        # this key handling is very poor and should be worked out
        # in the future, but I just want to test how mode switch works
        if event.GetUnicodeKey() == wx.WXK_NONE:
            return
        ch = chr(event.GetUnicodeKey())

        if ch == u"i":
            self.__enterInsertMode()
        else:
            self.__nav_acc.append(ch)

    def __handleCharInsertMode(self, event, *args, **kwargs):
        event.Skip()

    def __enterNavigateMode(self):
        prev = self.__mode
        self.__mode = NAVIGATE_MODE
        self.__nav_acc = []
        self.__pidconn.broadcast({
            'mode': NAVIGATE_MODE,
            'prev': prev}, meta={'event': 'mode-change'})

    def __enterInsertMode(self):
        prev = self.__mode
        self.__mode = INSERT_MODE
        self.__pidconn.broadcast({
            'mode': INSERT_MODE,
            'prev': prev,
            'navAcc': self.__nav_acc}, meta={'event': 'mode-change'})
