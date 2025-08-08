import wx
import os

class EditableTextDialog(wx.Dialog):
    def __init__(self, parent, title="Edit Text", size=(800, 600)):
        super().__init__(parent, title=title, size=size)

        self.current_path = None

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Toolbar buttons
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_open = wx.Button(self, label="Open")
        self.btn_save = wx.Button(self, label="Save")
        self.btn_save_as = wx.Button(self, label="Save As")
        hbox_buttons.Add(self.btn_open, 0, wx.ALL, 5)
        hbox_buttons.Add(self.btn_save, 0, wx.ALL, 5)
        hbox_buttons.Add(self.btn_save_as, 0, wx.ALL, 5)
        vbox.Add(hbox_buttons, 0, wx.LEFT, 5)

        # Editable multi-line text control with scrollbars
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
        vbox.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        # Close button
        btns = self.CreateStdDialogButtonSizer(wx.CANCEL | wx.OK)
        vbox.Add(btns, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(vbox)

        # Bind events
        self.btn_open.Bind(wx.EVT_BUTTON, self.on_open)
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        self.btn_save_as.Bind(wx.EVT_BUTTON, self.on_save_as)

    def on_open(self, event):
        with wx.FileDialog(self, "Open Text File", wildcard="Text files (*.txt)|*.txt|All files|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
                self.text_ctrl.SetValue(text)
                self.current_path = path
                self.SetTitle(f"Edit Text - {os.path.basename(path)}")
            except Exception as e:
                wx.MessageBox(f"Failed to open file:\n{e}", "Error", wx.ICON_ERROR)

    def on_save(self, event):
        if self.current_path:
            try:
                with open(self.current_path, 'w', encoding='utf-8') as f:
                    f.write(self.text_ctrl.GetValue())
                wx.MessageBox("File saved successfully.", "Info", wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Failed to save file:\n{e}", "Error", wx.ICON_ERROR)
        else:
            self.on_save_as(event)

    def on_save_as(self, event):
        with wx.FileDialog(self, "Save Text File", wildcard="Text files (*.txt)|*.txt|All files|*.*",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(self.text_ctrl.GetValue())
                self.current_path = path
                self.SetTitle(f"Edit Text - {os.path.basename(path)}")
                wx.MessageBox("File saved successfully.", "Info", wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Failed to save file:\n{e}", "Error", wx.ICON_ERROR)
