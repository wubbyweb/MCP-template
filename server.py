# mcp_server.py
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Define our addition function
def add_numbers(a, b):
    """Add two numbers together and return the result."""
    return a + b

# Define the function schema for the MCP protocol
FUNCTION_SCHEMA = {
    "name": "add_numbers",
    "description": "Add two numbers together",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {
                "type": "number",
                "description": "The first number"
            },
            "b": {
                "type": "number",
                "description": "The second number"
            }
        },
        "required": ["a", "b"]
    }
}

@app.route("/mcp/functions", methods=["GET"])
def list_functions():
    """Endpoint to list available functions."""
    return jsonify({
        "functions": [FUNCTION_SCHEMA]
    })

@app.route("/mcp/execute", methods=["POST"])
def execute_function():
    """Endpoint to execute a function."""
    data = request.json
    
    function_name = data.get("name")
    arguments = data.get("arguments", {})
    
    if function_name == "add_numbers":
        try:
            # Parse arguments as needed
            a = float(arguments.get("a", 0))
            b = float(arguments.get("b", 0))
            
            # Call the function
            result = add_numbers(a, b)
            
            # Return the result
            return jsonify({
                "result": result
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 400
    else:
        return jsonify({
            "error": f"Unknown function: {function_name}"
        }), 404

if __name__ == "__main__":
    print("Starting MCP server on http://localhost:8080")
    print(f"Available functions: {json.dumps([FUNCTION_SCHEMA], indent=2)}")
    app.run(host="0.0.0.0", port=8080)