FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --upgrade pip

# Using twitchio alpha version
RUN apt-get update && apt-get install -y git
RUN pip install -U git+https://github.com/PythonistaGuild/TwitchIO.git@dev/3.0 --force-reinstall

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="/app"
CMD ["python", "/app/efttroll/__main__.py"]
