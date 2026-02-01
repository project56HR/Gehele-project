# Simple Ubuntu base Dockerfile
FROM node:25-slim
ENV DEBIAN_FRONTEND=noninteractive

# Install a few common utilities and clean apt cache
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    wget \
    git \
    nano \
    python3 \
    python3-venv \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

EXPOSE 3000
EXPOSE 32848

CMD ["bash", "run.sh"]