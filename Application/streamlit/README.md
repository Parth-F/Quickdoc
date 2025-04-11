# QuickDoc AI Streamlit Frontend

This is the Streamlit-based frontend for the QuickDoc AI medical chatbot.

## Deployment to Google Cloud Run

### Prerequisites
- Google Cloud SDK (gcloud) installed and configured
- Docker installed on your local machine
- Access to a Google Cloud Project with Cloud Run API enabled

### Steps to Deploy

1. **Build and push the Docker image to Google Container Registry**

```bash
# Navigate to the streamlit directory
cd Application/streamlit

# Build the Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/quickdoc-streamlit .

# Push the image to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/quickdoc-streamlit
```

2. **Deploy to Cloud Run**

```bash
gcloud run deploy quickdoc-streamlit \
  --image gcr.io/YOUR_PROJECT_ID/quickdoc-streamlit \
  --platform managed \
  --region YOUR_PREFERRED_REGION \
  --allow-unauthenticated \
  --set-env-vars "BACKEND_URL=https://your-backend-service-url.a.run.app"
```

Replace:
- `YOUR_PROJECT_ID` with your Google Cloud Project ID
- `YOUR_PREFERRED_REGION` with your preferred Google Cloud region (e.g., us-central1)
- Set the `BACKEND_URL` to point to your backend service's URL

3. **Access your deployed application**

After deployment, Cloud Run will provide a URL to access your application.

### Local Testing

To test locally before deploying:

```bash
docker build -t quickdoc-streamlit .
docker run -p 8080:8080 -e BACKEND_URL=http://localhost:5000 quickdoc-streamlit
```

Then access the application at http://localhost:8080 
