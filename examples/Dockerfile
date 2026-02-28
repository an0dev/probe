# This is a Dockerfile for using an isolated instance of Probe

# Start with Python 3.11
FROM python:3.11

# Replace <your_openai_api_key> with your own key
ENV OPENAI_API_KEY <your_openai_api_key>

# Install Probe
RUN pip install probe


# To run the container

# docker build -t probe .
# docker run -d -it --name probe-instance probe
# docker attach probe-instance

# To mount a volume
# docker run -d -it -v /path/on/your/host:/path/in/the/container --name probe-instance probe
