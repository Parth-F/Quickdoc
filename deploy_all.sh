#!/bin/bash

# Deploy backend first
echo "Deploying backend..."
cd "$(dirname "$0")"
bash Backend/deploy_backend.sh

# Deploy frontend
echo -e "\n\nDeploying frontend..."
bash Frontend/deploy_frontend.sh

echo -e "\n\nDeployment complete!"
echo "Backend is running on http://localhost:5000"
echo "Frontend is running on http://localhost:8501"
echo "You can access the application at http://$(hostname -I | awk '{print $1}')"
echo -e "\nCheck logs with:"
echo "  Backend: sudo journalctl -u quickdoc-backend -f"
echo "  Frontend: sudo journalctl -u streamlit -f" 