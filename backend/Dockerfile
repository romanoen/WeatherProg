FROM python:3.9

WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . /app

EXPOSE 5000
ENV FLASK_APP=api.py
CMD ["flask", "run", "--host=0.0.0.0"]
