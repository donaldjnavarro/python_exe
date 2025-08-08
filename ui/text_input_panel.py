import wx
from utils.file_helpers import read_file_content
from utils.text_analysis import analyze_text
from utils.wordcloud_helper import generate_wordcloud_image

class TextInputPanel(wx.Panel):
    def __init__(self, parent, on_result_callback=None):
        super().__init__(parent)
        self.on_result_callback = on_result_callback
        self.current_path = None

        main_sizer = wx.BoxSizer(wx.VERTICAL)  # Stack vertically

        label = wx.StaticText(self, label="Input text or open a file")
        main_sizer.Add(label, 0, wx.ALL, 5)

        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
        main_sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.open_btn = wx.Button(self, label="Open")
        self.open_btn.Bind(wx.EVT_BUTTON, self.on_open)
        btn_sizer.Add(self.open_btn, 0, wx.ALL, 5)

        self.save_btn = wx.Button(self, label="Save")
        self.save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        btn_sizer.Add(self.save_btn, 0, wx.ALL, 5)

        self.process_btn = wx.Button(self, label="Process Text")
        self.process_btn.Bind(wx.EVT_BUTTON, self.on_process)
        btn_sizer.Add(self.process_btn, 0, wx.ALL, 5)

        main_sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT)

        self.SetSizer(main_sizer)

    def set_text_and_process(self, text, path=None):
        self.text_ctrl.SetValue(text)
        self.current_path = path
        self.on_process()

    def on_open(self, event):
        with wx.FileDialog(self, "Open Text File", wildcard="Text files (*.txt)|*.txt|All files|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            path = dlg.GetPath()
            try:
                content = read_file_content(path)
                self.set_text_and_process(content, path)
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
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            path = dlg.GetPath()
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(self.text_ctrl.GetValue())
                self.current_path = path
                wx.MessageBox("File saved successfully.", "Info", wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Failed to save file:\n{e}", "Error", wx.ICON_ERROR)

    def on_process(self, event=None):
        text = self.text_ctrl.GetValue()
        if not text.strip():
            wx.MessageBox("Please enter or open some text first.", "Info", wx.ICON_INFORMATION)
            return
        try:
            result = analyze_text(text)
            wx_image = generate_wordcloud_image(result['nonstopword_counts'])
        except Exception as e:
            wx.MessageBox(f"Error processing text:\n{e}", "Error", wx.ICON_ERROR)
            return

        if self.on_result_callback:
            self.on_result_callback(result, wx_image)
