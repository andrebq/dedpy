# First things, first. Import the wxPython package.
import wx
import wx.aui

from panels import CodeEditorPanel

# Next, create an application object.
app = wx.App()

# Then a frame.
frm = wx.Frame(None, title="Hello World", size=wx.Size(800, 600))


# dock
manager = wx.aui.AuiManager(frm)
manager.AddPane(CodeEditorPanel(frm), wx.CENTER, "mainEditor")

scratchArea = CodeEditorPanel(frm)
info = wx.aui.AuiPaneInfo().BestSize(wx.Size(300, 600)).Caption("Scratch")
info = info.Right().CloseButton(0)
manager.AddPane(scratchArea, info)
manager.Update()

# Show it.
frm.Show()

# Start the event loop.
app.MainLoop()
