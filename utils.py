import json
import os
import openai
from prompts_info import *

API_KEY = "your_openai_api_key"
openai.api_key = API_KEY

def print_arguments(args):
    """Print all input arguments."""
    print("\n=== Input Arguments ===")
    for arg, value in vars(args).items():
        print(f"{arg}: {value}")
    print("======================\n")

def load_json(file_path):
    """Load JSON data from a file."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)[:10]
    return []

def save_json(file_path, data):
    """Save JSON data to a file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def create_directory(path):
    """Create a directory if it does not exist."""
    os.makedirs(path, exist_ok=True)
    print(f"Directory '{path}' is ready.")

def initialize_output_file(file_path):
    """Ensure the output JSON file exists."""
    if not os.path.exists(file_path):
        save_json(file_path, [])
        print(f"Created output file: {file_path}")
    else:
        print(f"Output file already exists: {file_path}")

def get_prompt_components(prompt_method):
    """Retrieve the appropriate system prompt and examples based on the prompt method."""
    prompt_mappings = {
        "non_agent": (None, non_agent_system_prompt),
        "non_agent_cs": (None, non_agent_system_prompt),
        "original": (system_prompt, examples),
        "examples_updated_2n1s": (system_prompt, examples_updated_2n1s),
        "examples_updated_2s": (system_prompt, examples_updated_2s),
        "system_prompt_updated": (system_prompt_updated, examples),
        "system_prompt_updated_stop_2n": (system_prompt_updated_stop, examples),
        "system_prompt_updated_stop_2s": (system_prompt_updated_stop, examples_updated_2s),
    }
    return prompt_mappings.get(prompt_method, (system_prompt, examples))

def generate_response(llm_model, chat_messages):
    """Generate a response from OpenAI's API."""
    try:
        response = openai.ChatCompletion.create(
            model=llm_model,
            messages=chat_messages,
            max_tokens=2048
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Error generating response."