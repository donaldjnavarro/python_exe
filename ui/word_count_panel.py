import wx

class WordCountPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = wx.StaticText(self, label="Total words: 0")
        font = self.label.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.label.SetFont(font)

        outer_sizer = wx.BoxSizer(wx.VERTICAL)
        outer_sizer.AddStretchSpacer(1)
        outer_sizer.Add(self.label, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        outer_sizer.AddStretchSpacer(1)
        self.SetSizer(outer_sizer)

    def update_count(self, total_words: int):
        """Update label with commas for thousands."""
        self.label.Wrap(-1)
        self.label.SetLabel(f"Total words: {total_words:,}")
        self.Layout()
        self.Refresh()

        parent = self.GetParent()
        if parent:
            parent.Layout()
            parent.Refresh()
