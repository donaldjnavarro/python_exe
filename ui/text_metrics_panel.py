import wx

class TextMetricsPanel(wx.Panel):
    """Panel displaying text metrics: number-first, human-readable phrase second."""
    def __init__(self, parent):
        super().__init__(parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        # Add a placeholder row so panel is visible initially
        placeholder = wx.StaticText(self, label="Metrics will appear here")
        self.sizer.Add(placeholder, 0, wx.ALL, 5)
        self.Layout()

    def update_metrics(self, metrics: dict):
        """
        metrics: dict mapping metric name -> "number description" string
        """
        # Clear old children
        self.sizer.Clear(True)

        for key, phrase in metrics.items():
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)

            # Number (bold, leftmost)
            number_str = phrase.split()[0]
            number_label = wx.StaticText(self, label=number_str)
            font = number_label.GetFont()
            font = font.Bold()
            number_label.SetFont(font)
            h_sizer.Add(number_label, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

            # Remaining text
            text_label = wx.StaticText(self, label=' '.join(phrase.split()[1:]))
            h_sizer.Add(text_label, 1, wx.ALIGN_CENTER_VERTICAL)

            self.sizer.Add(h_sizer, 0, wx.BOTTOM, 2)

        self.Layout()
