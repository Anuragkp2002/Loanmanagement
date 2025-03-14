# Use official Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /lmapp

# Copy only requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the port Django runs on
EXPOSE 8000

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "loanmanagement.wsgi:application"]