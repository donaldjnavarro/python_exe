import wx
import re
import unicodedata

def normalize_text(text):
    """Normalize text to handle curly quotes and accents"""
    normalized = unicodedata.normalize('NFKD', text)
    # Clean apostrophe variants
    return normalized.replace("’", "'")

class LongestParagraphsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        title_label = wx.StaticText(self, label="Longest Paragraphs")
        font = title_label.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        title_label.SetFont(font)
        main_sizer.Add(title_label, 0, wx.EXPAND | wx.LEFT | wx.TOP, 0)
        
        # Add some spacing
        main_sizer.AddSpacer(5)
        
        # Content panel
        content_panel = wx.Panel(self)
        content_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create a list control to show longest paragraphs
        self.paragraphs_list = wx.ListCtrl(content_panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.paragraphs_list.InsertColumn(0, 'Wordcount', width=80)
        self.paragraphs_list.InsertColumn(1, 'Preview', width=320)
        
        # Add tooltip to explain usage
        self.paragraphs_list.SetToolTip("Double-click any row to view the full paragraph")
        
        # Make the list control expand to fill available space
        content_sizer.Add(self.paragraphs_list, 1, wx.EXPAND | wx.ALL, 5)
        
        # Ensure columns use full width
        self.paragraphs_list.Bind(wx.EVT_SIZE, self.on_resize)
        
        content_panel.SetSizer(content_sizer)
        # Make content panel expand to fill available vertical space
        main_sizer.Add(content_panel, 1, wx.EXPAND | wx.ALL, 5)
        
        # Store the current data
        self.longest_paragraphs = []
        
        self.SetSizer(main_sizer)
        
        # Set a minimum width to prevent text cropping
        self.SetMinSize((400, -1))  # Minimum width of 400 pixels, height flexible
        self.SetSize((400, -1))     # Set initial size to 400 pixels width
    
    def update_analysis(self, text):
        """Update the panel with new text analysis"""
        if not text.strip():
            self.paragraphs_list.DeleteAllItems()
            return
        
        # Find the longest paragraphs by word count
        self.longest_paragraphs = self._find_longest_paragraphs(text, top_n=50)
        
        # Clear and populate the list
        self.paragraphs_list.DeleteAllItems()
        for i, result in enumerate(self.longest_paragraphs):
            if result:
                index = self.paragraphs_list.InsertItem(i, str(result["word_count"]))  # Count
                # Add preview text (truncated to fit column)
                preview_text = self._truncate_text(result["paragraph"], 80)
                self.paragraphs_list.SetItem(index, 1, preview_text)  # Preview
        
        # Bind double-click event to show paragraph
        self.paragraphs_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_paragraph_selected)
    
    def _find_longest_paragraphs(self, text, top_n=50):
        """Find the top N longest paragraphs by word count"""
        # Split into paragraphs
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        paragraph_results = []

        for paragraph in paragraphs:
            paragraph = normalize_text(paragraph)

            words = re.findall(r"\b\w+(?:'\w+)*\b", paragraph.lower())
            word_count = len(words)
            
            if word_count > 0:
                paragraph_results.append({
                    'word_count': word_count,
                    'paragraph': paragraph
                })

        # Sort by word count (descending) and return top N
        paragraph_results.sort(key=lambda x: x['word_count'], reverse=True)
        return paragraph_results[:min(top_n, len(paragraph_results))]
    
    def _truncate_text(self, text, max_chars=80):
        """Truncate text to fit in preview column, adding ellipsis if needed"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars-3] + "..."
    
    def on_paragraph_selected(self, event):
        """Show the full paragraph in a modal dialog when a list item is selected"""
        index = event.GetIndex()
        if 0 <= index < len(self.longest_paragraphs):
            result = self.longest_paragraphs[index]
            dlg = LongestParagraphDialog(self, result['word_count'], result['paragraph'])
            dlg.ShowModal()
            dlg.Destroy()
    
    def on_resize(self, event):
        """Handle resize events to adjust column widths"""
        width = self.paragraphs_list.GetSize().width
        # Give Count column 20%, Preview column 80%
        self.paragraphs_list.SetColumnWidth(0, int(width * 0.20))
        self.paragraphs_list.SetColumnWidth(1, int(width * 0.80))
        event.Skip()


class LongestParagraphDialog(wx.Dialog):
    def __init__(self, parent, word_count, paragraph_text):
        super().__init__(parent, title=f'Longest Paragraph ({word_count} words)', size=(600, 400))
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Header
        header_label = wx.StaticText(self, label=f'Paragraph with {word_count} words:')
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
