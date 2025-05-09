import pandas as pd
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from collections import Counter

# Load CSV file
df = pd.read_csv("export/documents.csv")

# Split and flatten all keywords into a single list
all_keywords = []
for keyword_list in df['keywords'].dropna():
    all_keywords.extend([kw.strip() for kw in keyword_list.split(',')])

# Count keyword frequencies
keyword_counts = Counter(all_keywords)

# Convert to DataFrame for plotting
freq_df = pd.DataFrame(keyword_counts.items(), columns=['Keyword', 'Frequency'])
freq_df = freq_df.sort_values(by='Frequency', ascending=False)

###################################
# Frequency Analysis
###################################
# Plot the keyword frequencies
plt.figure(figsize=(12, 6))
plt.bar(freq_df['Keyword'], freq_df['Frequency'], color='skyblue')
plt.title('Keyword Frequency Visualization')
plt.xlabel('Keyword')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

###################################
# Word Cloud Visualization
###################################
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(all_keywords))

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Keyword Word Cloud')
plt.tight_layout()
plt.show()
