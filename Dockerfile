## TODO: The following could be replaced with "mcp/sqlite" from "hub.docker.com" registry
FROM ubuntu:latest

RUN echo "Fun:  Debuggin is here"

# Documentation says reliability.
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 python3-pip sqlite3 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./app /app
COPY ./requirements.txt .

# TODO: Yes, I know, "never break user space".
RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python3", "main.py"]
