import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA

import warnings
warnings.filterwarnings('ignore')

class Clustering:
	def __init__(self, rfm, rfm_scaled, n_clusters=4, n_components=4, random_state=42, n_init=10, eps=0.8, min_samples=5):
		self.rfm = rfm
		self.rfm_scaled = rfm_scaled
		
		self.algorithms = {
			"KMeans": KMeans(n_clusters=n_clusters, random_state=random_state, n_init=n_init),
			"DBSCAN": DBSCAN(eps=eps, min_samples=min_samples),
			"Agglomerative": AgglomerativeClustering(n_clusters=n_clusters),
			"GMM": GaussianMixture(n_components=n_components, random_state=random_state)
		}
	
		self.results = None
		self.best_algo = None

	def cluster_results(self):
		print(f"Clustering Results")
		self.results = []
		for name, algo in self.algorithms.items():
			try:
				labels = algo.fit_predict(self.rfm_scaled)
				if len(set(labels)) > 1:
					score = silhouette_score(self.rfm_scaled, labels)
				else:
					score = np.nan
				self.results.append((name, len(set(labels)), score))
				print(f"{name}: Clusters={len(set(labels))}, Silhouette={score:.3f}")
			except Exception as e:
				self.results.append((name, 0, np.nan))
				print(f"{name} failed: {e}")
		
		print("Results: ", self.results)
	
	def determine_best_algorithm(self):
		valid_results = [(n, c, s) for n, c, s in self.results if not np.isnan(s)]
		best_algo_name, _, best_score = max(valid_results, key=lambda x: x[2])
		print(f"\nBest clustering algorithm: {best_algo_name} (Silhouette={best_score:.3f})")

		self.best_algo = self.algorithms[best_algo_name]
		self.rfm['Segment'] = self.best_algo.fit_predict(self.rfm_scaled)
		print("\nCustomer segment distribution:")
		print(self.rfm['Segment'].value_counts())
