import wx
import re
from data.spacy_stopwords import STOPWORDS

class SentenceStartPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        title_label = wx.StaticText(self, label="Top Sentence Starters")
        font = title_label.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        title_label.SetFont(font)
        main_sizer.Add(title_label, 0, wx.EXPAND | wx.LEFT | wx.TOP, 0)
        
        # Add some spacing
        main_sizer.AddSpacer(5)
        
        # Content panel
        content_panel = wx.Panel(self)
        content_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create a list control to show top paragraphs
        self.paragraphs_list = wx.ListCtrl(content_panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.paragraphs_list.InsertColumn(0, 'Count', width=80)
        self.paragraphs_list.InsertColumn(1, 'Word', width=120)
        self.paragraphs_list.InsertColumn(2, 'Preview', width=200)
        
        # Add tooltip to explain usage
        self.paragraphs_list.SetToolTip("Double-click any row to view the full paragraph")
        
        # Make the list control expand to fill available space
        content_sizer.Add(self.paragraphs_list, 1, wx.EXPAND | wx.ALL, 5)
        
        # Ensure columns use full width
        self.paragraphs_list.Bind(wx.EVT_SIZE, self.on_resize)
        
        content_panel.SetSizer(content_sizer)
        # Make content panel expand to fill available vertical space
        main_sizer.Add(content_panel, 1, wx.EXPAND | wx.ALL, 5)
        
        # Add some spacing between panels
        main_sizer.AddSpacer(10)
        
        # Second panel for non-stopword results
        nonstopword_title = wx.StaticText(self, label="Top Sentence Starters (Non-Stopword)")
        nonstopword_font = nonstopword_title.GetFont()
        nonstopword_font.SetWeight(wx.FONTWEIGHT_BOLD)
        nonstopword_title.SetFont(nonstopword_font)
        main_sizer.Add(nonstopword_title, 0, wx.EXPAND | wx.LEFT | wx.TOP, 0)
        
        main_sizer.AddSpacer(5)
        
        # Non-stopword content panel
        nonstopword_content_panel = wx.Panel(self)
        nonstopword_content_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create a list control for non-stopword results
        self.nonstopword_paragraphs_list = wx.ListCtrl(nonstopword_content_panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.nonstopword_paragraphs_list.InsertColumn(0, 'Count', width=80)
        self.nonstopword_paragraphs_list.InsertColumn(1, 'Word', width=120)
        self.nonstopword_paragraphs_list.InsertColumn(2, 'Preview', width=200)
        
        # Add tooltip to explain usage
        self.nonstopword_paragraphs_list.SetToolTip("Double-click any row to view the full paragraph")
        
        # Make the list control expand to fill available space
        nonstopword_content_sizer.Add(self.nonstopword_paragraphs_list, 1, wx.EXPAND | wx.ALL, 5)
        
        # Ensure columns use full width
        self.nonstopword_paragraphs_list.Bind(wx.EVT_SIZE, self.on_nonstopword_resize)
        
        nonstopword_content_panel.SetSizer(nonstopword_content_sizer)
        main_sizer.Add(nonstopword_content_panel, 1, wx.EXPAND | wx.ALL, 5)
        
        # Store the current data
        self.top_paragraphs = []  # List of top 5 paragraph results
        self.top_nonstopword_paragraphs = []  # List of top non-stopword paragraph results
        
        self.SetSizer(main_sizer)
        
        # Set a minimum width to prevent text cropping
        self.SetMinSize((400, -1))  # Minimum width of 400 pixels, height flexible
        self.SetSize((400, -1))     # Set initial size to 400 pixels width
    
    def update_analysis(self, text):
        """Update the panel with new text analysis"""
        if not text.strip():
            self.paragraphs_list.DeleteAllItems()
            return
        
        # Find the top paragraphs with the most sentences starting with the same word
        self.top_paragraphs = self._find_top_paragraphs(text, top_n=50)
        
        # Find the top paragraphs with the most sentences starting with non-stopwords
        self.top_nonstopword_paragraphs = self._find_top_nonstopword_paragraphs(text, top_n=50)
        
        # Clear and populate the first list (all words)
        self.paragraphs_list.DeleteAllItems()
        for i, result in enumerate(self.top_paragraphs):
            if result:
                index = self.paragraphs_list.InsertItem(i, str(result["count"]))  # Count
                self.paragraphs_list.SetItem(index, 1, f'{result["word"]}')  # Word
                # Add preview text (truncated to fit column)
                preview_text = self._truncate_text(result["paragraph"], 50)
                self.paragraphs_list.SetItem(index, 2, preview_text)  # Preview
        
        # Clear and populate the second list (non-stopwords only)
        self.nonstopword_paragraphs_list.DeleteAllItems()
        for i, result in enumerate(self.top_nonstopword_paragraphs):
            if result:
                index = self.nonstopword_paragraphs_list.InsertItem(i, str(result["count"]))  # Count
                self.nonstopword_paragraphs_list.SetItem(index, 1, f'{result["word"]}')  # Word
                # Add preview text (truncated to fit column)
                preview_text = self._truncate_text(result["paragraph"], 50)
                self.nonstopword_paragraphs_list.SetItem(index, 2, preview_text)  # Preview
        
        # Bind double-click events to show paragraphs
        self.paragraphs_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_paragraph_selected)
        self.nonstopword_paragraphs_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_nonstopword_paragraph_selected)
    
    def _find_top_paragraphs(self, text, top_n=5):
        """Find the top N paragraphs with the most sentences starting with the same word"""
        # Split into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        paragraph_results = []
        
        for paragraph in paragraphs:
            # Split paragraph into sentences (simple approach)
            sentences = re.split(r'[.!?]+', paragraph)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            # Count sentences starting with each word
            word_counts = {}
            for sentence in sentences:
                # Get first word (case-insensitive)
                words = sentence.split()
                if words:
                    first_word = words[0].lower()
                    # Remove punctuation from first word
                    first_word = re.sub(r'[^\w\']', '', first_word)
                    if first_word:
                        word_counts[first_word] = word_counts.get(first_word, 0) + 1
            
            # Find the word with highest count in this paragraph
            if word_counts:
                max_word = max(word_counts, key=word_counts.get)
                max_count = word_counts[max_word]
                
                paragraph_results.append({
                    'word': max_word.title(),  # Capitalize for display
                    'count': max_count,
                    'paragraph': paragraph
                })
        
        # Sort by count (descending) and return top N
        paragraph_results.sort(key=lambda x: x['count'], reverse=True)
        # Return all results if we have fewer than top_n, otherwise return top_n
        return paragraph_results[:min(top_n, len(paragraph_results))]
    
    def _find_top_nonstopword_paragraphs(self, text, top_n=50):
        """Find the top N paragraphs with the most sentences starting with non-stopwords"""
        # Split into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        paragraph_results = []
        
        for paragraph in paragraphs:
            # Split paragraph into sentences (simple approach)
            sentences = re.split(r'[.!?]+', paragraph)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            # Count sentences starting with non-stopwords only
            word_counts = {}
            for sentence in sentences:
                # Get first word (case-insensitive)
                words = sentence.split()
                if words:
                    first_word = words[0].lower()
                    # Remove punctuation from first word
                    first_word = re.sub(r'[^\w\']', '', first_word)
                    if first_word and first_word not in STOPWORDS:
                        word_counts[first_word] = word_counts.get(first_word, 0) + 1
            
            # Find the word with highest count in this paragraph
            if word_counts:
                max_word = max(word_counts, key=word_counts.get)
                max_count = word_counts[max_word]
                
                paragraph_results.append({
                    'word': max_word.title(),  # Capitalize for display
                    'count': max_count,
                    'paragraph': paragraph
                })
        
        # Sort by count (descending) and return top N
        paragraph_results.sort(key=lambda x: x['count'], reverse=True)
        # Return all results if we have fewer than top_n, otherwise return top_n
        return paragraph_results[:min(top_n, len(paragraph_results))]
    
    def _truncate_text(self, text, max_chars=50):
        """Truncate text to fit in preview column, adding ellipsis if needed"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars-3] + "..."
    
    def on_paragraph_selected(self, event):
        """Show the full paragraph in a modal dialog when a list item is selected"""
        index = event.GetIndex()
        if 0 <= index < len(self.top_paragraphs):
            result = self.top_paragraphs[index]
            dlg = ParagraphDialog(self, result['word'], result['paragraph'])
            dlg.ShowModal()
            dlg.Destroy()
    
    def on_nonstopword_paragraph_selected(self, event):
        """Show the full paragraph in a modal dialog when a non-stopword list item is selected"""
        index = event.GetIndex()
        if 0 <= index < len(self.top_nonstopword_paragraphs):
            result = self.top_nonstopword_paragraphs[index]
            dlg = ParagraphDialog(self, result['word'], result['paragraph'])
            dlg.ShowModal()
            dlg.Destroy()
    
    def on_resize(self, event):
        """Handle resize events to adjust column widths"""
        width = self.paragraphs_list.GetSize().width
        # Give Count column 15%, Word column 25%, Preview column 60%
        self.paragraphs_list.SetColumnWidth(0, int(width * 0.15))
        self.paragraphs_list.SetColumnWidth(1, int(width * 0.25))
        self.paragraphs_list.SetColumnWidth(2, int(width * 0.60))
        event.Skip()
    
    def on_nonstopword_resize(self, event):
        """Handle resize events to adjust column widths for non-stopword panel"""
        width = self.nonstopword_paragraphs_list.GetSize().width
        # Give Count column 15%, Word column 25%, Preview column 60%
        self.nonstopword_paragraphs_list.SetColumnWidth(0, int(width * 0.15))
        self.nonstopword_paragraphs_list.SetColumnWidth(1, int(width * 0.25))
        self.nonstopword_paragraphs_list.SetColumnWidth(2, int(width * 0.60))
        event.Skip()


class ParagraphDialog(wx.Dialog):
    def __init__(self, parent, word, paragraph_text):
        super().__init__(parent, title=f'Paragraph with "{word}"', size=(600, 400))
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Header
        header_label = wx.StaticText(self, label=f'Paragraph containing "{word}" starting {self._count_sentences_starting_with(paragraph_text, word)} sentences:')
        header_font = header_label.GetFont()
        header_font.SetWeight(wx.FONTWEIGHT_BOLD)
        header_label.SetFont(header_font)
        main_sizer.Add(header_label, 0, wx.ALL, 10)
        
        # Paragraph text (read-only)
        self.text_ctrl = wx.TextCtrl(
            self, 
            value=paragraph_text, 
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP
        )
        main_sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        
        # Close button
        close_btn = wx.Button(self, label="Close")
        close_btn.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
        main_sizer.Add(close_btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        self.SetSizer(main_sizer)
    
    def _count_sentences_starting_with(self, text, word):
        """Count how many sentences in the text start with the given word"""
        sentences = re.split(r'[.!?]+', text)
        count = 0
        word_lower = word.lower()
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                first_word = sentence.split()[0].lower()
                first_word = re.sub(r'[^\w\']', '', first_word)
                if first_word == word_lower:
                    count += 1
        
        return count
