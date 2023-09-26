# Spaceclouder
Spaceclouder is word cloud maker for space and popular science related topics. This was a learning project made to provide custom visualisations for pitch decks in a previous public relations role. 


## Use
Spaceclouder depends on wordcloud, pillow, scrapy, and some standard libraries. Make sure that both spacespiders.py and wordcloudmaker.py are in the same directory as your scrapy.cfg file. 
When ready, run spacespiders.py and input a search query. The script will then scrape various space and science-related news sites for article headings, save them, and use them to create a wordcloud with wordcloudmaker.py. 
A standard mask is included but you can use any image as long as it's named 'earth.jpg' and in the same directory as the .py files.
