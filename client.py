# openai_client.py
import os
import json
import requests
from openai import OpenAI

# Configure OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY", "your-api-key-here"),
)

# MCP server details
MCP_SERVER_URL = "http://localhost:8080/mcp"

def get_available_functions():
    """Get the list of available functions from the MCP server."""
    response = requests.get(f"{MCP_SERVER_URL}/functions")
    return response.json().get("functions", [])

def execute_function(name, arguments):
    """Execute a function on the MCP server."""
    response = requests.post(
        f"{MCP_SERVER_URL}/execute",
        json={"name": name, "arguments": arguments}
    )
    return response.json()

def main():
    # Get available functions from MCP server
    available_functions = get_available_functions()
    
    print("Available MCP functions:")
    print(json.dumps(available_functions, indent=2))
    
    # Create function mapping for OpenAI
    tools = []
    for function in available_functions:
        tools.append({
            "type": "function",
            "function": function
        })
    
    # Start a conversation with the model
    print("\nStarting chat with OpenAI model...")
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant that can add numbers using a special function."},
        {"role": "user", "content": "Can you add 42 and 17 for me?"}
    ]
    
    # First, get the model's response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or another model that supports tool calling
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    messages.append(response_message)
    
    # Check if the model wants to call a function
    if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
        # Process each tool call
        for tool_call in response_message.tool_calls:
            if tool_call.type == 'function':
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"Model wants to call function: {function_name}")
                print(f"With arguments: {function_args}")
                
                # Call the function via MCP server
                function_response = execute_function(function_name, function_args)
                print(f"Function response: {function_response}")
                
                # Add the function response to the messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(function_response)
                })
        
        # Get a new response from the model
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        # Print the final result
        final_response = second_response.choices[0].message.content
        print("\nFinal response:")
        print(final_response)
    else:
        # Model didn't call a function
        print("\nModel response without function calling:")
        print(response_message.content)

if __name__ == "__main__":
    main()