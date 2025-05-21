# Dockerfile
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev && \
    apt-get clean

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Port (Render uses this)
EXPOSE 8000

RUN python manage.py migrate
# Start app
CMD ["gunicorn", "taskmanagement.wsgi:application", "--bind", "0.0.0.0:8000"]
