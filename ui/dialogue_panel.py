import wx

class DialogueNarrationPanel(wx.Panel):
    """Panel showing dialogue vs narration proportions in the text."""

    def __init__(self, parent):
        super().__init__(parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        # Title label
        self.title_label = wx.StaticText(self, label="Dialogue vs Narration")
        font = self.title_label.GetFont()
        font.PointSize += 2
        font = font.Bold()
        self.title_label.SetFont(font)
        self.sizer.Add(self.title_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # Horizontal sizer for numbers and bar
        numbers_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Dialogue label
        self.dialogue_label = wx.StaticText(self, label="Dialogue: 0 words")
        numbers_sizer.Add(self.dialogue_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)

        # Spacer stretches the bar and separates numbers
        numbers_sizer.AddStretchSpacer(1)

        # Narration label
        self.narration_label = wx.StaticText(self, label="Narration: 0 words")
        numbers_sizer.Add(self.narration_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        self.sizer.Add(numbers_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Proportion bar
        self.gauge = wx.Gauge(self, range=100, style=wx.GA_HORIZONTAL)
        self.sizer.Add(self.gauge, 0, wx.EXPAND | wx.ALL, 5)

        # Initially empty counts
        self.dialogue_words = 0
        self.narration_words = 0
        self.Layout()

    def update_counts(self, dialogue_words: int, narration_words: int):
        """Update the displayed counts and adjust the bar."""
        self.dialogue_words = dialogue_words
        self.narration_words = narration_words

        total_words = dialogue_words + narration_words
        if total_words > 0:
            dialogue_percent = int((dialogue_words / total_words) * 100)
        else:
            dialogue_percent = 0

        # Update labels
        self.dialogue_label.SetLabel(f"Dialogue: {dialogue_words:,} words")
        self.narration_label.SetLabel(f"Narration: {narration_words:,} words")

        # Update bar
        self.gauge.SetValue(dialogue_percent)

        self.Layout()
        self.Refresh()
