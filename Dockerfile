FROM python:3.11-slim

WORKDIR /app

# This installs the required system dependencies, including ffmpeg
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
# This tells Docker to copy your actual app instead of the template folder
COPY app.py ./

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# This forces the server to run your code
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]