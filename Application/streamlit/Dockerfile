FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PORT=8080
# You'll need to set BACKEND_URL during deployment

# Expose the port
EXPOSE 8080

# Command to run the application
CMD streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 
