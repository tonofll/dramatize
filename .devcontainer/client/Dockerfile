FROM python:3.10.11

# there is no user to interact while building the image
ENV DEBIAN_FRONTEND=noninteractive

# /app is used to copy configuration scripts during img creation
WORKDIR /app

# system libraries
#COPY ./shared/dependencies.txt .
RUN apt update && \
    apt install -y --no-install-recommends \
    build-essential \
    pkg-config \
    make \
    curl \
    wget \
    git \
    graphviz && \
    rm -rf /var/lib/apt/lists/*

# create new user, 'vscdode' by default
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m -d /home/$USERNAME $USERNAME \
    && usermod --shell /bin/bash $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Change to the new user.
USER $USERNAME

# Install pre-commit and poetry using pip
RUN pip3 install --upgrade pip
RUN pip3 install poetry==1.4.0 pre-commit==3.2.0
ENV PATH="${PATH}:/home/${USERNAME}/.local/bin"

# set the default frontend back
ENV DEBIAN_FRONTEND=dialog

# Do nothing so the contaienr does not exit automatically.
CMD ["tail","-f","/dev/null"]