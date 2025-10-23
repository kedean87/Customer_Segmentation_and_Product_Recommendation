from load_dataset import *
from clustering import *
from reorganize import *
from embed_data import *
from product_query import *

import warnings
warnings.filterwarnings('ignore')

def main():
	d = Dataset()
	d.group_data()
	d.scale_data()
	
	c = Clustering(
		rfm=d.rfm, 
		rfm_scaled=d.rfm_scaled
		)
	c.cluster_results()
	c.determine_best_algorithm()
	
	r = Reorganize(
		data=d.data
		)
	
	ed = EmbedData(
		pivot=r.pivot
		)
	ed.create_model()
	ed.setup_data()
	ed.train()
	ed.get_embeddings()
	
	pq = ProductQuery(
		vectorizer=ed.vectorizer, 
		product_names=ed.product_names,
		product_name_embeddings=ed.product_name_embeddings,
		similarity_df=ed.similarity_df
		)
	
	results = pq.recommend("PINK CANDLES")
	for item, values in results.items():
		print(item, values)

if __name__ == "__main__":
	main()
