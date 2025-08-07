import wx
from utils.file_helpers import read_file_content
from utils.text_analysis import analyze_text
from utils.wordcloud_helper import generate_wordcloud_image

class TextPastePanel(wx.Panel):
    def __init__(self, parent, on_result_callback=None):
        super().__init__(parent)
        self.on_result_callback = on_result_callback

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, label="Input text or import a file with text")
        main_sizer.Add(label, 0, wx.ALL, 5)

        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
        main_sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        # Horizontal sizer for buttons side-by-side
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.import_btn = wx.Button(self, label="Import Text")
        self.import_btn.Bind(wx.EVT_BUTTON, self.on_import)
        btn_sizer.Add(self.import_btn, 0, wx.ALL, 5)

        self.process_btn = wx.Button(self, label="Process Text")
        self.process_btn.Bind(wx.EVT_BUTTON, self.on_process)
        btn_sizer.Add(self.process_btn, 0, wx.ALL, 5)

        main_sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT)

        self.SetSizer(main_sizer)

    def set_text_and_process(self, text):
        """
        Set text and immediately process it (used by MainFrame when importing file)
        """
        self.text_ctrl.SetValue(text)
        self.on_process()

    def on_process(self, event=None):
        """
        Analyze the pasted text and call the callback with results
        """
        text = self.text_ctrl.GetValue()
        if not text.strip():
            wx.MessageBox("Please enter or import some text first.", "Info", wx.ICON_INFORMATION)
            return

        try:
            result = analyze_text(text)
            wx_image = generate_wordcloud_image(result['nonstopword_counts'])
        except Exception as e:
            wx.MessageBox(f"Error processing text:\n{e}", "Error", wx.ICON_ERROR)
            return

        if self.on_result_callback:
            self.on_result_callback(result, wx_image)

    def on_import(self, event):
        """
        Open a file dialog, read the file content and set it into the text box, then process it.
        """
        wildcard = ("Text files (*.txt)|*.txt|"
                    "PDF files (*.pdf)|*.pdf|"
                    "Word documents (*.docx)|*.docx|"
                    "Rich Text Format (*.rtf)|*.rtf")

        with wx.FileDialog(self, "Import text from file", wildcard=wildcard,
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return  # User cancelled

            path = dlg.GetPath()
            try:
                content = read_file_content(path)
            except Exception as e:
                wx.MessageBox(f"Error reading file:\n{e}", "Error", wx.ICON_ERROR)
                return

            self.set_text_and_process(content)
