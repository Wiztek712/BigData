# Use official Python image
FROM python:3.12

# Set working directory inside the container
WORKDIR /app

# Copy only requirements.txt first for caching
COPY app/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copy the entire app directory
COPY app /app

# Expose port 8000
EXPOSE 8000

# Set entrypoint to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
