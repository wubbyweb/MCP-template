# MCP Hello World Example

This project demonstrates a simple implementation of the Model Context Protocol (MCP) using a Flask server and OpenAI integration. It showcases how to create an MCP server that provides a number addition function and a client that can use this function through OpenAI's function calling capabilities.

## Components

### Server (`server.py`)
- A Flask-based MCP server that implements:
  - A simple addition function (`add_numbers`)
  - MCP protocol endpoints for function listing and execution
  - JSON schema definition for the addition function
  - Runs on `http://localhost:8080`

### Client (`client.py`)
- Integrates with OpenAI's API and the MCP server
- Demonstrates:
  - Fetching available functions from the MCP server
  - Converting MCP functions to OpenAI function specifications
  - Making function calls through OpenAI's chat completions
  - Processing and displaying results

## Prerequisites

- Python 3.x
- OpenAI API key

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

1. Start the MCP server:
```bash
python server.py
```

2. In a separate terminal, run the client:
```bash
python client.py
```

The client will:
1. Connect to the MCP server
2. Fetch available functions
3. Start a conversation with OpenAI's model
4. Demonstrate function calling by adding two numbers (42 and 17)
5. Display the results

## Project Structure

```
.
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
├── server.py          # MCP server implementation
└── client.py          # OpenAI client implementation
```

## Dependencies

- `python-dotenv`: Environment variable management
- `openai`: OpenAI API client
- `flask`: Web server framework
- `requests`: HTTP client library

## Example Output

When running the client, you'll see:
1. Available MCP functions listing
2. Model's decision to use the addition function
3. Function execution results
4. Final response from the model

## Contributing

Feel free to submit issues and enhancement requests!