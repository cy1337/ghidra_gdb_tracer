# Use an official Ubuntu base image
FROM ubuntu:latest

# Install necessary packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gdb \
    python3 \
    libcjson-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Optionally, configure sudo to allow the user to run commands without a password
WORKDIR /demo
RUN wget http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.22_amd64.deb
RUN dpkg -i libssl1.1_1.1.1f-1ubuntu2.22_amd64.deb
COPY CommandServer /demo
COPY CommandClient.py /demo
COPY gdb_script.py /demo

EXPOSE 8080

CMD ["bash"]
