import wx

class WordCloudPanel(wx.Panel):
    def __init__(self, parent, size=(180, 180)):
        super().__init__(parent, size=size)
        self.SetMinSize(size)

    def set_wordcloud(self, wx_image):
        # Clear existing children
        for child in self.GetChildren():
            child.Destroy()

        if wx_image:
            panel_size = self.GetSize()
            img = wx_image.Copy()
            w, h = img.GetWidth(), img.GetHeight()
            max_w, max_h = panel_size.GetWidth(), panel_size.GetHeight()

            scale_w = max_w / w
            scale_h = max_h / h
            scale = min(scale_w, scale_h, 1.0)  # Don't upscale

            new_w = int(w * scale)
            new_h = int(h * scale)

            img = img.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)

            bmp = wx.Bitmap(img)
            wx.StaticBitmap(self, bitmap=bmp)
            self.Layout()
