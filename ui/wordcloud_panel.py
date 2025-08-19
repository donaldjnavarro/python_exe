import wx

class WordCloudPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.original_bitmap = None  # Original wx.Bitmap
        self.scaled_bitmap = None    # Scaled bitmap for drawing

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def set_wordcloud(self, wx_image: wx.Image):
        """Set a new wordcloud image and rescale it."""
        self.original_bitmap = wx.Bitmap(wx_image)
        self._rescale_to_fit()
        self.Refresh()

    def _rescale_to_fit(self):
        if not self.original_bitmap:
            return

        panel_w, panel_h = self.GetClientSize()
        if panel_w <= 0 or panel_h <= 0:
            return

        bmp_w, bmp_h = self.original_bitmap.GetSize()
        if bmp_w == 0 or bmp_h == 0:
            return

        scale = min(panel_w / bmp_w, panel_h / bmp_h)
        new_w, new_h = int(bmp_w * scale), int(bmp_h * scale)

        img = self.original_bitmap.ConvertToImage()
        img = img.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)
        self.scaled_bitmap = wx.Bitmap(img)

    def on_size(self, event):
        if self.original_bitmap:
            self._rescale_to_fit()
            self.Refresh()
        event.Skip()

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        if self.scaled_bitmap:
            panel_w, panel_h = self.GetClientSize()
            bmp_w, bmp_h = self.scaled_bitmap.GetSize()
            x = (panel_w - bmp_w) // 2
            y = (panel_h - bmp_h) // 2
            dc.DrawBitmap(self.scaled_bitmap, x, y, True)
