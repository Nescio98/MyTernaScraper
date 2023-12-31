FROM python:3.9

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable

# Installing Unzip
RUN apt-get install -yqq unzip

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
ENV DISPLAY=:99

ENV ENVIRONMENT="prod"
ENV SERVICE_NAME="scraper"
ENV AWS_DEFAULT_REGION="eu-west-1"

ENV DESTINATION_BUCKET=""
ENV DOWNLOAD_PATH="/app"
ENV QUEUE_NAME="test-scraper-tso"

ENV HISTORICAL="True"
ENV COMPANY="EGO Data"

# File to copy inside the container
# NB: You have to insert those also on bitbucket-pipelines condition in order to create the new image on file edit
COPY requirements.txt  ./

# Insert here app installation
RUN pip install -r requirements.txt

WORKDIR /app
# COPY src/* /app
COPY src/handler.py ./handler.py
COPY src/application/ ./application/

ENTRYPOINT [ "python" ]
CMD ["handler.py"]
