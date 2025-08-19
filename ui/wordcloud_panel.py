import wx

class WordCloudPanel(wx.Panel):
    def __init__(self, parent, size=(300, 300)):
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

            # Calculate scale to fill the panel while maintaining aspect ratio
            scale_w = max_w / w
            scale_h = max_h / h
            scale = min(scale_w, scale_h)  # Allow upscaling to fill available space

            new_w = int(w * scale)
            new_h = int(h * scale)

            img = img.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)
            bmp = wx.Bitmap(img)

            static_bitmap = wx.StaticBitmap(self, bitmap=bmp)
            static_bitmap.Bind(wx.EVT_LEFT_DOWN, self.on_click)

            # Use a sizer that expands to fill available space
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(static_bitmap, 1, wx.EXPAND)
            self.SetSizer(sizer)
            self.Layout()

    def on_click(self, event):
        if not hasattr(self, 'current_image') or self.current_image is None:
            return

        dlg = wx.Dialog(self, title="Wordcloud - Click and drag to resize", size=(400, 400), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        
        # Bitmap control for displaying image
        self.bitmap_ctrl = wx.StaticBitmap(dlg)
        
        # Save button
        save_btn = wx.Button(dlg, label="Save Image")
        
        # Event handler for save button
        def on_save(event):
            with wx.FileDialog(dlg, "Save Wordcloud Image", wildcard="PNG files (*.png)|*.png|JPEG files (*.jpg)|*.jpg",
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # User cancelled
                path = fileDialog.GetPath()
                ext = os.path.splitext(path)[1].lower()
                # Default to PNG if no extension or unknown
                img_format = wx.BITMAP_TYPE_PNG
                if ext in ['.jpg', '.jpeg']:
                    img_format = wx.BITMAP_TYPE_JPEG
                try:
                    self.current_image.SaveFile(path, img_format)
                    wx.MessageBox(f"Image saved to:\n{path}", "Success", wx.ICON_INFORMATION)
                except Exception as e:
                    wx.MessageBox(f"Failed to save image:\n{e}", "Error", wx.ICON_ERROR)
        
        save_btn.Bind(wx.EVT_BUTTON, on_save)
        
        # Layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.bitmap_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        vbox.Add(save_btn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        dlg.SetSizer(vbox)
        
        def on_resize(evt):
            size = dlg.GetClientSize()
            max_w, max_h = size.GetWidth() - 20, size.GetHeight() - 60  # leave room for button
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
        
        # Initial set image
        on_resize(None)
        dlg.ShowModal()
        dlg.Destroy()



