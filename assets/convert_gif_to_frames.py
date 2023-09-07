from moviepy.editor import *

# Define the desired size for the Power-Up frames
POWERUP_SIZE = (30, 30)

# Load the GIF
gif = VideoFileClip("/Users/gabrielsanandaji/pythongame/aa1cd0ed9505355ffffd836b67f28be43d271b44_hq.gif")

# Resize the frames to fit the game
frames = [frame.resize(POWERUP_SIZE) for frame in gif.iter_frames(fps=10)]

# Save the resized frames as PNG images
for i, frame in enumerate(frames):
    frame_image = ImageClip(frame)
    frame_image.save_frame(f"frame_{i}.png", t=i * (1 / 10))
