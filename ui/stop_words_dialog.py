import wx
from utils.text_analysis import STOPWORDS

class StopwordsInfoDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Learn more about stopwords", size=(500, 400),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        info_text = (
            "Stopwords are common words that are often excluded from text analysis because they appear frequently and carry little meaningful information."
            "\n"
            "\nBelow is the full list of words that are considered stopwords by this application:"
        )

        # Static text label for explanation
        info_label = wx.StaticText(self, label=info_text)
        info_label.Wrap(480)

        # Stopwords as a single wrapped paragraph
        stopwords_text = ", ".join(sorted(STOPWORDS))

        # Use a read-only, word-wrapped TextCtrl
        stopwords_ctrl = wx.TextCtrl(
            self,
            value=stopwords_text,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP | wx.BORDER_SUNKEN
        )

        btn_close = wx.Button(self, wx.ID_CLOSE, label="Close")
        btn_close.Bind(wx.EVT_BUTTON, self.on_close)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(info_label, 0, wx.ALL, 10)
        sizer.Add(stopwords_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        sizer.Add(btn_close, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(sizer)
        self.Layout()
        self.Centre()

    def on_close(self, event):
        self.EndModal(wx.ID_CLOSE)
