import wx
from utils.file_helpers import read_file_content
from utils.wordcloud_helper import generate_wordcloud_image
from ui.word_count_panel import WordCountPanel
from ui.word_list_panel import WordListPanel
from ui.wordcloud_panel import WordCloudPanel
from ui.text_paste_panel import TextPastePanel
from utils.text_analysis import STOPWORDS

class MainFrame(wx.Frame):
    def __init__(self, parent, title, size):
        super().__init__(parent, title=title, size=size)

        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # --- Info about Stopwords ---
        stopword_info_sizer = wx.BoxSizer(wx.HORIZONTAL)
        stopword_label = wx.StaticText(panel, label="Learn more about stopwords")
        font = stopword_label.GetFont()
        font.MakeBold()
        stopword_label.SetFont(font)

        help_icon = wx.StaticText(panel, label="?")
        help_font = help_icon.GetFont()
        help_font.MakeBold()
        help_icon.SetFont(help_font)
        help_icon.SetForegroundColour(wx.Colour(0, 102, 204))
        help_icon.SetToolTip("Click to see a full explanation of stopwords")
        help_icon.Bind(wx.EVT_LEFT_DOWN, self.show_stopwords_modal)

        stopword_info_sizer.Add(stopword_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        stopword_info_sizer.Add(help_icon, 0, wx.ALIGN_CENTER_VERTICAL)

        # Panels
        self.word_count_panel = WordCountPanel(panel)
        self.word_count_panel.update_count(0)

        # Helper to create WordListPanel with a title sizer that includes a question icon with tooltip
        def create_wordlist_panel_with_tooltip(parent, title, tooltip_text):
            container = wx.Panel(parent)
            container_sizer = wx.BoxSizer(wx.VERTICAL)
            container.SetSizer(container_sizer)

            # Title with label and icon
            title_sizer = wx.BoxSizer(wx.HORIZONTAL)

            title_label = wx.StaticText(container, label=title)
            font = title_label.GetFont()
            font.SetWeight(wx.FONTWEIGHT_BOLD)
            font.SetPointSize(font.GetPointSize() + 4)  # Increase font size
            title_label.SetFont(font)
            title_sizer.Add(title_label, 0, wx.ALIGN_CENTER_VERTICAL)

            icon_bmp = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_TOOLBAR, (16, 16))
            icon = wx.StaticBitmap(container, bitmap=icon_bmp)
            icon.SetToolTip(tooltip_text)
            title_sizer.Add(icon, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)

            container_sizer.Add(title_sizer, 0, wx.LEFT | wx.TOP, 2)

            # WordListPanel below title (no title)
            word_list_panel = WordListPanel(container, title="")
            container_sizer.Add(word_list_panel, 1, wx.EXPAND | wx.ALL, 2)

            return container, word_list_panel

        self.top_nonstopwords_panel_wrapped, self.top_nonstopwords_panel = create_wordlist_panel_with_tooltip(
            panel,
            "Top Words",
            "Ignores stopwords in analysis."
        )
        self.top_bigrams_panel_wrapped, self.top_bigrams_panel = create_wordlist_panel_with_tooltip(
            panel,
            "Top Bigrams",
            "Phrases entirely composed of stopwords are excluded."
        )
        self.top_trigrams_panel_wrapped, self.top_trigrams_panel = create_wordlist_panel_with_tooltip(
            panel,
            "Top Trigrams",
            "Phrases entirely composed of stopwords are excluded."
        )

        self.wordcloud_panel = WordCloudPanel(panel)

        # NEW: Text paste panel, alternate input method with callback
        self.text_paste_panel = TextPastePanel(panel, on_result_callback=self.on_text_processed)

        # Layout:
        content_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(self.text_paste_panel, 1, wx.EXPAND | wx.ALL, 10)
        left_sizer.Add(self.word_count_panel, 0, wx.EXPAND | wx.ALL, 10)

        lists_sizer = wx.BoxSizer(wx.VERTICAL)
        lists_sizer.Add(stopword_info_sizer, 0, wx.EXPAND | wx.BOTTOM, 5)  # added above top words
        lists_sizer.Add(self.top_nonstopwords_panel_wrapped, 1, wx.EXPAND | wx.BOTTOM, 5)
        lists_sizer.Add(self.top_bigrams_panel_wrapped, 1, wx.EXPAND | wx.BOTTOM, 5)
        lists_sizer.Add(self.top_trigrams_panel_wrapped, 1, wx.EXPAND)

        left_sizer.Add(lists_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        content_sizer.Add(left_sizer, 0, wx.EXPAND)
        content_sizer.Add(self.wordcloud_panel, 1, wx.EXPAND | wx.ALL, 10)

        main_sizer.Add(content_sizer, 1, wx.EXPAND)
        panel.SetSizer(main_sizer)
        panel.Layout()
        self.Layout()

        self.SetMinSize((800, 600))
        self.Centre()
        self.Maximize(True)

    def show_stopwords_modal(self, event):
        dlg = wx.Dialog(self, title="About Stopwords", size=(600, 500))  # bigger dialog
        vbox = wx.BoxSizer(wx.VERTICAL)

        text = (
            "Stopwords are very common words (like 'the', 'is', 'and') "
            "that are ignored in analysis to focus on more meaningful terms.\n\n"
            "In this app, the following words are treated as stopwords:\n\n"
            + ", ".join(sorted(STOPWORDS))
        )

        text_ctrl = wx.TextCtrl(dlg, value=text,
                                style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_NONE)
        vbox.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 10)

        btn_sizer = dlg.CreateStdDialogButtonSizer(wx.OK)
        vbox.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        dlg.SetSizer(vbox)
        dlg.Layout()
        dlg.ShowModal()
        dlg.Destroy()

    def on_open_file(self, event):
        path = self.show_file_dialog()
        if not path:
            return
        try:
            content = read_file_content(path)
        except Exception as e:
            wx.MessageBox(f"Error reading file:\n{e}", "Error", wx.ICON_ERROR)
            return
        self.text_paste_panel.set_text_and_process(content)

    def on_text_processed(self, result, wx_image):
        self._update_ui_from_result(result, wx_image)

    def _update_ui_from_result(self, result, wx_image=None):
        self.word_count_panel.update_count(result['total_words'])
        self.top_nonstopwords_panel.update_list(result['top_nonstopwords'])
        self.top_bigrams_panel.update_list(result['top_bigrams'])
        self.top_trigrams_panel.update_list(result['top_trigrams'])

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
