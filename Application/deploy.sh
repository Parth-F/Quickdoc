#!/bin/bash

# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Build frontend
cd client
npm install
npm run build
cd ..

# Configure Nginx
sudo tee /etc/nginx/sites-available/quickdoc << EOF
server {
    listen 80;
    server_name _;

    location / {
        root $(pwd)/client/build;
        try_files \$uri \$uri/ /index.html;
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
sudo nginx -t
sudo systemctl restart nginx

# Start backend server
gunicorn -c gunicorn_config.py app.app:app 
