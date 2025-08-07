import wx
from utils.file_helpers import read_file_content
from utils.text_analysis import analyze_text
from utils.wordcloud_helper import generate_wordcloud_image

from ui.word_count_panel import WordCountPanel
from ui.word_list_panel import WordListPanel
from ui.wordcloud_panel import WordCloudPanel

class MainFrame(wx.Frame):
    def __init__(self, parent, title, size):
        super().__init__(parent, title=title, size=size)

        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Panels
        self.open_btn = wx.Button(panel, label="Open file")
        self.open_btn.Bind(wx.EVT_BUTTON, self.on_open_file)

        self.word_count_panel = WordCountPanel(panel)
        self.word_count_panel.update_count(0)
        self.top_nonstopwords_panel = WordListPanel(panel, title="Top 10 Words")
        self.top_stopwords_panel = WordListPanel(panel, title="Top 10 Stopwords")
        self.wordcloud_panel = WordCloudPanel(panel)

        # New layout: horizontal sizer for main content below the button
        content_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Left vertical stack: button on top + word count panel + word lists
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(self.open_btn, 0, wx.ALL | wx.ALIGN_LEFT, 10)  # button tucked top-left
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

        # Analyze text
        result = analyze_text(content)

        # Update UI panels
        self.word_count_panel.update_count(result['total_words'])
        self.top_nonstopwords_panel.update_list(result['top_nonstopwords'])
        self.top_stopwords_panel.update_list(result['top_stopwords'])

        # Generate and update word cloud
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
