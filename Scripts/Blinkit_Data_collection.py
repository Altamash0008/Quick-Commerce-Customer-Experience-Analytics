import pandas as pd

from google_play_scraper import Sort, reviews
results, _ = reviews('com.grofers.customerapp',
                     lang='en',
                    country='in',
                    sort= Sort.NEWEST,
                    count=20000)    

print(len(results))

df = pd.DataFrame(results)
print(df.columns)
print(df.shape)

df.to_csv('Blinkit_reviews.csv', index=False)
