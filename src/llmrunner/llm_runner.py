import argparse
import appdirs
from pathlib import Path
from .llm_runner import LlmRunner

def init():
    pass

def print_help():
    print("""Available commands:
        /getconfig           Output the paths of app config and llm config files
        /help                Show this help message
        /exit                Exit the CLI
        """)

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
    llm_server             = LlmRunner(termux_paths=args.termux)
    llm_config_path        = llm_server.get_llm_config_path()
    llm_server_config_path = llm_server.get_llm_server_config_path()


    print("----> LLM Runner CLI.<----\n\n")
    print_help()

    while True:
        try:
            user_input = input("chatshell > ").strip()
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

        if command == "/getconfig":
            #print(f"  -> App config path: {app_conf_path}")
            print(f"  -> LLM server config path: {llm_server_config_path}")
            print(f"  -> LLM config path: {llm_config_path}")
        
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
