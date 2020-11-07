import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

mask = np.array(Image.open('earth.jpg'))

with open('titlesfixed.txt', 'r') as f:
        title_data = f.read()
 
def make_cloud(wordcloud):
        plt.figure(figsize=(60, 30))
        plt.imshow(wordcloud)
        plt.tight_layout(pad=0)
        plt.axis('off');
        wordcloud.to_file('newcloud.png')

wordcloud = WordCloud(max_font_size=25, 
                      max_words=len(title_data), random_state=3, collocations=False, relative_scaling=0.27,
                      background_color='navy', colormap='rainbow', mask=mask).generate(title_data)

make_cloud(wordcloud)

