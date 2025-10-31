# --- Stage 1: Build Stage ---
# Use an official Python image as the base
FROM python:3.11-slim as builder

# Set the working directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# --- Stage 2: Final Stage ---
# Use a fresh slim image for a small final size
FROM python:3.11-slim

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy the application code
WORKDIR /home/app/web
COPY ./app /home/app/web/app

# Change ownership to the non-root user
RUN chown -R app:app /home/app/web
USER app

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]