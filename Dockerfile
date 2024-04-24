FROM python:3.8
# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . /app/

#Expose the port the app runs in
EXPOSE 7755

# Start Bash Script
ENTRYPOINT ["/bin/bash", "run.sh"]


