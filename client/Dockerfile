FROM python:3.10.11-slim

WORKDIR /src

RUN apt update && apt install -y build-essential pkg-config libssl-dev

# Install poetry
RUN pip3 install poetry==1.3.2

COPY poetry.lock pyproject.toml ./

# Install project dependencies
RUN poetry install

COPY . .

CMD ["poetry","run","python","launcher.py"]