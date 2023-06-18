# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot.py and imdb.py files to the container
COPY bot.py .
COPY imdb.py .

# Run the bot.py script when the container starts
CMD ["python", "bot.py"]
