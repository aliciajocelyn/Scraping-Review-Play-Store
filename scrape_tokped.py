import serpapi
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('SERPAPI_KEY')
client = serpapi.Client(api_key=api_key)

desired_reviews_per_rating = 500 # Each rating will have 500 reviews
ratings_collected = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0} # Tracking how many reviews have been collected
all_reviews = {1: [], 2: [], 3: [], 4: [], 5: []} 

def has_collected_enough_reviews():
    return all(count >= desired_reviews_per_rating for count in ratings_collected.values())

results = client.search(
    engine='google_play_product',
    product_id='com.tokopedia.tkpd',
    store='apps',
    hl='id',
    gl='id',
    all_reviews='true',
    num=199
)

while 'serpapi_pagination' in results and not has_collected_enough_reviews():
    for review in results.get("reviews", []):
        rating = review.get("rating")
        if rating and ratings_collected[rating] < desired_reviews_per_rating:
            all_reviews[rating].append(review)
            ratings_collected[rating] += 1
        
        if has_collected_enough_reviews(): # If collected enough ratings
            break

    if not has_collected_enough_reviews():
        results = client.search(
            engine='google_play_product',
            product_id='com.tokopedia.tkpd',
            store='apps',
            hl='id',
            gl='id',
            all_reviews='true',
            num=199,
            next_page_token=results['serpapi_pagination']['next_page_token']
        )

collected_reviews = [] # Combine all reviews
for rating, reviews in all_reviews.items():
    collected_reviews.extend(reviews)

# Save to pandas dataframe
df_reviews = pd.DataFrame(collected_reviews)
df_reviews.to_csv('tokopedia_balanced_reviews.csv', index=False)
print(f"Collected a total of {len(collected_reviews)} reviews (500 per rating) and saved them to 'shopee_balanced_reviews.csv'.")