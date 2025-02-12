# Use a base image
FROM ubuntu:latest

# Install necessary packages
RUN apt-get update && apt-get install -y \
    openssh-server \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set up SSH
RUN mkdir /var/run/sshd
RUN echo 'root:rootpassword' | chpasswd  # Change 'rootpassword' to a strong password

# Allow root login
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expose SSH and Flask ports
EXPOSE 22 5000

# Start SSH and keep container running
CMD service ssh start && tail -f /dev/null
