# First things, first. Import the wxPython package.
import wx
import wx.aui
import internals
import subprocess
import threading
import time

import bus
import pid
import dirlist
import initializers

from panels import CodeEditorPanel

rootPID = pid.Pid()

try:
    globalBus = bus.Bus()
except ConnectionRefusedError as e:
    # this whole logic is too broken to be considered reliable,
    # but works for testing purposes
    def start_hmq(name):
        subprocess.call("hmq")

    t = threading.Thread(target=start_hmq, args=(1,), daemon=True)
    t.start()
    time.sleep(5)
    globalBus = bus.Bus()


globalBus.start_loop()


app = wx.App()
(busview, debugBus) = initializers.enable_bus_debugger(globalBus.duplicate())

# dock
frm = wx.Frame(None, title="Hello World", size=wx.Size(800, 600))
manager = wx.aui.AuiManager(frm)
mainEditor = CodeEditorPanel(frm, bus=globalBus, pid=rootPID.sub_pid())

manager.AddPane(mainEditor, wx.CENTER, "mainEditor")

scratchArea = CodeEditorPanel(frm, bus=globalBus, pid=rootPID.sub_pid())

info = wx.aui.AuiPaneInfo().BestSize(wx.Size(300, 600)).Caption("Scratch")
info = info.Right().CloseButton(0)
manager.AddPane(scratchArea, info)

filenav = dirlist.LocalDirList(frm, bus=globalBus, pid=rootPID.sub_pid())
info = wx.aui.AuiPaneInfo().BestSize(wx.Size(300, 600)).Caption("Files")
info = info.Left().CloseButton(0)
manager.AddPane(filenav, info)

manager.Update()

# Show it.
frm.Show()

# Start the event loop.
app.MainLoop()
globalBus.end_loop()
debugBus.end_loop()
