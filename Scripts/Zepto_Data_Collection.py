import pandas as pd

from google_play_scraper import Sort, reviews

results, _ = reviews(
    'com.zeptoconsumerapp',
    lang='en',
    country='in',
    sort=Sort.NEWEST,
    count=20000
)

print(len(results))

df = pd.DataFrame(results)

print(df.columns)
print(df.shape)

df['platform'] = 'Zepto'

df.to_csv('Zepto_reviews.csv', index=False)