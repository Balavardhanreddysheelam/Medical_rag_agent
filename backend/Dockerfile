FROM python:3.11-slim

ARG QDRANT_VERSION=1.11.1

WORKDIR /app

# Install system dependencies
# build-essential, libssl-dev, libffi-dev, python3-dev are often needed for python packages
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  curl \
  ca-certificates \
  tar \
  build-essential \
  libssl-dev \
  libffi-dev \
  python3-dev \
  && rm -rf /var/lib/apt/lists/*

# Install Qdrant binary
# We download to a temp dir, find the binary, and move it to /opt/qdrant
RUN mkdir -p /tmp/qdrant_install \
  && curl -L "https://github.com/qdrant/qdrant/releases/download/v${QDRANT_VERSION}/qdrant-x86_64-unknown-linux-gnu.tar.gz" \
  | tar -xz -C /tmp/qdrant_install \
  && mkdir -p /opt/qdrant \
  && find /tmp/qdrant_install -name "qdrant" -type f -exec mv {} /opt/qdrant/qdrant \; \
  && chmod +x /opt/qdrant/qdrant \
  && rm -rf /tmp/qdrant_install

ENV PATH="/opt/qdrant:${PATH}"
ENV USE_FASTEMBED=true

COPY requirements-prod.txt .

RUN pip install --no-cache-dir -r requirements-prod.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

COPY . .

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
