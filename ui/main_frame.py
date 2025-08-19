import wx
import re
from ui.word_list_panel import WordListPanel
from ui.wordcloud_panel import WordCloudPanel
from ui.text_input_panel import TextInputPanel
from ui.stop_words_dialog import StopwordsInfoDialog
from ui.sentence_start_panel import SentenceStartPanel
from ui.longest_paragraphs_panel import LongestParagraphsPanel
from ui.text_metrics_panel import TextMetricsPanel
from ui.dialogue_panel import DialogueNarrationPanel
class MainFrame(wx.Frame):
    """Main application window: left rail, center text input, right rail."""
    def __init__(self, parent, title="Text Analysis", size=(1200, 600)):
        super().__init__(parent, title=title, size=size)

        self.panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Left, center, right sections
        main_sizer.Add(self._build_left_rail(), 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(self._build_center_panel(), 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(self._build_right_rail(), 0, wx.EXPAND | wx.ALL, 10)

        self.panel.SetSizer(main_sizer)
        self.panel.Layout()

        self.SetMinSize((1200, 600))
        self.Centre()
        self.Maximize(True)

    # --------------------------
    # Left Rail
    # --------------------------
    def _build_left_rail(self):
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        # Wordcloud panel at top — give minimum size to ensure visibility
        self.wordcloud_panel = WordCloudPanel(self.panel)
        self.wordcloud_panel.SetMinSize((400, 300))  # crucial: prevents collapse
        left_sizer.Add(self.wordcloud_panel, 0, wx.EXPAND | wx.ALL, 0)

        # Stopwords info button
        info_btn = wx.Button(self.panel, label="Learn more about stopwords")
        info_btn.SetToolTip("Click for details about stopwords")
        info_btn.Bind(wx.EVT_BUTTON, self.on_show_stopwords_modal)
        left_sizer.Add(info_btn, 0, wx.EXPAND | wx.ALL, 5)

        # Bottom tables container — takes all remaining vertical space
        tables_panel = wx.Panel(self.panel)
        table_sizer = wx.BoxSizer(wx.VERTICAL)

        self.top_nonstopwords_panel = WordListPanel(
            tables_panel, "Top Words",
            "Ignores stopwords in analysis.", False
        )
        table_sizer.Add(self.top_nonstopwords_panel, 1, wx.EXPAND | wx.BOTTOM, 5)

        self.top_bigrams_panel = WordListPanel(
            tables_panel, "Top Bigrams",
            "Phrases entirely composed of stopwords are excluded.", False
        )
        table_sizer.Add(self.top_bigrams_panel, 1, wx.EXPAND | wx.BOTTOM, 5)

        self.top_trigrams_panel = WordListPanel(
            tables_panel, "Top Trigrams",
            "Phrases entirely composed of stopwords are excluded.", False
        )
        table_sizer.Add(self.top_trigrams_panel, 1, wx.EXPAND)

        tables_panel.SetSizer(table_sizer)
        left_sizer.Add(tables_panel, 1, wx.EXPAND | wx.BOTTOM, 10)

        return left_sizer

    # --------------------------
    # Center Panel
    # --------------------------
    def _build_center_panel(self):
        self.text_input_panel = TextInputPanel(self.panel, on_result_callback=self.on_text_processed)
        return self.text_input_panel

    # --------------------------
    # Right Rail
    # --------------------------
    def _build_right_rail(self):
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        # Metrics container — protects its space
        metrics_container = wx.Panel(self.panel)
        metrics_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_metrics_panel = TextMetricsPanel(metrics_container)
        metrics_sizer.Add(self.text_metrics_panel, 1, wx.EXPAND)
        metrics_container.SetSizer(metrics_sizer)
        metrics_container.SetMinSize((-1, 220))  # slightly taller to prevent cutting off
        right_sizer.Add(metrics_container, 0, wx.EXPAND | wx.ALL, 10)

        # Stretch spacer pushes bottom panels down
        right_sizer.AddStretchSpacer(1)
        
        # Dialogue panel
        self.dialogue_panel = DialogueNarrationPanel(self.panel)
        right_sizer.Add(self.dialogue_panel, 0, wx.EXPAND | wx.ALL, 10)


        # Sentence Start panel (bottom)
        self.sentence_start_panel = SentenceStartPanel(self.panel)
        right_sizer.Add(self.sentence_start_panel, 1, wx.EXPAND | wx.ALL, 10)

        # Longest Paragraphs panel (bottom)
        self.longest_paragraphs_panel = LongestParagraphsPanel(self.panel)
        right_sizer.Add(self.longest_paragraphs_panel, 1, wx.EXPAND | wx.ALL, 10)

        return right_sizer

    # --------------------------
    # Event Handlers
    # --------------------------
    def on_show_stopwords_modal(self, event):
        dlg = StopwordsInfoDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    # --------------------------
    # Text Processing / Metrics
    # --------------------------
    def on_text_processed(self, result, wx_image=None):
        """Update all panels with processed text and metrics."""

        # Total words (in right rail metrics)
        total_words = result.get('total_words', 0)

        # Tables
        self.top_nonstopwords_panel.update_list(result.get('top_nonstopwords', []))
        self.top_bigrams_panel.update_list(result.get('top_bigrams', []))
        self.top_trigrams_panel.update_list(result.get('top_trigrams', []))

        # Get text
        text = result.get('original_text')
        if not text and hasattr(self.text_input_panel, 'get_text'):
            text = self.text_input_panel.get_text()

        if text:
            # Update panels
            self.sentence_start_panel.update_analysis(text)
            self.longest_paragraphs_panel.update_analysis(text)

            # --------------------------
            # Compute metrics
            # --------------------------
            # Split sentences safely for ellipses etc.
            sentence_list = [s.strip() for s in re.split(r'(?<!\.)[.!?]+(?!\.)', text) if s.strip()]
            num_sentences = len(sentence_list)
            sentence_lengths = [len(s.split()) for s in sentence_list]
            avg_sentence_len = round(sum(sentence_lengths) / num_sentences, 1) if num_sentences > 0 else 0
            longest_sentence_len = max(sentence_lengths) if sentence_lengths else 0

            paragraph_list = [p.strip() for p in text.split('\n') if p.strip()]
            num_paragraphs = len(paragraph_list)
            paragraph_lengths = [len(p.split()) for p in paragraph_list]
            avg_paragraph_len = round(sum(paragraph_lengths) / num_paragraphs, 1) if num_paragraphs > 0 else 0
            longest_paragraph_len = max(paragraph_lengths) if paragraph_lengths else 0

            # --------------------------
            # Compute dialogue vs narration
            # --------------------------
            # Match quoted text as dialogue
            dialogue_matches = re.findall(r'“.*?”|".*?"', text)
            dialogue_words = sum(len(d.split()) for d in dialogue_matches)
            narration_words = total_words - dialogue_words

            # Update the dialogue panel
            self.dialogue_panel.update_counts(dialogue_words, narration_words)

            # --------------------------
            # Update metrics panel
            # --------------------------
            metrics = {
                "Total Words": f"{total_words:,} words",
                "Sentences": "Sentences",
                "Total Sentences": f"{num_sentences:,} sentences",
                "Average Sentence Length": f"{avg_sentence_len} average words per sentence",
                "Longest Sentence": f"{longest_sentence_len:,} words in the longest sentence",
                "Paragraphs": "Paragraphs",
                "Total Paragraphs": f"{num_paragraphs:,} paragraphs",
                "Average Paragraph Length": f"{avg_paragraph_len} average words per paragraph",
                "Longest Paragraph": f"{longest_paragraph_len:,} words in the longest paragraph"
            }
            self.text_metrics_panel.update_metrics(metrics)

        # Wordcloud
        if wx_image:
            self.wordcloud_panel.set_wordcloud(wx_image)
