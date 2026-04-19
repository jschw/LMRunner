import argparse
import appdirs
import os
import subprocess
import sys
from pathlib import Path
from lmrunner.lm_runner_core import LMRunner

def init():
    pass

def print_help():
    print("""Available commands:
        /getconfigpaths       Output the paths of LLM config files
        /editconfig           Open llm_config.json in the default text editor
        /updatemodels         Update the LLM model catalog from GitHub
        /listendpoints        List all available LLM endpoint configs
        /startendpoint        Start a specific LLM endpoint
        /restartendpoint      Restart a specific LLM endpoint
        /stopendpoint         Stop a specific LLM endpoint
        /stopallendpnts       Stop all LLM inference endpoints
        /llmstatus            Show the status of local LLM inference endpoints
        /setautostartendpoint Set a specific LLM endpoint for autostart
        /help                 Show this help message
        /exit                 Exit the CLI
        """)

def open_in_default_editor(file_path: Path):
    try:
        if sys.platform.startswith("darwin"):
            subprocess.Popen(["open", "-t", str(file_path)])
        elif os.name == "nt":
            os.startfile(file_path)
        else:
            subprocess.Popen(["xdg-open", str(file_path)])
        print(f"Opened {file_path} in the default text editor.")
    except Exception as exc:
        print(f"Failed to open {file_path}: {exc}")

def _render_table(headers, rows, title=None):
    columns = len(headers)
    widths = [len(h) for h in headers]
    for row in rows:
        for i in range(columns):
            cell = str(row[i]) if i < len(row) else ""
            widths[i] = max(widths[i], len(cell))

    def format_row(values):
        padded = [str(values[i]).ljust(widths[i]) for i in range(columns)]
        return "| " + " | ".join(padded) + " |"

    separator = "| " + " | ".join("-" * w for w in widths) + " |"
    lines = []
    if title:
        lines.append(title)
    lines.append(format_row(headers))
    lines.append(separator)
    for row in rows:
        row_values = [row[i] if i < len(row) else "" for i in range(columns)]
        lines.append(format_row(row_values))
    return "\n".join(lines)

def format_model_list(avail_models):
    headers = ["Model name", "Port", "Path", "HF Repo", "HF Repo File"]
    rows = []
    for model in avail_models:
        rows.append([
            model.get("name", ""),
            model.get("port", ""),
            model.get("model", ""),
            model.get("hf-repo", ""),
            model.get("hf-file", ""),
        ])
    return _render_table(headers, rows, title="Available LLM models:")

def main_app():
    CONFIG_DIR = Path(appdirs.user_config_dir(appname='llmrunner'))
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    llm_config_path        = CONFIG_DIR / 'llm_config.json'
    llm_server_config_path = CONFIG_DIR / 'llm_server_config.json'

    parser = argparse.ArgumentParser(description="LLM Runner CLI - Manage inference endpoints")
    parser.add_argument('--termux', action='store_true')
    args, _ = parser.parse_known_args()

    if args.termux:
        print("--> Termux special paths enabled.")

    # Start LLM server
    llm_server             = LMRunner(termux_paths=args.termux)
    llm_config_path        = llm_server.get_llm_config_path()
    llm_server_config_path = llm_server.get_llm_server_config_path()

    splash_text = r'''
    __    __  _______                             
   / /   /  |/  / __ \__  ______  ____  ___  _____
  / /   / /|_/ / /_/ / / / / __ \/ __ \/ _ \/ ___/
 / /___/ /  / / _, _/ /_/ / / / / / / /  __/ /    
/_____/_/  /_/_/ |_|\__,_/_/ /_/_/ /_/\___/_/     
                                                  '''

    print(splash_text)
    print_help()

    while True:
        try:
            user_input = input("lmrunner > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            llm_server.stop_all_processes()
            break

        if not user_input:
            continue

        if not user_input.startswith("/"):
            print("Commands must start with a slash. Type /help for available commands.")
            continue

        tokens = user_input.split()
        command = tokens[0].lower()
        args = tokens[1:]

        if command == "/getconfigpaths":
            print(f"  -> LLM server config path: {llm_server_config_path}")
            print(f"  -> LLM config path: {llm_config_path}")

        elif command == "/editconfig":
            open_in_default_editor(llm_config_path)

        elif command == "/updatemodels":
            update_models_ok = llm_server.update_model_catalog()
            if update_models_ok:
                models_avail = llm_server.get_endpoints()
                print(format_model_list(models_avail))
            else:
                print("Updating the LLM model catalog failed.")

        elif command == "/listendpoints":
            models_avail = llm_server.get_endpoints()
            print(format_model_list(models_avail))

        elif command == "/startendpoint":
            if len(args) != 1:
                print("Usage: /startendpoint <Endpoint config name>")
            else:
                _, output = llm_server.create_endpoint(args[0])
                print(output)

        elif command == "/restartendpoint":
            if len(args) != 1:
                print("Usage: /restartendpoint <Endpoint config name>")
            else:
                _, output = llm_server.restart_process(args[0])
                print(output)

        elif command == "/stopendpoint":
            if len(args) != 1:
                print("Usage: /stopendpoint <Endpoint config name>")
            else:
                _, output = llm_server.stop_process(args[0])
                print(output)

        elif command == "/stopallendpnts":
            output = llm_server.stop_all_processes()
            print("\n".join(output))

        elif command == "/llmstatus":
            endpoint_processes = llm_server.list_processes()
            if len(endpoint_processes) > 0:
                headers = ["Inference Endpoints"]
                rows = [[endpoint] for endpoint in endpoint_processes]
                print(_render_table(headers, rows))
            else:
                print("There are currently no running LLM inference endpoints.")

        elif command == "/setautostartendpoint":
            if len(args) != 1:
                print("Usage: /setautostartendpoint <LLM endpoint name>")
            else:
                set_ok = llm_server.set_autostart_endpoint(args[0])
                if set_ok:
                    print(
                        f"The LLM endpoint '{args[0]}' was set and will be started automatically on next startup."
                    )
                else:
                    print(
                        f"There was an error setting the LLM endpoint '{args[0]}' for automatic startup."
                    )
        
        elif command == "/help":
            print_help()
        
        elif command == "/exit":
            print("Exiting.")
            llm_server.stop_all_processes()
            break

        else:
            print(f"Unknown command: {command}. Type /help for available commands.")

def main():
    init()
    main_app()

# ----------------------------
# Run main application
# ----------------------------
if __name__ == "__main__":
    main()
