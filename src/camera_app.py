import cv2
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import os
from datetime import datetime
from PIL import Image, ImageTk
import platform


class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CamRaw - Simple Camera App")
        self.root.geometry("800x650")
        self.root.resizable(True, True)
        
        # Initialize variables
        self.camera = None
        self.is_recording = False
        self.video_writer = None
        self.current_frame = None
        self.camera_thread = None
        self.running = False
        self.available_cameras = []
        self.selected_camera = 0
        
        # Create output directories
        self.ensure_output_dirs()
        
        # Setup GUI
        self.setup_gui()
        
        # Detect available cameras
        self.detect_cameras()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def ensure_output_dirs(self):
        """Ensure output directories exist"""
        os.makedirs("output/photos", exist_ok=True)
        os.makedirs("output/videos", exist_ok=True)
    
    def setup_gui(self):
        """Setup the GUI elements"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Camera selection frame
        camera_frame = ttk.LabelFrame(main_frame, text="Camera Selection", padding="5")
        camera_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        camera_frame.columnconfigure(1, weight=1)
        
        ttk.Label(camera_frame, text="Camera:").grid(row=0, column=0, padx=(0, 5))
        self.camera_var = tk.StringVar()
        self.camera_combo = ttk.Combobox(camera_frame, textvariable=self.camera_var, state="readonly")
        self.camera_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.camera_combo.bind('<<ComboboxSelected>>', self.on_camera_change)
        
        ttk.Button(camera_frame, text="Refresh Cameras", command=self.detect_cameras).grid(row=0, column=2)
        
        # Video display frame
        self.video_frame = ttk.LabelFrame(main_frame, text="Camera Preview", padding="5")
        self.video_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Video label
        self.video_label = ttk.Label(self.video_frame, text="Camera not started")
        self.video_label.pack(expand=True)
        
        # Control buttons frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        controls_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        # Buttons
        self.start_btn = ttk.Button(controls_frame, text="Start Camera", command=self.start_camera)
        self.start_btn.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.stop_btn = ttk.Button(controls_frame, text="Stop Camera", command=self.stop_camera, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.photo_btn = ttk.Button(controls_frame, text="Take Photo", command=self.take_photo, state="disabled")
        self.photo_btn.grid(row=0, column=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.video_btn = ttk.Button(controls_frame, text="Start Recording", command=self.toggle_recording, state="disabled")
        self.video_btn.grid(row=0, column=3, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def detect_cameras(self):
        """Detect available cameras"""
        self.available_cameras = []
        camera_names = []
        
        # Check for available cameras (try up to 10 camera indices)
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.available_cameras.append(i)
                # Try to get camera name or use generic name
                camera_names.append(f"Camera {i}")
                cap.release()
        
        if not self.available_cameras:
            camera_names = ["No cameras detected"]
            self.available_cameras = []
        
        # Update combobox
        self.camera_combo['values'] = camera_names
        if camera_names and camera_names[0] != "No cameras detected":
            self.camera_combo.current(0)
            self.selected_camera = self.available_cameras[0]
        
        self.status_var.set(f"Found {len(self.available_cameras)} camera(s)")
    
    def on_camera_change(self, event):
        """Handle camera selection change"""
        if self.available_cameras:
            index = self.camera_combo.current()
            self.selected_camera = self.available_cameras[index]
            
            # If camera is running, restart with new camera
            if self.running:
                self.stop_camera()
                self.root.after(500, self.start_camera)  # Restart after short delay
    
    def start_camera(self):
        """Start the camera"""
        if not self.available_cameras:
            messagebox.showerror("Error", "No cameras available!")
            return
        
        try:
            self.camera = cv2.VideoCapture(self.selected_camera)
            if not self.camera.isOpened():
                raise Exception("Could not open camera")
            
            # Set camera properties for better quality
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            self.running = True
            self.camera_thread = threading.Thread(target=self.update_frame, daemon=True)
            self.camera_thread.start()
            
            # Update button states
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            self.photo_btn.config(state="normal")
            self.video_btn.config(state="normal")
            
            self.status_var.set(f"Camera {self.selected_camera} started")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
            self.status_var.set("Failed to start camera")
    
    def stop_camera(self):
        """Stop the camera"""
        self.running = False
        
        if self.is_recording:
            self.stop_recording()
        
        if self.camera_thread:
            self.camera_thread.join(timeout=1.0)
        
        if self.camera:
            self.camera.release()
            self.camera = None
        
        # Clear video display
        self.video_label.config(image="", text="Camera stopped")
        
        # Update button states
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.photo_btn.config(state="disabled")
        self.video_btn.config(state="disabled")
        
        self.status_var.set("Camera stopped")
    
    def update_frame(self):
        """Update video frame in a separate thread"""
        while self.running and self.camera:
            ret, frame = self.camera.read()
            if ret:
                self.current_frame = frame.copy()
                
                # Convert frame for display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_pil = Image.fromarray(frame_rgb)
                
                # Resize frame to fit display
                display_size = (640, 480)
                frame_pil = frame_pil.resize(display_size, Image.Resampling.LANCZOS)
                
                frame_tk = ImageTk.PhotoImage(frame_pil)
                
                # Update GUI in main thread
                self.root.after(0, lambda: self.update_video_label(frame_tk))
                
                # Record frame if recording
                if self.is_recording and self.video_writer:
                    self.video_writer.write(frame)
            
            time.sleep(0.033)  # ~30 FPS
    
    def update_video_label(self, frame_tk):
        """Update video label with new frame"""
        if self.running:
            self.video_label.config(image=frame_tk, text="")
            self.video_label.image = frame_tk  # Keep a reference
    
    def take_photo(self):
        """Take a photo"""
        if self.current_frame is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output/photos/photo_{timestamp}.jpg"
            
            cv2.imwrite(filename, self.current_frame)
            self.status_var.set(f"Photo saved: {filename}")
            messagebox.showinfo("Photo Saved", f"Photo saved as:\n{filename}")
        else:
            messagebox.showerror("Error", "No frame available to capture!")
    
    def toggle_recording(self):
        """Toggle video recording"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start video recording"""
        if self.current_frame is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output/videos/video_{timestamp}.mp4"
            
            # Get frame dimensions
            height, width = self.current_frame.shape[:2]
            
            # Define codec and create VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter(filename, fourcc, 30.0, (width, height))
            
            if self.video_writer.isOpened():
                self.is_recording = True
                self.video_btn.config(text="Stop Recording")
                self.status_var.set(f"Recording to: {filename}")
            else:
                messagebox.showerror("Error", "Failed to start video recording!")
                self.video_writer = None
        else:
            messagebox.showerror("Error", "No frame available to record!")
    
    def stop_recording(self):
        """Stop video recording"""
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        
        self.is_recording = False
        self.video_btn.config(text="Start Recording")
        self.status_var.set("Recording stopped")
    
    def on_closing(self):
        """Handle window closing"""
        if self.running:
            self.stop_camera()
        
        # Clean up
        cv2.destroyAllWindows()
        self.root.destroy()


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = CameraApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.on_closing()


if __name__ == "__main__":
    main()