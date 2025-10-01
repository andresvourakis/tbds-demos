# Makefile for Streamlit Dashboard

.PHONY: run docker stop

run:
	@echo "Starting Streamlit app..."
	@streamlit run app.py

docker:
	@echo "Building Docker image..."
	@docker build -t streamlit-dashboard .
	@echo "Stopping and removing existing container..."
	-@docker stop streamlit-dashboard-app && docker rm streamlit-dashboard-app
	@echo "Running Docker container..."
	@docker run --name streamlit-dashboard-app -d -p 8501:8501 streamlit-dashboard

stop:
	@echo "Stopping Docker container..."
	-@docker stop streamlit-dashboard-app && docker rm streamlit-dashboard-app