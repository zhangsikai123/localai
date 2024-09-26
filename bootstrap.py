import os
import socket
from backend.configs import API_SERVER
from backend.configs import LLM_MODEL
import subprocess
from backend.server.chat.models import model_list

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to a known external server
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except socket.error:
        raise Exception("Unable to get local IP address")
    

def main():
    print("Welcome using localai\n")
    options = []
    model_name_list = model_list.keys()
    while True:
        print("\nOptions:")
        for idx, model_name in enumerate(model_name_list):
            options.append((idx + 1, model_name))
            print(f"{idx + 1}. {model_name}")

        print(f"{len(model_name_list) + 1}. Exit")

        choice = int(input("Select an option: "))
        if choice <= len(model_name_list):
            model_name = options[choice - 1][1]
            model_conf = model_list[model_name]
            model_provider = model_conf["provider"]
            if model_provider == "OpenAI":
                api_key = input("Enter API_KEY: ")
                os.environ["API_KEY"] = api_key
                print(f"API_KEY: {os.getenv('API_KEY')}")
                
            ip_address = get_local_ip()
            port = API_SERVER["port"]
            os.environ["VITE_BASE_URL"] = f"http://{ip_address}:{port}"
            os.environ["MODEL_NAME"] = model_name
            print(f"vist: {os.getenv('VITE_BASE_URL')}")

            os.system("make backend && make frontend")
            # tail logs from backend.log and frontend.log
            try:
                with subprocess.run(["tail", "-f", "backend.log", "frontend.log"]) as proc:
                    while True:
                        # Read output line by line
                        line = proc.stdout.readline()
                        if not line:
                            break
                        print(line.decode().strip())
            except KeyboardInterrupt:
                # catch KeyboardInterrupt to stop tailing logs
                print("Stopping backend and frontend...")
                os.system("make stop-backend")
                os.system("make stop-frontend")
            finally:
                pass
            break
        elif choice == len(model_name_list) + 1:
            break
        else:
            print("Invalid choice. Please select a valid option.")
    print("Bye!")


if __name__ == "__main__":
    main()
