import wx 
 
class Example(wx.Frame): 
   
   def __init__(self, parent, title): 
      super(Example, self).__init__(parent, title = title, size = (200,300)) 
             
      self.InitUI() 
      self.Centre() 
      self.Show()
		
   def InitUI(self): 
      p = wx.Panel(self) 
      vbox = wx.BoxSizer(wx.VERTICAL) 
      l1 = wx.StaticText(p,label = "Enter a number",style = wx.ALIGN_CENTRE ) 
      vbox.Add(l1,0,  wx.EXPAND) 
      b1 = wx.Button(p, label = "Btn1") 
      vbox.Add(b1,0,wx.EXPAND) 


      p.SetSizer(vbox) 
          
app = wx.App() 
Example(None, title = 'BoxSizer demo') 
app.MainLoop()
