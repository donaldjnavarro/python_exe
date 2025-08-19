import wx

class TextMetricsPanel(wx.Panel):
    """Panel displaying text metrics: number-first, human-readable phrase second, with optional group headers."""

    def __init__(self, parent):
        super().__init__(parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        # Placeholder row initially
        placeholder = wx.StaticText(self, label="Metrics will appear here")
        self.sizer.Add(placeholder, 0, wx.ALL, 5)
        self.Layout()

    def update_metrics(self, metrics: dict):
        """
        metrics: dict mapping metric name -> "number description" string, or group header string
        """
        # Clear old children
        self.sizer.Clear(True)

        for key, phrase in metrics.items():
            # Special styling for Total Words
            if key == "Total Words":
                number_str = phrase.split()[0]
                text_str = ' '.join(phrase.split()[1:])

                h_sizer = wx.BoxSizer(wx.HORIZONTAL)
                number_label = wx.StaticText(self, label=number_str)
                font = number_label.GetFont()
                font.PointSize += 6   # make it much bigger
                font = font.Bold()
                number_label.SetFont(font)
                h_sizer.Add(number_label, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)

                text_label = wx.StaticText(self, label=text_str)
                font2 = text_label.GetFont()
                font2.PointSize += 2
                text_label.SetFont(font2)
                h_sizer.Add(text_label, 1, wx.ALIGN_CENTER_VERTICAL)

                self.sizer.Add(h_sizer, 0, wx.TOP | wx.BOTTOM, 10)  # extra spacing around Total Words

            # Detect group header (no spaces or equal to key)
            elif phrase.strip() == key:  # group header
                header_label = wx.StaticText(self, label=phrase)
                font = header_label.GetFont()
                font.PointSize += 1
                font = font.Bold()
                header_label.SetFont(font)
                self.sizer.Add(header_label, 0, wx.TOP | wx.BOTTOM, 5)
            else:
                # Number-left, description-right
                parts = phrase.split()
                if not parts:
                    continue
                number_str = parts[0]
                text_str = ' '.join(parts[1:])
                h_sizer = wx.BoxSizer(wx.HORIZONTAL)

                # Number
                number_label = wx.StaticText(self, label=number_str)
                font = number_label.GetFont()
                font = font.Bold()
                number_label.SetFont(font)
                h_sizer.Add(number_label, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

                # Description
                text_label = wx.StaticText(self, label=text_str)
                h_sizer.Add(text_label, 1, wx.ALIGN_CENTER_VERTICAL)

                self.sizer.Add(h_sizer, 0, wx.BOTTOM, 2)

        self.Layout()
