# QuickDoc AI Streamlit Frontend

This is the Streamlit frontend for the QuickDoc AI medical chatbot application.

## Overview

The Streamlit frontend provides a user-friendly interface for interacting with the QuickDoc AI backend. It allows users to:

- Ask medical questions
- Choose between different LLM models (Flagship or Augmented)
- View chat history
- Start new conversations

## Deployment on Google Cloud Platform VM

Follow these steps to deploy the Streamlit frontend on your GCP VM:

1. Make sure you're in the project root directory:
   ```
   cd /path/to/your/project
   ```

2. Run the deployment script:
   ```
   ./Frontend/deploy_frontend.sh
   ```

   This script will:
   - Install necessary dependencies
   - Create a virtual environment for Streamlit
   - Set up a systemd service for running Streamlit
   - Configure Nginx as a reverse proxy
   - Start the Streamlit application

3. Access the application through your VM's IP address on port 80:
   ```
   http://<your-vm-ip>/
   ```

## Manual Setup (If Needed)

If you prefer to set up the application manually:

1. Create a virtual environment:
   ```
   python3 -m venv streamlit_venv
   source streamlit_venv/bin/activate
   ```

2. Install dependencies:
   ```
   pip install -r Frontend/requirements.txt
   ```

3. Run the Streamlit application:
   ```
   export BACKEND_URL=http://localhost:5000
   streamlit run Frontend/main.py --server.port=8501 --server.address=0.0.0.0
   ```

## Environment Variables

- `BACKEND_URL`: URL of the backend API (default: http://localhost:5000)

## Monitoring and Troubleshooting

- Check Streamlit service logs:
  ```
  sudo journalctl -u streamlit -f
  ```

- Restart the Streamlit service:
  ```
  sudo systemctl restart streamlit
  ```

- Check Nginx logs:
  ```
  sudo tail -f /var/log/nginx/error.log
  ```
