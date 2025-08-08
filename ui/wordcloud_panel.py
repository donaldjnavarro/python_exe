import wx

class WordCloudPanel(wx.Panel):
    def __init__(self, parent, size=(180, 180)):
        super().__init__(parent, size=size)
        self.SetMinSize(size)
        self.current_image = None

    def set_wordcloud(self, wx_image):
        self.DestroyChildren()
        self.current_image = wx_image

        if wx_image:
            panel_size = self.GetSize()
            img = wx_image.Copy()
            w, h = img.GetWidth(), img.GetHeight()
            max_w, max_h = panel_size.GetWidth(), panel_size.GetHeight()

            scale_w = max_w / w
            scale_h = max_h / h
            scale = min(scale_w, scale_h, 1.0)  # Do not upscale

            new_w = int(w * scale)
            new_h = int(h * scale)

            img = img.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)
            bmp = wx.Bitmap(img)

            static_bitmap = wx.StaticBitmap(self, bitmap=bmp)
            static_bitmap.Bind(wx.EVT_LEFT_DOWN, self.on_click)

            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(static_bitmap, 0, wx.ALIGN_CENTER)
            self.SetSizer(sizer)
            self.Layout()

    def on_click(self, event):
        if not self.current_image:
            return
        
        dlg = wx.Dialog(self, title="Wordcloud", size=(600, 600), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.bitmap_ctrl = wx.StaticBitmap(dlg)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.bitmap_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        dlg.SetSizer(sizer)

        def on_resize(evt):
            size = dlg.GetClientSize()
            max_w, max_h = size.GetWidth() - 20, size.GetHeight() - 20
            img = self.current_image.Copy()
            w, h = img.GetWidth(), img.GetHeight()

            scale = min(max_w / w, max_h / h, 1.0)
            new_w = int(w * scale)
            new_h = int(h * scale)
            img = img.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)
            bmp = wx.Bitmap(img)
            self.bitmap_ctrl.SetBitmap(bmp)
            dlg.Layout()
            if evt is not None:
                evt.Skip()


        dlg.Bind(wx.EVT_SIZE, on_resize)

        # Initial display
        on_resize(None)

        dlg.ShowModal()
        dlg.Destroy()


