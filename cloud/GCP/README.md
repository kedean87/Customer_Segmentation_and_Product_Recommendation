# 🧠 E-commerce Customer Segmentation and Product Recommendation (GCP Cloud Run Deployment)

This project demonstrates how to deploy a **Flask-based Product Recommendation API** deployed to **Google Cloud Platform (GCP)** using **Cloud Run** and **Container Registry**.

The vectorizer for product names and product embedding similarity information were pre-trained locally using scikit-learn and tensorflow, serialized with `joblib`, and then containerized into a production-ready API.

---

## 🚀 Overview

- **Clustering**: DBSCAN
- **Vectorizer**: TF-IDF
- **Autoendocer Embeddings**
- **Framework**: Flask  
- **Deployment Platform**: Google Cloud Run  
- **Container Registry**: Google Container Registry (GCR)  
- **Architecture**: `linux/amd64` (to match GCP build environment)  
- **Language**: Python 3.10  

---

## 🛠️ Step-by-Step Setup

### 1. Install and Initialize Google Cloud SDK

```bash
# Initialize gcloud
gcloud init
```

Follow the on-screen prompts to:
	- Log in with your Google account
	- Choose or create a project (we used fake-news-gcp)
	- Set a default region (e.g., us-central1)

---

### 2. Enable Required GCP APIs
```bash
gcloud services enable run.googleapis.com containerregistry.googleapis.com
```

Problem Encountered:
```bash
ERROR: Billing account for project '############' is not found.
```

Solution:
- GCP requires billing to be linked even for free-tier usage.
- Go to **Billing → Link a billing account** in the Google Cloud Console, then rerun the command.

---

### 3. Prepare Your Flask App: serve.py

---

### 4. Create the Dockerfile

---

### 5. Build and Push the Docker Image
```bash
# Build the Docker image with GCP-compatible architecture
export DOCKER_BUILDKIT=1
docker buildx build --provenance=false --output type=docker --platform linux/amd64 -t gcr.io/nth-transformer-476104-v5/ecommerce-recommendation .

# Submit the build to GCP Container Registry
gcloud builds submit --tag gcr.io/nth-transformer-476104-v5/ecommerce-recommendation
```

Problem Encountered:
```bash
PERMISSION_DENIED: The caller does not have permission.
```

Solution:
Ensure your terminal is authenticated as the correct Google account:
```bash
gcloud auth login
gcloud config set project fake-news-gcp
gcloud projects add-iam-policy-binding nth-transformer-476104-v5 \                         
  --member="user:<your-email-here>@gmail.com" \
  --role="roles/editor"
```

---

### 7. Deploy to Cloud Run
```bash
gcloud run deploy ecommerce-recommendation \
  --image gcr.io/nth-transformer-476104-v5/ecommerce-recommendation:latest \
  --platform managed \
  --region us-central1 \
  --memory 1Gi \
  --allow-unauthenticated
```

---

### 8. Test the Live API
After successful deployment, GCP will output a public URL, for example:
```bash
https://fake-news-api-abcdef123-uc.a.run.app
```

Run a test from your terminal:
```bash
curl -X POST https://fake-news-api-abcdef123-uc.a.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{"query": "CANDLES"}'
```

![Fake News Prediction](images/EcomRecDetectionGCPPrediction.png)
> Showing that the container can run the prediction from the GCP web console and local terminal.

✅ Example Output:
```bash
"{\"answer\": {\"query\": \"CANDLES\", \"closest_product\": \"S/4 CACTI CANDLES\", \"recommended_products\": {\"PINK POT PLANT CANDLE\": 0.9523045, \"OWL DOORSTOP\": 0.9431338, \"OVERNIGHT BAG VINTAGE ROSE PAISLEY\": 0.9409219, \"BLUE POT PLANT CANDLE \": 0.9404967, \"RED RETROSPOT TEA CUP AND SAUCER \": 0.9380021, \"FRYING PAN PINK POLKADOT\": 0.9345215, \"MILK PAN RED RETROSPOT\": 0.93127054, \"FRYING PAN RED RETROSPOT\": 0.9273778, \"VINTAGE UNION JACK APRON\": 0.92689294, \"LOCAL CAFE MUG\": 0.92587674}}}"
```

---

## 🧰 Common Issues & Fixes

| Issue | Cause | Solution |
|-------|--------|-----------|
| `PERMISSION_DENIED` during `gcloud builds submit` | Incorrect account | Run `gcloud auth login` and set project |

---

## Summary

This deployment shows how to:
- Cluster Customer Information using scikit-learn algorithms
  - Pick best Clustering algorithm using Silhouette Metric
- Create Embeddings for Product Information ( Values / Names)
- TF-IDF Vectorization for Product Name Similarity
- Serialize and serve it with Flask
- Containerize it for portability
- Deploy it to Google Cloud Run
- Test it live via public API

---

## Notes

- Cloud Run scales automatically based on incoming requests.
- You can add logging via print() or logging to see messages in Cloud Run Logs.
- This approach also works on AWS (Elastic Beanstalk, Lambda) and Azure (Web Apps).

