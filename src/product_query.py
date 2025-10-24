from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

import warnings
warnings.filterwarnings('ignore')

class ProductQuery:
    def __init__(self, pivot, rfm, vectorizer, product_names, product_name_embeddings, similarity_df):
        self.pivot = pivot
        self.rfm = rfm
        self.vectorizer = vectorizer
        self.product_names = product_names
        self.product_name_embeddings = product_name_embeddings
        self.similarity_df = similarity_df
    
    def recommend(self, query, customer_id=None, top_n=10):
        # Semantic similarity (TF-IDF)
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.product_name_embeddings).flatten()
        closest_idx = similarities.argmax()
        closest_product = self.product_names[closest_idx]

        # Behavioral similarity (co-purchase)
        if closest_product not in self.similarity_df.index:
            return f"'{closest_product}' not found in purchase data."

        similar_items = self.similarity_df[closest_product].sort_values(ascending=False)[1:top_n+1]

        # Optional customer-based refinement
        if customer_id and hasattr(self, 'rfm'):
            customer_segment = self.rfm.loc[self.rfm['CustomerID'] == customer_id, 'Segment']
            print('\n', customer_segment, '\n')
            if not customer_segment.empty:
                segment = customer_segment.values[0]
                
                # adjust ranking for products popular in this segment
                segment_customers = self.rfm[self.rfm['Segment'] == segment]['CustomerID']
                segment_purchases = self.pivot.loc[segment_customers].sum()
                similar_items = segment_purchases[similar_items.index].sort_values(ascending=False)

        return {
            "query": query,
            "closest_product": closest_product,
            "recommended_products": similar_items
        }

