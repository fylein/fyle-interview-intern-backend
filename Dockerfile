FROM python:3.8-slim-buster

# Set working directory
WORKDIR /app

# Copy the entire local directory into the image
COPY . /app

# Activate virtual environment and install dependencies
RUN pip install -r requirements.txt
EXPOSE 4040
# Run bash script
CMD ["bash", "run.sh"]
