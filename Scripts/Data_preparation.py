import pandas as pd 

blinkit = pd.read_csv("Blinkit_reviews.csv")
instamart = pd.read_csv("Instamart_reviews.csv")
zepto = pd.read_csv("Zepto_reviews.csv")

blinkit["platform"] = "Blinkit"
instamart["platform"] = "Instamart"
zepto["platform"] = "Zepto"

master = pd.concat(
    [blinkit, instamart, zepto],
    ignore_index=True
)

print(master.shape)

master.to_csv(
    "QuickCommerce_Raw.csv",
    index=False
)

# Cleaning the data
master = master[
    [
        "platform",
        "content",
        "score",
        "thumbsUpCount",
        "at"
    ]
]
master.columns = [
    "platform",
    "review",
    "rating",
    "thumbs_up",
    "review_date"
]
master = master.dropna(
    subset=["review"]
)
master = master.drop_duplicates(
    subset=["review"]
)

master["word_count"] = (
    master["review"]
    .str.split()
    .str.len()
)

# Remove reviews with fewer than 3 words
master = master[
    master["word_count"] >= 3
]

master.to_csv(
    "QuickCommerce_Clean.csv",
    index=False
)

print("Clean dataset saved successfully")