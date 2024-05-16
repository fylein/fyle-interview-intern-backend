FROM python:3.10

# Set environment variables for Flask
ENV FLASK_APP=core/server.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# expose port
EXPOSE 5000

# run app
CMD ["bash", "run.sh"]