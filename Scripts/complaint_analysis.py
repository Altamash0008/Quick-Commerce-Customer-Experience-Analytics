import pandas as pd

# Defining keywords 
support_keywords = ["customer service", "customer support", "support team", "response", "assistance", "care"]
delivery_keywords = ["delivery", "delivery partner", "delivery boy", "delivery person", "delivery time", "late", "delay","minutes", "arrived", "delivered"]
refund_keywords = [ "refund", "money", "payment", "return", "cash delivery", "refund process", "refund time", "refund policy"]
order_keywords = [ "cancel order", "placed order", "order delivered", "ordered", "order", "cancelled", "cancellation", "order issue", "order problem"]
product_keywords = [ "product", "products", "item", "items", "quality", "ice cream", "freshness", "packaging", "spoiled", "defective"]
app_keywords = ["bug", "crash", "error", "otp", "login", "software", "transaction fail", "payment failed", "technical", "app issue", "app problem", "app crash", "app bug", "app error", "app login"]
pricing_keywords = ["expensive", "high price", "delivery charges", "price", "costly", "rate high", "pricing", "overpriced"]

df = pd.read_csv("QuickCommerce_Clean.csv")

complaints_df = df[df["rating"] <= 2].copy()

print("Total complaint reviews:", complaints_df.shape[0])

# Categorize complaints based on keywords
def categorize_complaint(review):
    review = str(review).lower()
    if any(word in review for word in support_keywords):
        return "Customer Support"
    elif any(word in review for word in delivery_keywords):
        return "Delivery Issues"
    elif any(word in review for word in refund_keywords):
        return "Refund & Payment"
    elif any(word in review for word in order_keywords):
        return "Order Management"
    elif any(word in review for word in app_keywords):
        return "App Issues"
    elif any(word in review for word in product_keywords):
        return "Product Quality"
    elif any(word in review for word in pricing_keywords):
        return "Pricing Issues"
    else:
        return "Other"
        
complaints_df["complaint_category"] = complaints_df["review"].apply(
    categorize_complaint
)
    

# Create platform-wise comparison of complaint categories
comparison = pd.crosstab(
    complaints_df["platform"],
    complaints_df["complaint_category"]
)

print(comparison)

# Calculate percentages for better comparison
comparison_pct = pd.crosstab(
    complaints_df["platform"],
    complaints_df["complaint_category"],
    normalize="index"
) * 100

print(round(comparison_pct, 2))

# Analyze rating distribution by platform
rating_summary = pd.crosstab(
    df["platform"],
    df["rating"],
    normalize="index"
) * 100

print(round(rating_summary, 2))

# Average rating by platform
platform_rating = (
    df.groupby("platform")["rating"]
      .mean()
      .sort_values(ascending=False)
)

print(platform_rating)


# SENTIMENT ANALYSIS

def sentiment_from_rating(rating):

    if rating >= 4:
        return "Positive"

    elif rating == 3:
        return "Neutral"

    else:
        return "Negative"

df["sentiment"] = df["rating"].apply(
    sentiment_from_rating
)

sentiment_summary = pd.crosstab(
    df["platform"],
    df["sentiment"],
    normalize="index"
) * 100

print("\nSentiment Summary (%)")
print(round(sentiment_summary, 2))

# Save all results to CSV files
complaints_df.to_csv(
    "QuickCommerce_Complaints.csv",
    index=False
)

comparison.to_csv(
    "Complaint_Counts.csv"
)

comparison_pct.to_csv(
    "Complaint_Percentages.csv"
)

platform_rating.to_csv(
    "Average_Rating.csv"
)

rating_summary.to_csv(
    "Rating_Distribution.csv"
)

sentiment_summary.to_csv(
    "Sentiment_Summary.csv"
)

print("All files saved successfully!")