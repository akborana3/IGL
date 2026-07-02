FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create thumbnail storage directory (HF Bucket mount point)
RUN mkdir -p /data/thumbnails

ENV PORT=7860

EXPOSE 7860

CMD ["sh", "-c", "echo \"===== Application Startup at $(date) =====\" && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860} --workers 1"]