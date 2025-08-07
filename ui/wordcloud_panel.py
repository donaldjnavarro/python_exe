import wx

class WordCloudPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.bitmap = wx.StaticBitmap(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.bitmap, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

    def update_wordcloud(self, wx_image):
        bmp = wx_image.ConvertToBitmap()
        self.bitmap.SetBitmap(bmp)
        self.Layout()
