import wx
from utils.file_helpers import read_file_content

class MainFrame(wx.Frame):
    def __init__(self, parent, title, size):
        super().__init__(parent, title=title, size=size)
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.open_btn = wx.Button(panel, label="Open TXT or PDF file")
        self.open_btn.Bind(wx.EVT_BUTTON, self.on_open_file)
        vbox.Add(self.open_btn, flag=wx.ALL|wx.CENTER, border=10)

        self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        vbox.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def on_open_file(self, event):
        wildcard = "Text files (*.txt)|*.txt|PDF files (*.pdf)|*.pdf"
        dialog = wx.FileDialog(self, "Open TXT or PDF file", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()
        try:
            content = read_file_content(path)
        except Exception as e:
            wx.MessageBox(f"Error reading file:\n{e}", "Error", wx.ICON_ERROR)
            return

        self.text_ctrl.SetValue(content)
