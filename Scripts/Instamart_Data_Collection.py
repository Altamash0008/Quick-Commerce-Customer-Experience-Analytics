import pandas as pd

from google_play_scraper import Sort, reviews

results, _ = reviews(
    'in.swiggy.android.instamart',
    lang='en',
    country='in',
    sort=Sort.NEWEST,
    count=20000
)

print(len(results))

df = pd.DataFrame(results)

print(df.columns)
print(df.shape)

df['platform'] = 'Instamart'

df.to_csv('Instamart_reviews.csv', index=False)