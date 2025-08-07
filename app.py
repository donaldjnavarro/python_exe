import wx
from ui.main_frame import MainFrame
import nltk
import os
import sys

if hasattr(sys, '_MEIPASS'):
    # PyInstaller stores temp folder in _MEIPASS
    nltk.data.path.append(os.path.join(sys._MEIPASS, 'corpora'))

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, title="Text Analysis", size=(500, 400))
        self.frame.Show()
        return True
