from flask import Flask, request, jsonify
from product_query import *
from scipy import sparse
import json
import pickle
import joblib

import warnings
warnings.filterwarnings('ignore')

tfidf_vectorizer = joblib.load("tfidf_vectorizer.pkl")

with open('product_names.pkl', 'rb') as f:
    product_names = pickle.load(f)

product_name_embeddings = sparse.load_npz('product_name_embeddings.npz')

similarity_df = pd.read_csv('similarity.csv', index_col=0)

pq = ProductQuery(
    vectorizer=tfidf_vectorizer, 
    product_names=product_names,
    product_name_embeddings=product_name_embeddings,
    similarity_df=similarity_df
    )

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    query = data.get("query")
    
    results = pq.recommend(query)
    print(results)
    results['recommended_products'] = results['recommended_products'].to_dict()
    for item, values in results.items():
        print('\nKey: ', item)
        print('\t', values)
    
    response = {"answer": results}
    final_json = json.dumps(response)
    
    return jsonify(final_json)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)
