import wx
import wx.stc


class CodeEditorPanel(wx.Panel):
    """CodeEditorPanel wraps all the logic to process user input movement and
    interact with the external file manager to write/read data from files
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__vbox = wx.BoxSizer(wx.VERTICAL)

        self.__stc = wx.stc.StyledTextCtrl(self)

        self.__stc.StyleSetFont(wx.stc.STC_STYLE_DEFAULT,
            wx.Font(wx.FontInfo(14).Family(wx.FONTFAMILY_TELETYPE))) 


        self.__vbox.Add(self.__stc, wx.ID_ANY, wx.EXPAND | wx.ALL, 1)
        self.__stc.SetScrollWidth(self.GetSize().width)
        self.__stc.SetScrollWidthTracking(1)
        self.SetSizer(self.__vbox)
