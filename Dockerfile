FROM ubuntu:latest

# Update sources and install git
RUN apt-get update -y && apt-get install -y git python3-pip apt upgrade -y

#Git configuration
RUN git config --global user.name "tiagomatias930" \
    && git config --global user.email "tiagomatias072@gmail.com"

# Clone SETOOLKIT
RUN git clone --depth=1 git@github.com:tiagomatias930/setoolkit-pt.git

# Change Working Directory
WORKDIR /social-engineer-toolkit-pt

 # Install requirements
RUN pip3 install -r requirements.txt

# Install SETOOLKIT
RUN python3 setup.py 

ENTRYPOINT [ "./setoolkit" ]

    
