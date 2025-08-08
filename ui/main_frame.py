import wx
from utils.text_analysis import STOPWORDS
from ui.word_list_panel import WordListPanel
from ui.wordcloud_panel import WordCloudPanel
from ui.text_input_panel import TextInputPanel

class MainFrame(wx.Frame):
    def __init__(self, parent, title, size):
        super().__init__(parent, title=title, size=size)

        panel = wx.Panel(self)  # Root panel for the frame
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # This sizer splits the frame horizontally into two main sections:
        # left rail and main panel

        # --------------------------
        # Left rail vertical sizer: stacks elements vertically
        # --------------------------
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        # Wordcloud panel fixed size (small avatar)
        self.wordcloud_panel = WordCloudPanel(panel)
        left_sizer.Add(self.wordcloud_panel, 0, wx.ALL | wx.ALIGN_LEFT, 10)

        # Stopwords info label (bold)
        stopword_label = wx.StaticText(panel, label="Learn more about stopwords")
        font = stopword_label.GetFont()
        font.MakeBold()
        stopword_label.SetFont(font)
        left_sizer.Add(stopword_label, 0, wx.LEFT | wx.BOTTOM, 5)

        # Top Words panel
        self.top_nonstopwords_panel = WordListPanel(
            panel,
            title="Top Words",
            stopwords_tooltip_text="Ignores stopwords in analysis."
        )
        left_sizer.Add(self.top_nonstopwords_panel, 1, wx.EXPAND | wx.BOTTOM, 5)

        # Top Bigrams panel
        self.top_bigrams_panel = WordListPanel(
            panel,
            title="Top Bigrams",
            stopwords_tooltip_text="Phrases entirely composed of stopwords are excluded."
        )
        left_sizer.Add(self.top_bigrams_panel, 1, wx.EXPAND | wx.BOTTOM, 5)

        # Top Trigrams panel
        self.top_trigrams_panel = WordListPanel(
            panel,
            title="Top Trigrams",
            stopwords_tooltip_text="Phrases entirely composed of stopwords are excluded."
        )
        left_sizer.Add(self.top_trigrams_panel, 1, wx.EXPAND)

        # Add left rail sizer to main horizontal sizer
        # Proportion=0 means left rail uses minimal width based on content width
        main_sizer.Add(left_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # --------------------------
        # Main panel (right side): Text input panel that fills remaining horizontal space
        # --------------------------
        self.text_input_panel = TextInputPanel(panel, on_result_callback=self.on_text_processed)
        main_sizer.Add(self.text_input_panel, 1, wx.EXPAND | wx.ALL, 10)

        # --------------------------
        # Set sizer and layout
        # --------------------------
        panel.SetSizer(main_sizer)
        panel.Layout()

        self.SetMinSize((900, 600))
        self.Centre()
        self.Maximize(True)

    def on_text_processed(self, result, wx_image=None):
        # Update the word list panels on the left rail
        self.top_nonstopwords_panel.update_list(result['top_nonstopwords'])
        self.top_bigrams_panel.update_list(result['top_bigrams'])
        self.top_trigrams_panel.update_list(result['top_trigrams'])

        if wx_image:
            self.wordcloud_panel.set_wordcloud(wx_image)
