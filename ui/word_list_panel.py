import wx
import wx.html
import html as _html
import re

class WordListPanel(wx.Panel):
    def __init__(self, parent, title="", stopwords_tooltip_text=None, click_to_open_modal=False):
        """
        Word list panel with optional inline help.
        If `stopwords_tooltip_text` is provided:
          - The small question-mark icon will show a short hover tooltip.
          - If `click_to_open_modal` is True, clicking the icon opens a modal dialog rendering the full text.
          - In the dialog, **double-asterisk** markup (e.g. **stopwords**) will be rendered bold.
        """
        super().__init__(parent)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Title sizer with label + optional question mark icon
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.title_label = wx.StaticText(self, label=title)
        font = self.title_label.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.title_label.SetFont(font)

        title_sizer.Add(self.title_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 0)

        # If help text provided, add an icon with a short tooltip and optional click to show modal
        self._help_text = stopwords_tooltip_text
        if stopwords_tooltip_text:
            # Use a standard question icon
            icon_bmp = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_TOOLBAR, (16, 16))
            icon = wx.StaticBitmap(self, bitmap=icon_bmp)

            # Set the tooltip to the short text
            icon.SetToolTip(stopwords_tooltip_text)

            # Bind click event only if enabled
            if click_to_open_modal:
                icon.Bind(wx.EVT_LEFT_DOWN, lambda evt: self._show_help_dialog())

            title_sizer.Add(icon, 0, wx.ALIGN_CENTER_VERTICAL)

        main_sizer.Add(title_sizer, 0, wx.LEFT | wx.TOP, 0)

        # List control for showing words and counts
        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'Word', width=140)
        self.list_ctrl.InsertColumn(1, 'Count', width=70)

        main_sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(main_sizer)

    def update_list(self, word_count_list):
        """Populate the list control with (word, count) tuples."""
        self.list_ctrl.DeleteAllItems()
        for word, count in word_count_list:
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(word))
            self.list_ctrl.SetItem(index, 1, str(count))

    # ---------- Internal helper to show the formatted modal ----------
    def _show_help_dialog(self):
        """
        Shows a modal dialog rendering the `stopwords_tooltip_text`.
        Supports **bold** using double-asterisk markup.
        """
        if not self._help_text:
            return

        # Convert plain text with **bold** markers into safe HTML
        safe = _html.escape(self._help_text)

        # Convert **bold** markup to <b>...</b>
        html_with_bold = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', safe, flags=re.DOTALL)

        # Convert newlines to <br/>
        html_with_breaks = html_with_bold.replace('\n', '<br/>')

        # Wrap in minimal HTML, choose a readable font size
        html_content = (
            "<html><body style='font-family: system-ui, -apple-system, "
            "Segoe UI, Roboto, Arial, sans-serif; font-size:11pt; color:#222;'>"
            f"{html_with_breaks}"
            "</body></html>"
        )

        # Create dialog
        dlg = wx.Dialog(self.GetTopLevelParent() or self, title="Details", size=(520, 420))
        dlg_sizer = wx.BoxSizer(wx.VERTICAL)

        html_win = wx.html.HtmlWindow(dlg, style=wx.html.HW_SCROLLBAR_AUTO)
        try:
            html_win.SetPage(html_content)
        except Exception:
            fallback = wx.TextCtrl(dlg, value=self._help_text, style=wx.TE_MULTILINE | wx.TE_READONLY)
            dlg_sizer.Add(fallback, 1, wx.EXPAND | wx.ALL, 8)
        else:
            dlg_sizer.Add(html_win, 1, wx.EXPAND | wx.ALL, 8)

        btns = dlg.CreateStdDialogButtonSizer(wx.OK)
        dlg_sizer.Add(btns, 0, wx.ALIGN_CENTER | wx.ALL, 8)

        dlg.SetSizer(dlg_sizer)
        dlg.ShowModal()
        dlg.Destroy()
