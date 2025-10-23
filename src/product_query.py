from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

import warnings
warnings.filterwarnings('ignore')

class ProductQuery:
	def __init__(self, vectorizer, product_names, product_name_embeddings, similarity_df):
		self.vectorizer = vectorizer
		self.product_names = product_names
		self.product_name_embeddings = product_name_embeddings
		self.similarity_df = similarity_df
	
	def recommend(self, query, top_n=10):
		# Embed query using the same TF-IDF vectorizer
		query_vec = self.vectorizer.transform([query])
		
		# Find closest product by cosine similarity in text space
		similarities = cosine_similarity(query_vec, self.product_name_embeddings).flatten()
		closest_idx = similarities.argmax()
		closest_product = self.product_names[closest_idx]
		
		# Use purchase-pattern similarity to get top co-purchased products
		if closest_product not in self.similarity_df.index:
			return f"'{closest_product}' not found in purchase data."
		similar_items = self.similarity_df[closest_product].sort_values(ascending=False)[1:top_n+1]
		
		return {
			"query": query,
			"closest_product": closest_product,
			"recommended_products": similar_items
		}
