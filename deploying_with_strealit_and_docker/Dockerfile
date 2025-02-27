# Use a lightweight Python image  
FROM python:3.9-slim  

# Set the working directory inside the container  
WORKDIR /app  

# Copy only the requirements file first (helps with caching layers)
COPY requirements.txt .  

# Install dependencies  
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the rest of the application files  
COPY . .  

# Streamlit requires environment variables for seamless deployment  
ENV STREAMLIT_SERVER_HEADLESS=true  

# Expose the port Streamlit runs on  
EXPOSE 8501  

# Run the Streamlit app  
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
