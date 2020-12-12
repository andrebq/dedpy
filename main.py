# First things, first. Import the wxPython package.
import wx
import wx.aui

from panels import CodeEditorPanel

# Next, create an application object.
app = wx.App()

# Then a frame.
frm = wx.Frame(None, title="Hello World")


# dock
manager = wx.aui.AuiManager(frm)
manager.AddPane(CodeEditorPanel(parent=frm), wx.CENTER, "mainEditor")
manager.Update()

# Show it.
frm.Show()

# Start the event loop.
app.MainLoop()
