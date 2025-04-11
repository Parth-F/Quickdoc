#!/bin/bash

# Install system dependencies if needed
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx

# Create a virtual environment for Streamlit if it doesn't exist
if [ ! -d "streamlit_venv" ]; then
    python3 -m venv streamlit_venv
fi

# Activate the virtual environment
source streamlit_venv/bin/activate

# Install Streamlit and other dependencies
pip install -r streamlit/requirements.txt

# Create Systemd service file for Streamlit
sudo tee /etc/systemd/system/streamlit.service << EOF
[Unit]
Description=Streamlit Web Application
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/streamlit_venv/bin"
Environment="BACKEND_URL=http://localhost:5000"
Environment="PYTHONPATH=$(pwd)"
ExecStart=$(pwd)/streamlit_venv/bin/streamlit run streamlit/main.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx configuration for Streamlit
sudo tee /etc/nginx/sites-available/quickdoc << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_cache_bypass \$http_upgrade;
    }

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

# Start Streamlit service
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl restart streamlit

# Display status
echo "Streamlit service status:"
sudo systemctl status streamlit --no-pager

echo "Nginx status:"
sudo systemctl status nginx --no-pager

echo ""
echo "Deployment complete! Your Streamlit app should now be running at http://$(hostname -I | awk '{print $1}')"
echo "You can check the logs with: sudo journalctl -u streamlit -f" 
