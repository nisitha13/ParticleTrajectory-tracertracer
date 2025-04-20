import cv2
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Manually enter the input directory containing the 60 frames
input_folder = r"C:\Users\gunar\Desktop\vids_classifications\output\test_frames_folders (individual_folders)\s2"
""
# Ensure the input folder exists
if not os.path.exists(input_folder):
    print("Error: The specified folder does not exist.")
    exit()

# Ask for separate output directories for CSV and plots
csv_output_directory = r"C:\Users\gunar\Desktop\vids_classifications\output\coordinates&plot_test (ALL TEST)\coordinates_test"
plot_output_directory = r"C:\Users\gunar\Desktop\vids_classifications\output\coordinates&plot_test (ALL TEST)\plots_test"

# Ensure the output directories exist
os.makedirs(csv_output_directory, exist_ok=True)
os.makedirs(plot_output_directory, exist_ok=True)

# Extract folder name for naming the output files
folder_name = os.path.basename(input_folder)
csv_filename = os.path.join(csv_output_directory, f"{folder_name}.csv")
plot_filename = os.path.join(plot_output_directory, f"{folder_name}_trajectory.png")

# Global variables for mouse dragging
drawing = False
center = None
radius = 0
first_frame_global = None

# Mouse callback function to draw a circle
def draw_circle(event, x, y, flags, param):
    global drawing, center, radius, first_frame_global

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        center = (x, y)
        radius = 0

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        radius = int(np.sqrt((x - center[0])**2 + (y - center[1])**2))
        temp_frame = first_frame_global.copy()
        cv2.circle(temp_frame, center, radius, (0, 255, 0), 2)
        cv2.imshow("Select Bacterium", temp_frame)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        radius = int(np.sqrt((x - center[0])**2 + (y - center[1])**2))
        cv2.circle(first_frame_global, center, radius, (0, 255, 0), 2)
        cv2.imshow("Select Bacterium", first_frame_global)
        cv2.waitKey(1)  # Brief delay to update the window
        cv2.destroyWindow("Select Bacterium")
        track_bacterium(input_folder, csv_filename, plot_filename, center, radius)

# Function to track bacterium
def track_bacterium(folder_path, csv_path, plot_path, circle_center, circle_radius):
    frame_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.jpg')])
    
    if len(frame_files) != 60:
        print("Warning: The folder does not contain exactly 60 frames.")
    
    if not frame_files:
        print("No frames found.")
        return

    # Convert circle to bounding box for tracker
    x1 = circle_center[0] - circle_radius
    y1 = circle_center[1] - circle_radius
    w = 2 * circle_radius
    h = 2 * circle_radius
    bbox = (x1, y1, w, h)

    # Initialize OpenCV CSRT Tracker
    tracker = cv2.legacy.TrackerCSRT_create()
    first_frame = cv2.imread(os.path.join(folder_path, frame_files[0]))
    tracker.init(first_frame, bbox)

    coordinates = []

    # Process all frames
    for frame_idx, frame_path in enumerate(frame_files):
        frame = cv2.imread(os.path.join(folder_path, frame_path))
        success, bbox = tracker.update(frame)

        if success:
            x, y, w, h = [int(i) for i in bbox]
            cx, cy = x + w // 2, y + h // 2  # Get center of bounding box
            
            # Calculate milliseconds based on frame index
            milliseconds = round(frame_idx * (2000 / 60))  # 2000ms for 60 frames
            
            # Store the frame index, time, and coordinates
            coordinates.append((frame_idx + 1, milliseconds, cx, cy))
            
            # Draw tracking visuals
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)
        
        # Show tracking visuals
        cv2.imshow("Tracking", frame)

        # Close tracking window when user presses 'q'
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

    # Convert to DataFrame and save to CSV
    df_new = pd.DataFrame(coordinates, columns=["Frame", "Milliseconds", "X", "Y"])
    df_new.to_csv(csv_path, index=False)

    # Plot the trajectory of the bacterium
    plt.figure(figsize=(6, 6))
    plt.plot(df_new["X"], df_new["Y"], marker="o", linestyle="-", color="blue")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title(f"Trajectory of {folder_name}")
    plt.gca().invert_yaxis()  # Invert y-axis to match image coordinates
    plt.grid()
    
    # Save the plot separately
    plt.savefig(plot_path)
    plt.show()

# Load the first frame and set up the window for ROI selection
first_frame_global = cv2.imread(os.path.join(input_folder, sorted([f for f in os.listdir(input_folder) if f.endswith('.jpg')])[0]))
cv2.namedWindow("Select Bacterium")
cv2.setMouseCallback("Select Bacterium", draw_circle)
cv2.imshow("Select Bacterium", first_frame_global)
cv2.waitKey(0)

print(f"Tracking complete. CSV saved at: {csv_filename}")
print(f"Plot saved at: {plot_filename}")