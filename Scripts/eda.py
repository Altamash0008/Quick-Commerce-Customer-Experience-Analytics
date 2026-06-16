import pandas as pd
import re
from collections import Counter

df = pd.read_csv("QuickCommerce_Clean.csv")
print(df.shape)
print(df.head())

negative_reviews = df[df["rating"] <=2]
print("Negative_reviews:", len(negative_reviews))

# Combining all negative reviews  
text = " ".join(
    negative_reviews["review"].astype(str)
)

# Extract words using regular expressions
words = re.findall(
    r"\b[a-zA-Z]+\b",
    text.lower()
)
# Remove common stop words
stop_words = {
    "the","is","a","an","and","or","of","to","for","in","on","at",
    "it","this","that","was","are","be","have","has","had","with",
    "i","my","me","we","our","you","your","they","them","their",
    "from","when","will","there","if","so","all","one","can",
    "but","very","after","even","also","any","as","not","no",
    "t","s","don"
}

filtered_words = [
    word
    for word in words
    if word not in stop_words
]

# top 50 words 
word_freq = Counter(filtered_words)

print("\nTop 50 Most Common Words:\n")

for word, count in word_freq.most_common(50):
    print(f"{word}: {count}")

# Save words to a CSV file
top_words = pd.DataFrame(
    word_freq.most_common(100),
    columns=["word", "count"]
)

top_words.to_csv(
    "Top_Negative_Words.csv",
    index=False
)

# Analyze common bigrams in negative reviews
from sklearn.feature_extraction.text import CountVectorizer

negative_reviews = df[df["rating"] <= 2]

vectorizer = CountVectorizer(
    stop_words='english',
    ngram_range=(2,2),
    max_features=50
)

X = vectorizer.fit_transform(
    negative_reviews["review"].astype(str)
)

bigram_counts = X.sum(axis=0)

bigrams = [
    (word, bigram_counts[0, idx])
    for word, idx in vectorizer.vocabulary_.items()
]

bigrams = sorted(
    bigrams,
    key=lambda x: x[1],
    reverse=True
)

for phrase, count in bigrams[:30]:
    print(f"{phrase}: {count}")


# Average rating by platform
platform_rating = (
    df.groupby("platform")["rating"]
      .mean()
      .sort_values(ascending=False)
)

print(platform_rating)

# Percentage of negative reviews by platform
negative_pct = (
    df[df["rating"] <= 2]
    .groupby("platform")
    .size()
    / df.groupby("platform").size()
) * 100

print(round(negative_pct, 2))

# Save bigrams to CSV
top_bigrams = pd.DataFrame(
    bigrams[:50],
    columns=["bigram", "count"]
)

top_bigrams.to_csv(
    "Top_Negative_Bigrams.csv",
    index=False
)

# Save average ratings to CSV
platform_rating.to_csv(
    "Average_Rating.csv"
)
# Save negative review percentages to CSV
negative_pct.to_csv(
    "Negative_Review_Percentage.csv"
)


# Additional EDA: Reviews per platform
reviews_per_platform = (
    df["platform"]
    .value_counts()
)

print(reviews_per_platform)

reviews_per_platform.to_csv(
    "Reviews_Per_Platform.csv"
)