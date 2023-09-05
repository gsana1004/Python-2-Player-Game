from PIL import Image
from moviepy.editor import *

# Load the GIF
gif = VideoFileClip("/Users/gabrielsanandaji/pythongame/aa1cd0ed9505355ffffd836b67f28be43d271b44_hq.gif")

# Create a directory to store the resized frames
import os
output_dir = "resized_frames"
os.makedirs(output_dir, exist_ok=True)

# Resize and save each frame as a PNG image
frame_count = 0
for frame in gif.iter_frames(fps=10):
    # Resize the frame to fit the game
    resized_frame = Image.fromarray(frame).resize((POWERUP_SIZE, POWERUP_SIZE), Image.ANTIALIAS)
    
    # Save the resized frame as a PNG image
    resized_frame.save(os.path.join(output_dir, f"frame_{frame_count}.png"))
    frame_count += 1
