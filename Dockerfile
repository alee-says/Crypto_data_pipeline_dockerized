FROM apache/airflow:2.1.2-python3.8

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install your package
RUN pip install --no-cache-dir -e .