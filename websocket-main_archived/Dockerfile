FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Install git and ssh client
RUN apt-get update && \
    apt-get install -y git openssh-client && \
    rm -rf /var/lib/apt/lists/*

# Copy SSH key and set permissions
# Make sure you build with --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_ed25519)"
ARG SSH_PRIVATE_KEY
RUN mkdir -p /root/.ssh && \
    echo "$SSH_PRIVATE_KEY" > /root/.ssh/id_ed25519 && \
    chmod 600 /root/.ssh/id_ed25519 && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . /app

EXPOSE 32848

CMD ["python", "-u", "main.py"]
