# set_webhook.py

# Prompt the user to enter the Discord webhook URL
webhook_url = input("Enter the Discord webhook URL: ")

# Open the client.py file and read its contents
with open("client.py", "r") as file:
    lines = file.readlines()

# Search for the line containing DISCORD_WEBHOOK_URL and replace it with the new URL
for i, line in enumerate(lines):
    if "DISCORD_WEBHOOK_URL" in line:
        lines[i] = f"DISCORD_WEBHOOK_URL = '{webhook_url}'\n"
        break

# Write the modified contents back to the client.py file
with open("client.py", "w") as file:
    file.writelines(lines)

print("Webhook URL has been updated in client.py.")
