FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.11-bullseye

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=vscode
ENV POSTGRES_PASSWORD=vscode

# Set version of Node and Vue CLI
ENV NODE_VERSION=20.17

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openssh-client \
        build-essential \
        cmake && \ 
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


    # installs nvm (Node Version Manager)
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash 

RUN sudo apt update && \
    sudo apt-get install -y postgresql

RUN sudo service postgresql start && \
    sudo -u postgres psql -c "CREATE USER vscode WITH PASSWORD 'vscode' CREATEDB;" && \
    sudo -u vscode createdb trivia

WORKDIR /
