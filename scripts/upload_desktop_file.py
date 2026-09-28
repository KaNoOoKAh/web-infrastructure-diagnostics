import requests
import os

# Point straight to the file sitting on your desktop
desktop_path = os.path.expanduser(r"~\Desktop\my_movement.avi")

if not os.path.exists(desktop_path):
    print("Error: Could not find 'my_movement.avi' on your desktop.")
    exit()

print("Sending your raw video file up to the cloud as-is...")

# Uploading via a free transfer endpoint (transfer.sh)
url = "https://transfer.sh/my_movement.avi"

with open(desktop_path, "rb") as file_payload:
    response = requests.put(url, data=file_payload)

if response.status_code == 200:
    print("\nUpload complete! Your physical recording is now live in the cloud.")
    print("Download Link:", response.text.strip())
else:
    print(f"Upload failed with status code: {response.status_code}")
