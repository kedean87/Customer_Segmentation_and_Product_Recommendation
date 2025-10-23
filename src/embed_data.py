from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
import tensorflow as tf
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

class EmbedData:
	def __init__(self, pivot, encoding_dim=64, activation='relu', optimizer='adam', loss='mse'):
		self.product_matrix = pivot.T  # now each row = product, columns = customers
		self.input_dim_products = self.product_matrix.shape[1]
		
		self.encoding_dim = encoding_dim
		self.activation = activation
		self.optimizer = optimizer
		self.loss = loss
		
		self.product_names = self.product_matrix.index.tolist()
		self.vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1,2))
		self.product_name_embeddings = self.vectorizer.fit_transform(self.product_names)
		
		self.product_name_similarity_df = None
		
		self.autencoder = None
		self.encoder = None
		
		self.X_train = None
		self.X_test = None
		
		self.product_embeddings = None
		self.product_similarity = None
		self.similarity_df = None
		
	def create_model(self):
		input_layer_p = Input(shape=(self.input_dim_products,))
		encoded_p = Dense(256, activation=self.activation)(input_layer_p)
		encoded_p = Dense(128, activation=self.activation)(encoded_p)
		bottleneck_p = Dense(self.encoding_dim, activation=self.activation)(encoded_p)
		decoded_p = Dense(128, activation=self.activation)(bottleneck_p)
		decoded_p = Dense(256, activation=self.activation)(decoded_p)
		output_layer_p = Dense(self.input_dim_products, activation='sigmoid')(decoded_p)

		self.autoencoder = Model(input_layer_p, output_layer_p)
		self.encoder = Model(input_layer_p, bottleneck_p)
		self.autoencoder.compile(optimizer=self.optimizer, loss=self.loss)
	
	def setup_data(self):
		self.X_train, self.X_test = train_test_split(
			self.product_matrix.values, 
			test_size=0.2, 
			random_state=42
			)

	def train(self):
		self.autoencoder.fit(
			self.X_train, 
			self.X_train, 
			epochs=10, 
			batch_size=64, 
			validation_data=(self.X_test, self.X_test), 
			verbose=0
			)
	
	def get_embeddings(self):
		self.product_embeddings = self.encoder.predict(self.product_matrix.values)
		self.product_similarity = cosine_similarity(self.product_embeddings)
		self.similarity_df = pd.DataFrame(
			self.product_similarity, 
			index=self.product_matrix.index, 
			columns=self.product_matrix.index
			)
		
		product_name_similarity = cosine_similarity(self.product_name_embeddings)
		self.product_name_similarity_df = pd.DataFrame(
			product_name_similarity, 
			index=self.product_names, 
			columns=self.product_names
		)

