#!/bin/bash

# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev build-essential cmake

# Check if llama.cpp is built
if [ ! -f "../llama.cpp/bin/llama-cli" ]; then
    echo "Building llama.cpp..."
    cd ../llama.cpp
    
    # Ensure llama.cpp is properly built with all needed components
    make clean
    LLAMA_CUBLAS=1 make -j
    
    # If the build fails, try without CUDA
    if [ ! -f "./bin/llama-cli" ]; then
        echo "Build with CUDA failed, trying without CUDA..."
        make clean
        make -j
    fi
    
    cd ../Backend
    echo "llama.cpp built successfully"
fi

# Install backend dependencies
cd "$(dirname "$0")"
sudo pip3 install -r requirements.txt

# Verify model exists
if [ ! -f "../Models/model.gguf" ]; then
    echo "Error: model.gguf not found in Models directory"
    echo "Please ensure the model file is correctly placed before continuing"
    exit 1
fi

# Get absolute path to QuickDoc root directory
QUICKDOC_ROOT=$(cd .. && pwd)

# Create systemd service file for Flask backend
sudo tee /etc/systemd/system/quickdoc-backend.service << EOF
[Unit]
Description=QuickDoc Backend Flask Application
After=network.target

[Service]
User=$USER
WorkingDirectory=${QUICKDOC_ROOT}
Environment="PYTHONPATH=${QUICKDOC_ROOT}"
ExecStart=/usr/bin/python3 ${QUICKDOC_ROOT}/Backend/app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Make the service file executable
sudo chmod 755 /etc/systemd/system/quickdoc-backend.service

# Upgrade SQLite3 for Chroma
echo "Checking SQLite3 version..."
SQLITE_VERSION=$(sqlite3 --version | awk '{print $1}')
echo "Current SQLite3 version: $SQLITE_VERSION"

if [[ "$SQLITE_VERSION" < "3.35.0" ]]; then
    echo "Upgrading SQLite3 for Chroma compatibility..."
    sudo apt-get install -y build-essential wget
    cd /tmp
    wget https://www.sqlite.org/2023/sqlite-autoconf-3420000.tar.gz
    tar -xvf sqlite-autoconf-3420000.tar.gz
    cd sqlite-autoconf-3420000
    ./configure
    make
    sudo make install
    sudo ldconfig
    echo "SQLite3 upgraded. New version:"
    sqlite3 --version
fi

cd ${QUICKDOC_ROOT}/Backend

# Start and enable the service
sudo systemctl daemon-reload
sudo systemctl enable quickdoc-backend
sudo systemctl start quickdoc-backend

# Display service status
echo "Backend service status:"
sudo systemctl status quickdoc-backend --no-pager

echo ""
echo "Deployment complete! Backend should now be running on port 5000"
echo "You can check the logs with: sudo journalctl -u quickdoc-backend -f" 