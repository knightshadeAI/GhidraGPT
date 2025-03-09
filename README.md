# GhidraGPT
GhidraGPT is a Ghidra plugin that uses the OpenAI GPT API to provide explanations, analysis, and insights on decompiled functions. It supports user-provided prompts to guide GPT in various tasks, such as identifying vulnerabilities or clarifying complex code.

## Features

- **Reverse Engineering Assistance**  
  Provides GPT-based explanations for selected functions in Ghidra.

- **Optional Custom Prompt**  
  You can instruct GPT to perform a specific type of analysis, such as finding vulnerabilities or summarizing function behavior.

- **Integration with Ghidra**  
  Simple installation by placing `GhidraGPT.py` in Ghidra’s Script directory.

## Requirements

- **Ghidra 10.x+** (Tested on Ghidra 10.1+)
- **Python 2.7+** or **Jython** (bundled with Ghidra)
- **OpenAI GPT API Key**  
  Sign up at [OpenAI’s API Keys page](https://platform.openai.com/account/api-keys) and set an environment variable `OPENAI_API_KEY` or manually place the key in the script.

## Installation & Usage

1. Copy `GhidraGPT.py` to your `Scripts` folder within Ghidra.  
2. (Recommended) Set your API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="sk-..."
