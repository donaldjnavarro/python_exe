import wx

class WordListPanel(wx.Panel):
    def __init__(self, parent, title="Word List"):
        super().__init__(parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.title_lbl = wx.StaticText(self, label=title)
        font = self.title_lbl.GetFont()
        font.PointSize += 2
        font = font.Bold()
        self.title_lbl.SetFont(font)
        vbox.Add(self.title_lbl, 0, wx.LEFT | wx.TOP, 10)

        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, "Word", width=150)
        self.list_ctrl.InsertColumn(1, "Count", width=70)

        vbox.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(vbox)

    def update_list(self, items):
        self.list_ctrl.DeleteAllItems()
        for word, count in items:
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), word)
            self.list_ctrl.SetItem(index, 1, str(count))
