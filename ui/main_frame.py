import wx
from utils.file_helpers import read_file_content
from utils.wordcloud_helper import generate_wordcloud_image

from ui.word_count_panel import WordCountPanel
from ui.word_list_panel import WordListPanel
from ui.wordcloud_panel import WordCloudPanel
from ui.text_paste_panel import TextPastePanel  # NEW import


class MainFrame(wx.Frame):
    def __init__(self, parent, title, size):
        super().__init__(parent, title=title, size=size)

        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Panels
        self.word_count_panel = WordCountPanel(panel)
        self.word_count_panel.update_count(0)
        self.top_nonstopwords_panel = WordListPanel(panel, title="Top 10 Words")
        self.top_stopwords_panel = WordListPanel(panel, title="Top 10 Stopwords")
        self.wordcloud_panel = WordCloudPanel(panel)

        # NEW: Text paste panel, alternate input method with callback
        self.text_paste_panel = TextPastePanel(panel, on_result_callback=self.on_text_processed)

        # Layout:

        # Horizontal sizer for main content below inputs
        content_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Left vertical stack: text paste panel, word count, and lists
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(self.text_paste_panel, 1, wx.EXPAND | wx.ALL, 10)  # text paste panel includes Import and Process buttons
        left_sizer.Add(self.word_count_panel, 0, wx.EXPAND | wx.ALL, 10)

        lists_sizer = wx.BoxSizer(wx.VERTICAL)
        lists_sizer.Add(self.top_nonstopwords_panel, 1, wx.EXPAND | wx.BOTTOM, 5)
        lists_sizer.Add(self.top_stopwords_panel, 1, wx.EXPAND)
        left_sizer.Add(lists_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        content_sizer.Add(left_sizer, 0, wx.EXPAND)

        # Word cloud panel takes remaining space on the right
        content_sizer.Add(self.wordcloud_panel, 1, wx.EXPAND | wx.ALL, 10)

        main_sizer.Add(content_sizer, 1, wx.EXPAND)

        panel.SetSizer(main_sizer)
        panel.Layout()
        self.Layout()

        self.SetMinSize((800, 600))   # set a comfortable minimum size
        self.Centre()
        self.Maximize(True)           # start maximized

    def on_open_file(self, event):
        path = self.show_file_dialog()
        if not path:
            return
        try:
            content = read_file_content(path)
        except Exception as e:
            wx.MessageBox(f"Error reading file:\n{e}", "Error", wx.ICON_ERROR)
            return

        # Instead of analyzing here, put content into paste panel and process from there:
        self.text_paste_panel.set_text_and_process(content)

    def on_text_processed(self, result, wx_image):
        # This is the callback from the TextPastePanel when user pastes & processes text
        self._update_ui_from_result(result, wx_image)

    def _update_ui_from_result(self, result, wx_image=None):
        self.word_count_panel.update_count(result['total_words'])
        self.top_nonstopwords_panel.update_list(result['top_nonstopwords'])
        self.top_stopwords_panel.update_list(result['top_stopwords'])

        if wx_image is None:
            wx_image = generate_wordcloud_image(result['nonstopword_counts'])
        self.wordcloud_panel.update_wordcloud(wx_image)

    def show_file_dialog(self):
        wildcard = ("Text files (*.txt)|*.txt|"
                    "PDF files (*.pdf)|*.pdf|"
                    "Word documents (*.docx)|*.docx|"
                    "Rich Text Format (*.rtf)|*.rtf")
        dlg = wx.FileDialog(self, "Open file", wildcard=wildcard,
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_CANCEL:
            dlg.Destroy()
            return None
        path = dlg.GetPath()
        dlg.Destroy()
        return path
