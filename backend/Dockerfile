FROM python:3.11-slim

ARG QDRANT_VERSION=1.11.1

WORKDIR /app

# Install system dependencies
# build-essential, libssl-dev, libffi-dev, python3-dev are often needed for python packages
# libgomp1 is needed for onnxruntime (FastEmbed)
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  curl \
  ca-certificates \
  tar \
  build-essential \
  libssl-dev \
  libffi-dev \
  python3-dev \
  libgomp1 \
  && rm -rf /var/lib/apt/lists/*

# Qdrant binary installation removed - using Qdrant Cloud

ENV USE_FASTEMBED=true
ENV FASTEMBED_CACHE_PATH="/tmp/fastembed_cache"

COPY requirements-prod.txt .

RUN pip install --no-cache-dir -r requirements-prod.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Pre-download FastEmbed model to speed up startup
RUN mkdir -p ${FASTEMBED_CACHE_PATH} \
  && python -c "from langchain_community.embeddings.fastembed import FastEmbedEmbeddings; FastEmbedEmbeddings()"

COPY . .

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
