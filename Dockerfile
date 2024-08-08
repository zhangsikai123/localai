# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set the timezone environment variable
ENV TZ=Asia/Shanghai

# Update package lists and install necessary dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common vim net-tools \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update

# Install Python 3.11
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3.11 python3.11-dev python3.11-distutils python3-pip


# Install frontend
# TODO somtimes failed because of network issue, effect following steps because of cache
RUN apt-get install -y curl && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Set the working directory
WORKDIR /app

ENV NVM_DIR="/root/.nvm"

COPY frontend/package.json /app/frontend/package.json

RUN [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" \
	&& nvm install 20 \
	&& node --version \
	&& npm --version \
	&& npm install -g yarn

RUN [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" \
	&& cd /app/frontend && yarn add vite

# Display installed versions
RUN python3.11 --version
COPY backend/requirements.txt backend/requirements.txt
RUN pip install -r backend/requirements.txt

# Copy your application code into the container
COPY . /app

# Define the default command to run when the container starts
CMD ["/bin/bash"]
