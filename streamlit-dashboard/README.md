# Sample Streamlit Dashboard

This is a simple Streamlit dashboard that demonstrates how to create a containerized Streamlit application.

## Prerequisites

- Python 3.9+
- Docker

## Setup

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Application

You can run the application either locally or using Docker.

### Locally

To run the application directly on your machine, use the following command:

```bash
make run
```

This will start the Streamlit server on `http://localhost:8501`.

### With Docker

To build and run the application inside a Docker container:

```bash
make docker
```

This will build the Docker image and start the container. The application will be accessible at `http://localhost:8501`.

**Note on Port Conflicts:** The `make docker` command will fail if another process is already using port 8501 (e.g., if you are already running the app with `make run`). The `Makefile` is configured to stop any previous *Docker container* using the same name, but it cannot stop a local process.

To stop the container started by `make docker`, run:

```bash
make stop
```
