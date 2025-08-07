import wx

class MyApp(wx.App):
    def OnInit(self):
        frame = wx.Frame(None, title="wxPython EXE Test", size=(300, 150))
        panel = wx.Panel(frame)

        wx.StaticText(panel, label="Hello from my wxPython EXE!", pos=(50, 40))

        btn = wx.Button(panel, label="OK", pos=(110, 80))
        btn.Bind(wx.EVT_BUTTON, self.on_close)

        frame.Show()
        return True

    def on_close(self, event):
        self.ExitMainLoop()

def main():
    app = MyApp(False)
    app.MainLoop()

if __name__ == "__main__":
    main()
