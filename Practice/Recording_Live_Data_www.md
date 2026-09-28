### Recording Live Data & Sending it to Servers or The Cloud 

Step 1: Open cmd 
Step 2:

penCV (Just once)
Open your Command Prompt and make sure your computer has the tool it needs to talk to your webcam:

DOS
pip install opencv-python
Step 2: Create Your Recording Script
On your Desktop, create a new text file and name it record_and_push.py (make sure it doesn't end in .txt).

Open it in Notepad and paste this exact code inside:

Python
import cv2

# Open your webcam
cap = cv2.VideoCapture(0)

# Set up the video recorder (.avi format)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('my_movement.avi', fourcc, 20.0, (640, 480))

print("Recording active! Press 'q' on your keyboard inside the video window to stop...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Save and show the frame
    out.write(frame)
    cv2.imshow('Recording Movement', frame)

    # Press 'q' to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up and save the file
cap.release()
out.release()
cv2.destroyAllWindows()
print("Done! Saved as my_movement.avi")
Save and close the file.

Step 3: Record Your Video
Open your Command Prompt, go to your Desktop folder, and run your script:

DOS
cd /d C:\Users\dell\OneDrive\Desktop
python record_and_push.py
A camera window will pop up. When you're done recording, just click inside that video window and press the q key on your keyboard to stop. Your video (my_movement.avi) will instantly appear on your desktop!

Step 4: Push It Straight to the Cloud
Instead of dealing with storage limits or syncing apps, use Windows' built-in curl command to send your video straight to the cloud web server and save the receipt:

DOS
curl -X POST -F "file=@my_movement.avi" https://httpbin.org/post -o upload_response.txt
Watch the progress bar hit 100%, and you're all done! A neat little upload_response.txt file will show up on your desktop proving the cloud server successfully ingested your video payload.
