import pandas as pd

import warnings
warnings.filterwarnings('ignore')

class Reorganize:
	def __init__(self, data):
		self.pivot = data.pivot_table(
			index='CustomerID', 
			columns='Description', 
			values='Quantity', 
			fill_value=0
			)
