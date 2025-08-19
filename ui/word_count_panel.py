import wx

class WordCountPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = wx.StaticText(self, label="Total words: 0")

        font = self.label.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.label.SetFont(font)

        # Outer sizer fills the panel
        outer_sizer = wx.BoxSizer(wx.VERTICAL)

        # Center label inside the expanded panel
        outer_sizer.AddStretchSpacer(1)  # push label down
        outer_sizer.Add(self.label, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        outer_sizer.AddStretchSpacer(1)  # push label up

        self.SetSizer(outer_sizer)

    def update_count(self, total_words: int):
        self.label.SetLabel(f"Total words: {total_words}")
        self.label.Wrap(-1)   # help with text sizing
        self.Layout()
        self.Refresh()

        # Refresh parent too
        parent = self.GetParent()
        if parent:
            parent.Layout()
            parent.Refresh()
