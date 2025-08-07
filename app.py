import wx
from ui.main_frame import MainFrame

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, title="File Upload App", size=(500, 400))
        self.frame.Show()
        return True
