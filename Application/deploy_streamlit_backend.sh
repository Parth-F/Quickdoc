#!/bin/bash

# Exit on error
set -e

echo "===== Starting deployment of QuickDoc AI with Streamlit frontend ====="

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies for both backend and Streamlit
echo "Installing Python dependencies..."
pip install -r requirements.txt
pip install -r streamlit/requirements.txt

# Set up systemd service for Flask Backend
echo "Setting up Flask backend service..."
sudo tee /etc/systemd/system/quickdoc-backend.service << EOF
[Unit]
Description=QuickDoc AI Backend
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
Environment="PYTHONPATH=$(pwd)"
ExecStart=$(pwd)/venv/bin/gunicorn -c gunicorn_config.py app.app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Set up systemd service for Streamlit Frontend
echo "Setting up Streamlit frontend service..."
sudo tee /etc/systemd/system/quickdoc-streamlit.service << EOF
[Unit]
Description=QuickDoc AI Streamlit Frontend
After=network.target quickdoc-backend.service

[Service]
User=$(whoami)
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
Environment="BACKEND_URL=http://localhost:5000"
Environment="PYTHONPATH=$(pwd)"
ExecStart=$(pwd)/venv/bin/streamlit run streamlit/main.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx configuration
echo "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/quickdoc << EOF
server {
    listen 80;
    server_name _;

    # Serve Streamlit frontend
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_cache_bypass \$http_upgrade;
    }

    # Route API requests to Flask backend
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# Enable Nginx configuration
sudo ln -sf /etc/nginx/sites-available/quickdoc /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

# Enable and start services
echo "Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable quickdoc-backend
sudo systemctl enable quickdoc-streamlit
sudo systemctl restart quickdoc-backend
sudo systemctl restart quickdoc-streamlit

# Display status
echo -e "\n===== Deployment Complete! ====="
echo "Backend service status:"
sudo systemctl status quickdoc-backend --no-pager

echo -e "\nFrontend service status:"
sudo systemctl status quickdoc-streamlit --no-pager

echo -e "\nNginx status:"
sudo systemctl status nginx --no-pager

echo -e "\n===== QuickDoc AI is now running! ====="
echo "Your application should be available at: http://$(hostname -I | awk '{print $1}')"
echo ""
echo "Monitor backend logs: sudo journalctl -u quickdoc-backend -f"
echo "Monitor frontend logs: sudo journalctl -u quickdoc-streamlit -f"
echo "Monitor nginx logs: sudo tail -f /var/log/nginx/error.log" 
