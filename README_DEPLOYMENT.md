# QuickDoc AI Deployment Guide

This guide explains how to deploy QuickDoc AI with the Streamlit frontend on your Google Cloud Platform VM.

## Prerequisites

- A Google Cloud Platform VM running Ubuntu or Debian-based Linux
- Python 3.7 or higher
- Sudo access on the VM

## Quick Deployment

For a quick automatic deployment:

1. Connect to your GCP VM via SSH
2. Clone the repository (if you haven't already)
3. Navigate to the application directory
4. Run the deployment script:

```bash
./deploy_streamlit_backend.sh
```

The script will:
- Install all required dependencies
- Set up services for both backend and frontend
- Configure Nginx as a reverse proxy
- Start all services

After deployment, visit your VM's IP address in a browser to access the application.

## Manual Deployment Steps

If you prefer to deploy manually or need to troubleshoot, follow these steps:

### 1. Install Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx
```

### 2. Set Up Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r streamlit/requirements.txt
```

### 3. Run Services

**Backend:**
```bash
gunicorn -c gunicorn_config.py app.app:app
```

**Frontend:**
```bash
cd streamlit
streamlit run main.py --server.port=8501 --server.address=0.0.0.0
```

## Configuration

The application uses the following environment variables:

- `BACKEND_URL`: URL to the backend service (default: http://localhost:5000)
- `CORS_ORIGIN`: CORS settings for the backend (default: *)

## Troubleshooting

### Services Not Starting

Check the service logs:

```bash
sudo journalctl -u quickdoc-backend -f
sudo journalctl -u quickdoc-streamlit -f
```

### Cannot Access the Application

Check Nginx status and logs:

```bash
sudo systemctl status nginx
sudo tail -f /var/log/nginx/error.log
```

### Restarting Services

```bash
sudo systemctl restart quickdoc-backend
sudo systemctl restart quickdoc-streamlit
sudo systemctl restart nginx
```

## Monitoring

Monitor application logs:

```bash
# Backend logs
sudo journalctl -u quickdoc-backend -f

# Frontend logs
sudo journalctl -u quickdoc-streamlit -f
``` 
