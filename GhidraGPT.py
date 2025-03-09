# GhidraGPT: Ghidra plugin for GPT-based function analysis.
# @author HMasic
# @category Analysis
# @keybinding Ctrl-Alt-G
# @menupath Tools.GhidraGPT
# @toolbar

import os
import json
import urllib2
from ghidra.util.task import TaskMonitor
from ghidra.app.decompiler import DecompInterface

# Customize these as needed.
API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4"
MAX_TOKENS = 1024

def get_decompiled_function():
    """Returns (function, c_code) for the currently selected function."""
    monitor = TaskMonitor.DUMMY
    decompiler = DecompInterface()
    decompiler.openProgram(currentProgram)

    addr = currentLocation.getAddress()
    func = getFunctionContaining(addr)
    if not func:
        raise ValueError("No function selected.")
    results = decompiler.decompileFunction(func, 30, monitor)
    if not results or not results.getDecompiledFunction():
        raise ValueError("Decompilation failed.")
    return func, results.getDecompiledFunction().getC()

def build_prompt(func, code, user_prompt=None):
    """Builds a GPT prompt with optional user instructions."""
    msg = (
        "This is decompiled code from a reverse-engineering context.\n\n"
        "Signature:\n{}\n"
        "Name: {}\n\n"
        "Code:\n{}\n\n"
    ).format(func.getSignature(), func.getName(), code)
    if user_prompt:
        msg += "\nAdditional instructions:\n" + user_prompt
    return msg

def call_gpt_api(prompt):
    """Calls OpenAI Chat API with the given prompt and returns the response."""
    if not API_KEY:
        raise ValueError("OpenAI API key not provided.")
    data = json.dumps({
        "model": OPENAI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": MAX_TOKENS,
        "temperature": 0.7
    })
    request = urllib2.Request(OPENAI_URL, data, {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + API_KEY
    })
    try:
        resp = urllib2.urlopen(request)
        resp_data = json.loads(resp.read())
    except urllib2.HTTPError as e:
        raise ValueError("HTTP Error: {}".format(e.read()))
    if "error" in resp_data:
        raise ValueError("OpenAI Error: {}".format(resp_data["error"]))
    choices = resp_data.get("choices")
    if not choices:
        raise ValueError("No response from GPT.")
    return choices[0]["message"]["content"]

def run():
    """Main script entry point in Ghidra."""
    user_in = askString(
        "GhidraGPT Prompt",
        "Enter an optional instruction for GPT (leave blank for general explanation)."
    )
    if user_in is None:
        return
    try:
        func, c_code = get_decompiled_function()
    except ValueError as e:
        print("[ERROR]", e)
        return
    prompt = build_prompt(func, c_code, user_in)
    try:
        answer = call_gpt_api(prompt)
    except ValueError as e:
        print("[ERROR]", e)
        return
    print("\n--- GhidraGPT Analysis for '{}' ---".format(func.getName()))
    print(answer)
    print("--- End of GhidraGPT Output ---\n")
