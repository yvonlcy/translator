# AI Translator

A powerful AI-based text translation tool using LLM models via Ollama, with a user-friendly Gradio interface.

## ✨ Features

- 🌐 Supports translation between 20+ languages
- 🔍 Automatic language detection
- 🔄 Easy language swapping
- 🤖 Model flexibility: Works with any Ollama-compatible LLM (Gemma3, Llama3, Mixtral, Yi, Qwen, etc.)
- 💻 Clean and intuitive user interface
- 🌍 Multi-language UI support (English, Simplified Chinese, Hong Kong Traditional Chinese)

## 🔧 Prerequisites

- Python 3.10+
- Ollama running with Gemma3 or other compatible LLM model
- Docker & Docker Compose (for containerized deployment)

## 🚀 Installation

### Ollama Setup

Before using the translator, ensure you have Ollama installed and at least one language model pulled:

```bash
# Install Ollama (if not already installed)  
# Follow instructions at https://ollama.com/download

# Pull your preferred model
ollama pull gemma3   # Default model
# Or choose other models
ollama pull llama3
ollama pull mixtral
# etc.
```

### Local Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/translator.git
   cd translator
   ```

2. Install dependencies:
   ```bash
   pip install gradio langdetect langchain-community langchain-core langchain-ollama
   ```

3. Run the application:
   ```bash
   python app.py
   ```

### Docker Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/translator.git
   cd translator
   ```

2. Create a `docker-compose.yml` file based on the template:
   ```bash
   cp docker-compose.template.yml docker-compose.yml
   ```

3. Edit the `docker-compose.yml` file to configure your environment (see Configuration section)

4. Build and run the container:
   ```bash
   docker-compose up -d
   ```

## 🎮 Usage

1. Access the UI at `http://localhost:7861` (local installation) or at your configured URL for Docker deployment

2. Select the source and target languages from the dropdown menus

3. Enter text in the source language text area

4. Click the "Translate" button to get your translation

5. Use the language switcher button to reverse the translation direction

## ⚙️ Configuration

### Environment Variables

- `OLLAMA_BASE_URL`: URL of your Ollama instance (default: `http://localhost:11434`)
- `OLLAMA_MODEL`: Model to use for translation (default: `gemma3:latest`). You can choose any Ollama-compatible model (e.g., `llama3`, `mixtral`, `yi`, `qwen`, etc.) based on your preferences and translation quality requirements
- `GRADIO_SERVER_NAME`: Server address (default: `0.0.0.0`)
- `GRADIO_SERVER_PORT`: Server port (default: `7861`)
- `GRADIO_ROOT_PATH`: Optional root path for the application

### Docker Deployment

The application can be deployed using Docker with Traefik as a reverse proxy. The `docker-compose.template.yml` file provides a starting point for your configuration:

- Update the image name to match your registry
- Configure the environment variables as needed
- Adjust volume mappings for logs and outputs
- Modify Traefik labels for your domain and routing

## 🌍 Multi-language Support

The UI supports the following languages:

- English (en.json)
- Simplified Chinese (cn.json)
- Hong Kong Traditional Chinese (hk.json)

Language files are located in the `language/` directory and can be customized or extended.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
