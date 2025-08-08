# import wx

# class WordCloudPanel(wx.Panel):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.current_wx_image = None
#         self.bitmap = None

#         self.Bind(wx.EVT_PAINT, self.on_paint)
#         self.Bind(wx.EVT_SIZE, self.on_size)

#     def update_wordcloud(self, wx_image):
#         self.current_wx_image = wx_image
#         self._refresh_bitmap()
#         self.Refresh()

#     def _refresh_bitmap(self):
#         if not self.current_wx_image:
#             self.bitmap = None
#             return

#         panel_size = self.GetClientSize()
#         img_w, img_h = self.current_wx_image.GetWidth(), self.current_wx_image.GetHeight()

#         scale_w = panel_size.width / img_w
#         scale_h = panel_size.height / img_h
#         # Allow scaling UP to fill space
#         scale = min(scale_w, scale_h)  

#         new_w = max(int(img_w * scale), 1)
#         new_h = max(int(img_h * scale), 1)

#         scaled_img = self.current_wx_image.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)
#         self.bitmap = wx.Bitmap(scaled_img)

#     def on_paint(self, event):
#         dc = wx.PaintDC(self)
#         if self.bitmap:
#             # Center bitmap in panel
#             w, h = self.GetClientSize()
#             bmp_w, bmp_h = self.bitmap.GetWidth(), self.bitmap.GetHeight()
#             x = (w - bmp_w) // 2
#             y = (h - bmp_h) // 2
#             dc.DrawBitmap(self.bitmap, x, y)

#     def on_size(self, event):
#         self._refresh_bitmap()
#         self.Refresh()
#         event.Skip()
