import wx
from utils.text_analysis import STOPWORDS
from ui.word_list_panel import WordListPanel
from ui.wordcloud_panel import WordCloudPanel
from ui.text_input_panel import TextInputPanel
from ui.stop_words_dialog import StopwordsInfoDialog
from ui.sentence_start_panel import SentenceStartPanel

class MainFrame(wx.Frame):
    def __init__(self, parent, title, size):
        super().__init__(parent, title=title, size=size)

        panel = wx.Panel(self)  # Root panel for the frame
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # --------------------------
        # Left rail vertical sizer: stacks elements vertically
        # --------------------------
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        # Wordcloud panel fixed size (small avatar)
        self.wordcloud_panel = WordCloudPanel(panel)
        left_sizer.Add(self.wordcloud_panel, 0, wx.ALL | wx.ALIGN_LEFT, 10)

        # Stopwords info button (gray default style)
        info_btn = wx.Button(panel, label="Learn more about stopwords")
        info_btn.SetToolTip("Click for details about stopwords")
        info_btn.Bind(wx.EVT_BUTTON, self.on_show_stopwords_modal)

        left_sizer.Add(info_btn, 0, wx.LEFT | wx.BOTTOM | wx.EXPAND, 5)

        # Top Words panel — tooltip only, no modal on icon click
        self.top_nonstopwords_panel = WordListPanel(
            panel,
            title="Top Words",
            stopwords_tooltip_text="Ignores stopwords in analysis.",
            click_to_open_modal=False,
        )
        left_sizer.Add(self.top_nonstopwords_panel, 1, wx.EXPAND | wx.BOTTOM, 5)

        # Top Bigrams panel — tooltip only, no modal on icon click
        self.top_bigrams_panel = WordListPanel(
            panel,
            title="Top Bigrams",
            stopwords_tooltip_text="Phrases entirely composed of stopwords are excluded.",
            click_to_open_modal=False,
        )
        left_sizer.Add(self.top_bigrams_panel, 1, wx.EXPAND | wx.BOTTOM, 5)

        # Top Trigrams panel — tooltip only, no modal on icon click
        self.top_trigrams_panel = WordListPanel(
            panel,
            title="Top Trigrams",
            stopwords_tooltip_text="Phrases entirely composed of stopwords are excluded.",
            click_to_open_modal=False,
        )
        left_sizer.Add(self.top_trigrams_panel, 1, wx.EXPAND)

        # Add left rail sizer to main horizontal sizer
        main_sizer.Add(left_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # --------------------------
        # Main panel (center): Text input panel that fills remaining horizontal space
        # --------------------------
        self.text_input_panel = TextInputPanel(panel, on_result_callback=self.on_text_processed)
        main_sizer.Add(self.text_input_panel, 1, wx.EXPAND | wx.ALL, 10)

        # --------------------------
        # Right rail vertical sizer: stacks elements vertically
        # --------------------------
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        # Sentence Start Champion panel
        self.sentence_start_panel = SentenceStartPanel(panel)
        right_sizer.Add(self.sentence_start_panel, 1, wx.EXPAND | wx.ALL, 10)

        # Add right rail sizer to main horizontal sizer - give it more space
        main_sizer.Add(right_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # --------------------------
        # Set sizer and layout
        # --------------------------
        panel.SetSizer(main_sizer)
        panel.Layout()

        self.SetMinSize((1200, 600))
        self.Centre()
        self.Maximize(True)

    def on_show_stopwords_modal(self, event):
        dlg = StopwordsInfoDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    def on_text_processed(self, result, wx_image=None):
        self.top_nonstopwords_panel.update_list(result['top_nonstopwords'])
        self.top_bigrams_panel.update_list(result['top_bigrams'])
        self.top_trigrams_panel.update_list(result['top_trigrams'])

        # Update the sentence start panel with the original text
        if 'original_text' in result:
            self.sentence_start_panel.update_analysis(result['original_text'])
        elif hasattr(self.text_input_panel, 'get_text'):
            # Fallback: try to get text from the input panel
            text = self.text_input_panel.get_text()
            if text:
                self.sentence_start_panel.update_analysis(text)

        if wx_image:
            self.wordcloud_panel.set_wordcloud(wx_image)
