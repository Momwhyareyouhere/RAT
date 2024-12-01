import requests
import os


client_ngrok_url = input("Please enter the Ngrok URL: ")


def send_connect_request():
    target_url = f"{client_ngrok_url}/connect"
    data = {"message": "Connected"}
    
    try:
        response = requests.post(target_url, json=data)
        if response.status_code == 200:
            print("Successfully connected to client!")
            return response.json()
        else:
            print("Failed to connect.")
            return None
    except Exception as e:
        print(f"Error sending request to client: {e}")
        return None


def send_command_to_client(command):
    target_url = f"{client_ngrok_url}/terminal"
    data = {"command": command}
    
    try:
        response = requests.post(target_url, json=data)
        if response.status_code == 200:
            return response.json()['output']
        else:
            return "Error executing command"
    except Exception as e:
        return f"Error sending request: {e}"

def initiate_connection():
    response = send_connect_request()
    if response and response.get('status') == "Success":
        print("Connection established. Ready to receive commands.")
    else:
        print("Failed to connect to client. Exiting...")
        exit(1)


def main():
    initiate_connection()
    
    while True:
        command = input("shell > ")
        
        if command.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        
        output = send_command_to_client(command)
        
        if output:
            print("Output:\n", output)
        else:
            print("No output received or error occurred.")

if __name__ == "__main__":
    main()
