# Astor AI

Huggingface Model: [Medical LLAMA Model](https://huggingface.co/srikar-v05/llama3-Medical-Chat)

## Abstract
Large Language Models (LLMs) offer significant potential in the healthcare domain, particularly in scenarios where medical professionals may not be readily available. These models can serve as virtual medical assistants, addressing patient queries related to non-critical conditions. A pre-trained LLM, such as Mistral-7B, can be effectively utilized to develop a Medical Chat Doctor, capable of responding to patient inquiries with concise and relevant information. To enhance the accuracy and quality of the chatbot's responses, fine-tuning the model with domain-specific datasets, such as the "ChatDoctor-HealthCareMagic-100K" from Hugging Face, is essential. This approach ensures that the chatbot can accurately interpret symptoms described by patients and provide appropriate responses, thereby improving patient care and access to medical advice.

## Introduction
Welcome to the AstorAI website, your gateway to accurate and reliable medical information. Our user-friendly interface, combined with Retrieval-Augmented Generation technology, makes it easy for you to navigate and find the answers you need. Engage with AstorAI through our interactive chatbot for real-time, detailed responses to your medical questions. We prioritize your privacy and security, ensuring all interactions and personal information are kept confidential. Explore and discover how AstorAI can assist you on your health journey.
![image](https://github.com/user-attachments/assets/61c9109a-1112-4442-9f4f-37c74277d34d)
## Features of the Chatbot

### Medical Information
AstorAI provides reliable answers to a wide range of medical questions, leveraging the power of the advanced LLama 3 model with a [custom dataset](https://huggingface.co/datasets/lavita/ChatDoctor-HealthCareMagic-100k).

### Real-Time Responses
Get immediate, detailed responses to your queries with AstorAI's interactive chatbot, available 24/7 to assist you whenever you need it.

### User-Friendly Interface
Our chatbot is designed with simplicity in mind, offering a clean and intuitive interface that makes it easy to ask questions and receive answers.

### Privacy and Security
AstorAI prioritizes your privacy, ensuring that your information remains confidential with no account required and no chat history stored.

### Wide Range of Topics
From symptoms and treatments to medications and general health advice, AstorAI covers a broad spectrum of medical topics to help you find the information you need.

## Deployment Instructions

### Backend (Flask API)

1. Install required dependencies:
   ```
   cd Application/app
   pip install flask flask-cors langchain langchain_community chromadb
   ```

2. Configure environment variables:
   - `PORT`: API server port (default: 5000)
   - `CORS_ORIGIN`: Allowed origins for CORS (default: '*')

3. Ensure Ollama is installed and models are available:
   - You need both `llama3` and `medical-llama` models in Ollama

4. Run the server:
   ```
   python app.py
   ```

### Frontend (React)

1. Install dependencies:
   ```
   cd Application/client
   npm install
   ```

2. Configure environment variables:
   - Create a `.env` file with `REACT_APP_API_URL` pointing to your API server

3. Build for production:
   ```
   npm run build
   ```

4. Serve the built files using a static file server like Nginx or serve them directly from your backend

### Docker Deployment (Optional)

For easier deployment, you can containerize both the frontend and backend:

1. Backend Dockerfile example:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY Application/app .
   RUN pip install flask flask-cors langchain langchain_community chromadb
   EXPOSE $PORT
   CMD ["python", "app.py"]
   ```

2. Frontend Dockerfile example:
   ```dockerfile
   FROM node:16 as build
   WORKDIR /app
   COPY Application/client .
   RUN npm install && npm run build
   
   FROM nginx:alpine
   COPY --from=build /app/build /usr/share/nginx/html
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

## Recent Updates

The application has been simplified to focus solely on the chatbot functionality:

- Removed all user authentication and login requirements
- The chatbot interface now loads directly when visiting the site
- Each page refresh starts a new chat session
- Added environment variable configuration for better deployment flexibility
"# Quickdoc" 
