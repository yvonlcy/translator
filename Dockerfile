FROM python:3.10-slim

WORKDIR /app

COPY environment.yml .
COPY app.py .

# install dependencies directly with pip
RUN pip install --no-cache-dir gradio langdetect langchain-community langchain-core langchain-ollama

EXPOSE 7860

# set environment variables if needed

# ENV OLLAMA_BASE_URL=http://host.docker.internal:11434

CMD ["python", "app.py"]
