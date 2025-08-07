import wx

class WordCountPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.SetBackgroundColour(wx.Colour(220, 230, 250))  # panel bg color

        self.label = wx.StaticText(self, label="Total words: 0")

        font = self.label.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.label.SetFont(font)

        self.label.SetForegroundColour(wx.Colour(10, 36, 99))
        self.label.SetBackgroundColour(wx.Colour(220, 230, 250))  # match panel bg

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        self.SetSizer(sizer)

    def update_count(self, total_words: int):
        self.label.SetLabel(f"Total words: {total_words}")
        self.label.Wrap(-1)   # help with text sizing
        self.Layout()
        self.Refresh()

        # Also refresh parent panel in case
        parent = self.GetParent()
        if parent:
            parent.Layout()
            parent.Refresh()
