import wx
import threading
from utils.text_analysis import analyze_text
from utils.wordcloud_helper import generate_wordcloud_image

class TextPastePanel(wx.Panel):
    """
    Panel for pasting large text and processing it asynchronously.
    This is an ALTERNATE input method to file upload.
    """

    def __init__(self, parent, on_result_callback):
        """
        :param parent: wx parent window
        :param on_result_callback: function(result_dict) called when processing done
        """
        super().__init__(parent)

        self.on_result_callback = on_result_callback

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Instruction label
        label = wx.StaticText(self, label="Paste your text below (large text supported):")
        vbox.Add(label, 0, wx.ALL, 5)

        # Large multiline text input
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_RICH2)
        vbox.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        # Process button
        self.process_btn = wx.Button(self, label="Process Text")
        self.process_btn.Bind(wx.EVT_BUTTON, self.on_process_click)
        vbox.Add(self.process_btn, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        # Status label for feedback
        self.status_label = wx.StaticText(self, label="")
        vbox.Add(self.status_label, 0, wx.ALL, 5)

        self.SetSizer(vbox)

    def on_process_click(self, event):
        text = self.text_ctrl.GetValue().strip()
        if not text:
            wx.MessageBox("Please paste some text before processing.", "No Text", wx.ICON_WARNING)
            return

        # Disable controls while processing
        self.process_btn.Disable()
        self.text_ctrl.Disable()
        self.status_label.SetLabel("Processing... please wait.")

        # Start background thread to avoid freezing UI
        thread = threading.Thread(target=self._process_text, args=(text,), daemon=True)
        thread.start()

    def _process_text(self, text):
        try:
            # Run your analysis (can be slow for big text)
            result = analyze_text(text)

            # Generate word cloud wx.Image (may take some time)
            wx_image = generate_wordcloud_image(result['nonstopword_counts'])

            # We need to update UI on main thread, so use CallAfter
            wx.CallAfter(self._processing_done, result, wx_image)
        except Exception as e:
            wx.CallAfter(self._processing_error, str(e))

    def _processing_done(self, result, wx_image):
        # Re-enable controls
        self.process_btn.Enable()
        self.text_ctrl.Enable()
        self.status_label.SetLabel("Processing complete.")

        # Callback to parent with the result dict and image
        if callable(self.on_result_callback):
            self.on_result_callback(result, wx_image)

    def _processing_error(self, error_msg):
        self.process_btn.Enable()
        self.text_ctrl.Enable()
        self.status_label.SetLabel("")

        wx.MessageBox(f"Error during processing:\n{error_msg}", "Error", wx.ICON_ERROR)
