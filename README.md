# Action Model

## Overview

Action Model is a FastAPI-based application that interacts with an LLM (GPT-4o-mini) to generate, validate, and execute Bash commands in a controlled environment. The system uses LangGraph for state management and Docker for script execution.

## Features

🛠 **FastAPI Backend**: Provides an API for handling user queries.

⚡ **Asynchronous Execution**: Uses async/await for non-blocking operations.

🤖 **LLM Integration**: Interacts with GPT-4o-mini to generate and validate Bash commands.

🔍 **Command Validation**: Ensures that generated commands are correct before execution.

🖥 **Bash Script Execution**: Runs validated commands inside a controlled Docker environment.

📜 **Session-Based Communication**: Supports thread-based execution with a session ID.

## File Structure

```
.
├── fast.py           # FastAPI application
├── main.py           # CLI-based interaction
├── model.py          # LangGraph state management & LLM interactions
├── script.py         # Bash script execution logic
├── templates/        # Prompt templates for LLM
├── requirements.txt  # Python dependencies
└── README.md         # Documentation
```

## Installation & Usage (Docker)

### Prerequisites
- Docker (for script execution)
- OpenAI API Key (required for LLM interactions)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/noxs1d/action-model.git
   cd action-model
   ```
2. **Set up environment variables**
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```
3. **Build the Docker image**
   ```bash
   docker build -t action-model .
   ```
4. **Run the container**
   ```bash
   docker run -p 8000:8000 --env OPENAI_API_KEY=$OPENAI_API_KEY --name action-model action-model
   ```

The API will be available at `http://localhost:8000/docs`.

## Future Improvements

- 🛡 **Enhance Security**: Implement command whitelisting to prevent dangerous operations.
- 🚀 **Improve Async Handling**: Replace blocking `subprocess.run()` with `asyncio.create_subprocess_exec()`.
- ✅ **Add Unit Tests**: Use `pytest` to ensure API stability.
- 📊 **Implement Logging**: Improve debugging with structured logs.


## Author

[Nurmukhammed](https://github.com/noxs1d)

