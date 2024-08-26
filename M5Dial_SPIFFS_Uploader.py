import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import serial.tools.list_ports
from datetime import datetime
import webbrowser
import shutil

def get_path_in_bundle(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return filename

mkspiffs_path = get_path_in_bundle('mkspiffs.exe')

def get_esptool_cmd():
    python_executable = shutil.which("python")
    if not python_executable:
        log_message("Python executable not found in PATH.", "error")
        return None
    
    esptool_path = get_path_in_bundle('esptool/esptool.py')
    return [python_executable, esptool_path]

esptool_cmd = get_esptool_cmd()

DEBUG_MODE = False

def log_message(message, message_type="info"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_window.config(state=tk.NORMAL)
    
    if message_type == "success":
        log_window.insert(tk.END, f"[SUCCESS] {timestamp}: {message}\n", "success")
    elif message_type == "error":
        log_window.insert(tk.END, f"[ERROR] {timestamp}: {message}\n", "error")
    elif message_type == "info" and DEBUG_MODE:
        log_window.insert(tk.END, f"[INFO] {timestamp}: {message}\n", "info")
    
    log_window.config(state=tk.DISABLED)
    log_window.see(tk.END)

def list_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

def connect_to_device():
    flash_size = detect_flash_size()
    if flash_size:
        create_button.config(state=tk.NORMAL)
        connection_status.config(text="Connected", fg="green")
        log_message("Device connected and flash size detected successfully.", "success")
    else:
        connection_status.config(text="Not Connected", fg="red")
        log_message("Failed to connect to the device or detect flash size.", "error")
        create_button.config(state=tk.DISABLED)

def detect_flash_size():
    if esptool_cmd is None:
        return None
    try:
        cmd = esptool_cmd + ["--chip", "esp32s3", "--port", port_var.get(), "flash_id"]
        log_message(f"Running command: {' '.join(cmd)}", "info")
        log_message(f"Using Python executable: {esptool_cmd[0]}", "info")
        log_message(f"Current working directory: {os.getcwd()}", "info")

        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

        log_message(f"Command stdout: {result.stdout}", "info")
        log_message(f"Command stderr: {result.stderr}", "info")
        log_message(f"Return code: {result.returncode}", "info")

        if "Detected flash size:" in result.stdout:
            flash_size_str = result.stdout.split("Detected flash size:")[1].split()[0]
            flash_size = int(flash_size_str.replace("MB", "")) * 1024 * 1024
            return flash_size
        else:
            log_message("Flash size not detected.", "error")
            return None
    except Exception as e:
        log_message(f"Could not detect flash size: {e}", "error")
        return None

def create_spiffs_image():
    directory = filedialog.askdirectory(title="Select Directory to Pack into SPIFFS")
    if not directory:
        return
    
    output_file = filedialog.asksaveasfilename(defaultextension=".bin", title="Save SPIFFS Image As", filetypes=[("Binary files", "*.bin")])
    if not output_file:
        return

    block_size = 4096
    page_size = 256
    size = "0x160000"

    mkspiffs_cmd = f'"{mkspiffs_path}" -c "{directory}" -b {block_size} -p {page_size} -s {size} "{output_file}"'
    
    try:
        log_message("Creating SPIFFS image...", "info")
        subprocess.run(mkspiffs_cmd, check=True, shell=True)
        log_message("SPIFFS image created successfully!", "success")
    except subprocess.CalledProcessError as e:
        log_message(f"Failed to create SPIFFS image. Error: {e}", "error")

def upload_spiffs_image():
    spiffs_image = filedialog.askopenfilename(title="Select SPIFFS Image to Upload", filetypes=[("Binary files", "*.bin")])
    if not spiffs_image:
        return
    
    port = port_var.get()
    baud = "921600"
    address = "0x00290000"

    cmd = esptool_cmd + ["--chip", "esp32s3", "--port", port, "--baud", baud, "write_flash", "-z", address, spiffs_image]
    
    try:
        log_message("Uploading SPIFFS image...", "info")
        subprocess.run(cmd, check=True, shell=True)
        log_message("SPIFFS image uploaded successfully!", "success")
    except subprocess.CalledProcessError as e:
        log_message(f"Failed to upload SPIFFS image. Error: {e}", "error")

def show_help():
    help_text = (
        "1. Connect to the device to detect flash size and enable SPIFFS creation.\n"
        "2. Use 'Create SPIFFS Image' to generate a SPIFFS image from a directory.\n"
        "3. Use 'Upload SPIFFS Image' to upload the image to your ESP32 device.\n"
        "4. The tool will automatically detect the flash size and calculate the maximum allowable SPIFFS image size."
    )
    messagebox.showinfo("Help", help_text)

def open_link(url):
    webbrowser.open_new(url)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("M5Dial SPIFFS Uploader")

    create_icon = tk.PhotoImage(file="create_icon.png")
    connect_icon = tk.PhotoImage(file="connect_icon.png")
    upload_icon = tk.PhotoImage(file="upload_icon.png")
    root.iconbitmap("window_icon.ico")

    style = ttk.Style()
    style.theme_use("clam")

    root.configure(bg="#333333")
    style.configure("TFrame", background="#333333")
    style.configure("TLabel", background="#333333", foreground="#FFFFFF")
    style.configure("TButton", background="#FFA500", foreground="#FFFFFF", font=("Arial", 10), padding=6)
    style.map("TButton", background=[('active', '#FF8C00')], foreground=[('active', '#FFFFFF')])
    style.configure("TCombobox", fieldbackground="#333333", background="#666666", foreground="#FFFFFF")

    connection_frame = ttk.Frame(root, padding="10", style="TFrame")
    connection_frame.pack(padx=10, pady=10, fill="x")

    ttk.Label(connection_frame, text="COM Port:", style="TLabel").pack(side="left", padx=5)
    port_var = tk.StringVar(value="COM6")
    port_dropdown = ttk.Combobox(connection_frame, textvariable=port_var, values=list_serial_ports(), state="readonly", width=10)
    port_dropdown.configure(background="white", foreground="black")
    port_dropdown.pack(side="left", padx=5)

    connect_button = ttk.Button(connection_frame, text="Connect", command=connect_to_device, image=connect_icon, compound=tk.LEFT)
    connect_button.pack(side="left", padx=5)

    connection_status = tk.Label(connection_frame, text="Not Connected", fg="red", bg="#333333", font=("Arial", 10))
    connection_status.pack(side="left", padx=10)

    spiffs_frame = ttk.Frame(root, padding="10", style="TFrame")
    spiffs_frame.pack(padx=10, pady=10, fill="x")

    create_button = ttk.Button(spiffs_frame, text="Create SPIFFS Image", command=create_spiffs_image, state=tk.DISABLED, image=create_icon, compound=tk.LEFT)
    create_button.pack(fill="x", pady=5)

    esptool_frame = ttk.Frame(root, padding="10", style="TFrame")
    esptool_frame.pack(padx=10, pady=10, fill="x")

    upload_button = ttk.Button(esptool_frame, text="Upload SPIFFS Image", command=upload_spiffs_image, image=upload_icon, compound=tk.LEFT)
    upload_button.pack(fill="x", pady=10)

    log_frame = ttk.Frame(root, padding="10", style="TFrame")
    log_frame.pack(padx=10, pady=10, fill="both", expand=True)

    log_window = tk.Text(log_frame, height=10, bg="#000000", fg="#FFFFFF", wrap="word", state=tk.DISABLED)
    log_window.pack(fill="both", expand=True)
    log_window.tag_configure("success", foreground="green")
    log_window.tag_configure("error", foreground="red")

    credit_label = tk.Label(root, text="© dagnazty", fg="#FFA500", bg="#333333", font=("Arial", 10), cursor="hand2")
    credit_label.pack(pady=10)
    credit_label.bind("<Button-1>", lambda e: open_link("https://linktr.ee/dagnazty"))

    menu_bar = tk.Menu(root)
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Help", command=show_help)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    root.config(menu=menu_bar)

    root.mainloop()
