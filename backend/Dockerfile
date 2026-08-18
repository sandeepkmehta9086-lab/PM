FROM node:22-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv \
    && uv pip install --system --no-cache "fastapi>=0.109.0" "httpx>=0.27.0" \
    "python-dotenv>=1.0.0" "uvicorn[standard]>=0.24.0"

COPY backend/ /app/backend/
COPY --from=frontend-builder /app/frontend/out /app/frontend/out

EXPOSE 8000

WORKDIR /app/backend

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
