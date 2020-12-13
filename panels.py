import wx
import wx.stc

INSERT_MODE = "I"
NAVIGATE_MODE = "N"


class CodeEditorPanel(wx.Panel):
    """CodeEditorPanel wraps all the logic to process user input movement and
    interact with the external file manager to write/read data from files
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__vbox = wx.BoxSizer(wx.VERTICAL)

        self.__stc = wx.stc.StyledTextCtrl(self)

        self.__stc.StyleSetFont(
            wx.stc.STC_STYLE_DEFAULT,
            wx.Font(wx.FontInfo(14).Family(wx.FONTFAMILY_TELETYPE)),
        )

        self.__mode = INSERT_MODE

        self.__vbox.Add(self.__stc, wx.ID_ANY, wx.EXPAND | wx.ALL, 1)
        self.__stc.Bind(wx.EVT_CHAR, self.__handleChar, id=wx.ID_ANY)
        self.__stc.Bind(wx.EVT_KEY_DOWN, self.__handleKeyDown, id=wx.ID_ANY)
        self.__stc.SetScrollWidth(self.GetSize().width)
        self.__stc.SetScrollWidthTracking(1)
        self.SetSizer(self.__vbox)

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
            self.__mode = NAVIGATE_MODE
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
            self.__mode = INSERT_MODE

    def __handleCharInsertMode(self, event, *args, **kwargs):
        event.Skip()
