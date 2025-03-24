# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Mounted SSL key cert 
chmod 600 /mnt2/cr-sql-client-key
chmod 644 /mnt1/cr-sql-client-cert
chmod 644 /mnt3/cr-sql-server-ca


# Run app.py when the container launches
CMD ["python", "test_cloud_sql.py"]
