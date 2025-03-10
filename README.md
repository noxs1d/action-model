# Action Model
---
## Overview
Action Model is a FastAPI-based application that interacts with an LLM (GPT-4o-mini) to generate, validate, and execute Bash commands in a controlled environment. The system uses LangGraph for state management and Docker for script execution.

## Features
- 🛠 **FastAPI Backend**: Provides an API for handling user queries.
- ⚡ **Asynchronous Execution**: Uses `async/await` for non-blocking operations.
- 🤖 **LLM Integration**: Interacts with GPT-4o-mini to generate and validate Bash commands.
- 🔍 **Command Validation**: Ensures that generated commands are correct before execution.
- 🖥 **Bash Script Execution**: Runs validated commands inside a controlled Docker environment.
- 📜 **Session-Based Communication**: Supports thread-based execution with a session ID.

## Installation
### Prerequisites
- Python 3.9+
- Docker (for script execution)
- Virtual environment (recommended)

### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/action-model.git
   cd action-model
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
   - Create a `.env` file and add the necessary API keys.
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage
### Running the API Server
```bash
uvicorn fast:app --host 0.0.0.0 --port 8000
```
The API will be available at `http://localhost:8000/docs`

### Running the CLI Interface
```bash
python main.py
```
This will prompt you for a session ID and allow you to enter queries interactively.

## API Endpoints
### `POST /run`
- **Description**: Executes a user query and returns the LLM-generated response.
- **Request Body**:
  ```json
  {
    "thread_id": "12345",
    "query": "List all files in the current directory"
  }
  ```
- **Response**:
  ```json
  {
    "content": "ls -l"
  }
  ```

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

## Future Improvements
- 🛡 **Enhance Security**: Implement command whitelisting to prevent dangerous operations.
- 🚀 **Improve Async Handling**: Replace blocking `subprocess.run()` with `asyncio.create_subprocess_exec()`.
- ✅ **Add Unit Tests**: Use `pytest` to ensure API stability.
- 📊 **Implement Logging**: Improve debugging with structured logs.

## License
MIT License

## Author
[Nurmukhammed](https://github.com/your-profile)

