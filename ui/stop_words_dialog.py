import wx
from utils.text_analysis import STOPWORDS

class StopwordsInfoDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Learn more about stopwords", size=(500, 400),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        info_text = (
            "Stopwords are common words that are often excluded from text analysis "
            "because they appear frequently and carry little meaningful information. "
            "Examples include words like 'the', 'and', 'is', etc.\n\n"
            "Below is the full list of stopwords used in this application:"
        )

        # Static text label for explanation (wrap it)
        info_label = wx.StaticText(self, label=info_text)
        info_label.Wrap(480)  # Wrap to fit nicely inside dialog width

        # Multiline read-only TextCtrl for full stopwords list, scrollable
        stopwords_text = "\n".join(sorted(STOPWORDS))
        stopwords_ctrl = wx.TextCtrl(self, value=stopwords_text,
                                     style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        
        btn_close = wx.Button(self, wx.ID_CLOSE, label="Close")
        btn_close.Bind(wx.EVT_BUTTON, self.on_close)

        # Layout sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(info_label, 0, wx.ALL, 10)
        sizer.Add(stopwords_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        sizer.Add(btn_close, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(sizer)
        self.Layout()
        self.Centre()

    def on_close(self, event):
        self.EndModal(wx.ID_CLOSE)
