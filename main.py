# First things, first. Import the wxPython package.
import wx
import wx.aui
import internals

from bus import Bus
import pid

rootPID = pid.Pid()

globalBus = Bus()
globalBus.start_loop()
globalBus.watch_pid(rootPID)

from panels import CodeEditorPanel

# Next, create an application object.
app = wx.App()

# Then a frame.
frm = wx.Frame(None, title="Hello World", size=wx.Size(800, 600))
busview = internals.BusView(None, bus=globalBus, size=wx.Size(800, 600))
busview.Show()
globalBus.watch_all_pids(busview.got_new_message)


# dock
manager = wx.aui.AuiManager(frm)
manager.AddPane(
    CodeEditorPanel(frm, bus=globalBus, pid=rootPID.sub_pid()), wx.CENTER, "mainEditor"
)

scratchArea = CodeEditorPanel(frm, bus=globalBus, pid=rootPID.sub_pid())
info = wx.aui.AuiPaneInfo().BestSize(wx.Size(300, 600)).Caption("Scratch")
info = info.Right().CloseButton(0)
manager.AddPane(scratchArea, info)
manager.Update()

# Show it.
frm.Show()

# Start the event loop.
app.MainLoop()
globalBus.end_loop()
