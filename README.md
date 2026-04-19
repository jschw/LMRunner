# LMRunner
LMRunner is a lightweight CLI for starting and managing local LLM inference endpoints backed by `llama.cpp`.

## Installation

### From source
```bash
git clone https://github.com/jschw/LMRunner.git
cd LMRunner
python -m pip install -e .
```

### With pip
If you want to compile llama-server by yourself or just download the binaries, just do:

```bash
python -m pip install --upgrade lmrunner
```
You will have to set the path according in llm_server_config.json .
Standard path of llama.cpp is <localhome>/lmrunner/Llamacpp/llama.cpp/build/bin/llama-server .

If you want to install the python-bindings for llama.cpp (easier but may not up-to-date):
```bash
python -m pip install --upgrade lmrunner[llamacppbindings]
```

### Run
```bash
./lmrunner
```

## Commands
Commands are entered inside the interactive prompt and always start with `/`.

| Command | Function |
| --- | --- |
| `/getconfigpaths` | Output the paths of LLM config files. |
| `/editlmconf` | Open `llm_config.json` in the default text editor. |
| `/editserverconf` | Open `llm_server_config.json` in the default text editor. |
| `/refreshconf` | Reload `llm_config.json` and `llm_server_config.json`. |
| `/updatemodels` | Update the LLM model catalog from GitHub and print the available models. |
| `/listendpoints` | List all available LLM endpoint configs. |
| `/startendpoint <name>` | Start a specific LLM endpoint by config name. |
| `/restartendpoint <name>` | Restart a specific LLM endpoint by config name. |
| `/stopendpoint <name>` | Stop a specific LLM endpoint by config name. |
| `/stopallendpnts` | Stop all LLM inference endpoints. |
| `/llmstatus` | Show the status of local LLM inference endpoints. |
| `/setautostartendpoint <name>` | Set a specific LLM endpoint for autostart on next startup. |
| `/help` | Show the help message. |
| `/exit` | Exit the CLI and stop running endpoints. |
