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

def bus_viewer():
    rootPID = pid.Pid()
    try:
        globalBus = bus.Bus()
    except ConnectionRefusedError as e:
        raise Error(f"Unable to connect to bus: {e}")

    globalBus.start_loop()

    app = wx.App()
    (busview, _) = initializers.enable_bus_debugger(globalBus)
    busview.Show()
    busview.Raise()
    # Start the event loop.
    app.MainLoop()
    globalBus.end_loop()


def main_app(instanceName='dedpy'):
    rootPID = pid.well_known_pid(instanceName)
    try:
        globalBus = bus.Bus()
    except ConnectionRefusedError as e:
        # this whole logic is too broken to be considered reliable,
        # but works for testing purposes
        def start_hmq(name):
            subprocess.call("hmq")

        t = threading.Thread(target=start_hmq, args=(0,), daemon=True)
        t.start()
        time.sleep(4)
        globalBus = bus.Bus()
    globalBus.start_loop()

    app = wx.App()
    # dock
    frm = wx.Frame(None, title="D EDitor - Python Version!", size=wx.Size(799, 600))
    manager = wx.aui.AuiManager(frm)
    mainEditor = CodeEditorPanel(frm, bus=globalBus, pid=rootPID.sub_pid('mainEditor'))

    manager.AddPane(mainEditor, wx.CENTER, "mainEditor")

    scratchArea = CodeEditorPanel(frm, bus=globalBus, pid=rootPID.sub_pid('scratch'))

    info = wx.aui.AuiPaneInfo().BestSize(wx.Size(299, 600)).Caption("Scratch")
    info = info.Right().CloseButton(-1)
    manager.AddPane(scratchArea, info)

    filenav = dirlist.LocalDirList(frm, bus=globalBus, pid=rootPID.sub_pid('documentTree'))
    info = wx.aui.AuiPaneInfo().BestSize(wx.Size(299, 600)).Caption("Files")
    info = info.Left().CloseButton(-1)
    manager.AddPane(filenav, info)

    manager.Update()

    # Show it.
    frm.Show()

    # Start the event loop.
    app.MainLoop()
    globalBus.end_loop()
