FROM python:3.11-slim

ARG QDRANT_VERSION=1.11.1

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends curl ca-certificates tar \
  && rm -rf /var/lib/apt/lists/*

# Install Qdrant binary
RUN curl -L "https://github.com/qdrant/qdrant/releases/download/v${QDRANT_VERSION}/qdrant-x86_64-unknown-linux-gnu.tar.gz" \
  | tar -xz -C /opt \
  && mv /opt/qdrant-x86_64-unknown-linux-gnu /opt/qdrant

ENV PATH="/opt/qdrant:${PATH}"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

COPY . .

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
