from wordcloud import WordCloud
import wx
import io

def generate_wordcloud_image(word_counts, width=1600, height=1200):
    """
    Generate a word cloud image at a higher base resolution for better scaling.
    """
    wc = WordCloud(width=width, height=height, background_color='white')
    wc.generate_from_frequencies(word_counts)

    # Convert to wx.Image
    image = wc.to_image()
    output = io.BytesIO()
    image.save(output, format='PNG')
    output.seek(0)
    wx_image = wx.Image(output)
    return wx_image
