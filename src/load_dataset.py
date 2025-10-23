import pandas as pd
from sklearn.preprocessing import StandardScaler

import warnings
warnings.filterwarnings('ignore')

class Dataset:
	def __init__(self):
		self.url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
		self.data = pd.read_excel(self.url)
		self.data = self.data.dropna(subset=['CustomerID'])
		self.data = self.data[self.data['Quantity'] > 0]
		print(f"Loaded {len(self.data):,} transactions.")
		
		self.rfm = None
		self.rfm_scaled = None
		self.scaler = None
	
	def group_data(self):
		self.rfm = self.data.groupby('CustomerID').agg({
			'InvoiceDate': lambda x: (self.data['InvoiceDate'].max() - x.max()).days,
			'InvoiceNo': 'count',
			'Quantity': 'sum',
			'UnitPrice': 'mean'
		}).reset_index()
		self.rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Quantity', 'AvgPrice']
	
	def scale_data(self):
		self.scaler = StandardScaler()
		self.rfm_scaled = self.scaler.fit_transform(self.rfm[['Recency', 'Frequency', 'Quantity', 'AvgPrice']])
