# Configuration for running Selenium tests in a Docker container with Chrome and Firefox
# with tests written in Python and using the Selenium WebDriver API.

# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install the Selenium Python package
RUN pip install selenium

# Install the Chromium browser and the Chrome WebDriver
RUN apt update
RUN apt install -y chromium chromium-driver curl

# Run the tests
CMD ["python", "run_tests.py"]

# Set ENV DISPLAY to 99
ENV DISPLAY=:99
