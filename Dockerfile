# syntax=docker/dockerfile:1

# --- Backend Stage ---
FROM python:3.10-slim AS backend
WORKDIR /app/backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend .

# --- Dashboard Stage ---
FROM python:3.10-slim AS dashboard
WORKDIR /app/dashboard
COPY dashboard/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY dashboard .

# --- Final Stage ---
FROM python:3.10-slim
WORKDIR /app
COPY --from=backend /app/backend ./backend
COPY --from=dashboard /app/dashboard ./dashboard
COPY .env.example .env

# Install both backend and dashboard dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt && \
    pip install --no-cache-dir -r dashboard/requirements.txt

EXPOSE 8000 8050

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & python dashboard/main.py"] 