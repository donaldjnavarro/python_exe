from wordcloud import WordCloud
import wx
import io

def generate_wordcloud_image(word_counts, width=400, height=300):
    # Create WordCloud with some enhanced styling options
    wc = WordCloud(
        width=width,
        height=height,
        background_color='white',    # Background color of the image
        max_words=150,               # Maximum number of words to show
        colormap='plasma',           # Use 'plasma' colormap for vibrant colors
        contour_color='steelblue',   # Optional: contour color around the word cloud
        contour_width=1,             # Width of the contour line
        random_state=42              # Fix random seed for reproducibility
        # You can add 'mask=...' here to shape the word cloud if you want
        # e.g., mask=np.array(Image.open("mask.png"))
    )
    wc.generate_from_frequencies(word_counts)

    # Convert PIL image to wx.Image for display in wxPython
    image = wc.to_image()

    output = io.BytesIO()
    image.save(output, format='PNG')
    output.seek(0)
    wx_image = wx.Image(output)

    return wx_image
