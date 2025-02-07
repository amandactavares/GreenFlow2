FROM python:3.9-slim
#FROM ubuntu:20.04
WORKDIR /app
# Install APT package manager & dependencies for apturl
# RUN apt-get update && apt-get install -y \
#     python3 python3-pip apturl \
#     && rm -rf /var/lib/apt/lists/*
# # Set default Python (optional)
# RUN ln -s /usr/bin/python3 /usr/bin/python
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "src/api.py"]