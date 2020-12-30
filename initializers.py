import wx
import internals


def enable_bus_debugger(bus):
    debugBus = bus.duplicate()
    debugBus.start_loop()
    busview = internals.BusView(None, size=wx.Size(800, 600))
    busview.Show()
    internals.attach_debugger(debugBus, busview)
    return (busview, debugBus)
