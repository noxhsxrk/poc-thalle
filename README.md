# poc-thalle

## Overview

poc-thalle is a project designed to demonstrate the capabilities of a chat interaction system using the THaLLE model. It processes user messages and generates responses based on predefined system prompts.

## Features

- **Chat Interaction**: Communicates with users by processing their messages and generating appropriate responses.
- **Logging**: Logs chat interactions to an Excel file for record-keeping and analysis.
- **Randomized System Prompts**: Selects system prompts randomly to provide varied responses.
- **Error Handling**: Captures and logs errors during API calls.

## Requirements

To run this project, you need the following Python packages:

- `requests`
- `pandas`
- `python-dotenv`

These can be installed using the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. **Set Up Environment Variables**: Ensure you have a `.env` file with the necessary environment variables, such as `ENDPOINT`.

2. **Prepare Message Files**: Create `user_message.txt` and `system_message.txt` files with the respective messages.

3. **Run the Script**: Execute the main script to start processing messages.

```bash
python main.py
```
