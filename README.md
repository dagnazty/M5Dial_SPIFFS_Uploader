# M5Dial SPIFFS Uploader

The M5Dial SPIFFS Uploader is a user-friendly tool for creating and uploading SPIFFS (SPI Flash File System) images to your M5Dial.

## Requirements for .py or building
1. ESPTool: Download from [Github](https://github.com/espressif/esptool)
2. SPIFFS: Download from [Github](https://github.com/igrr/mkspiffs)

## How to Use

### 1. Connecting to Your Device
- **Step 1**: Connect your M5Dial device to your PC via a USB cable.
- **Step 2**: Run the `M5Dial_SPIFFS_Uploader.exe`.
- **Step 3**: From the "COM Port" dropdown, select the correct COM port for your device.
- **Step 4**: Click the `Connect` button. The tool will attempt to detect the flash size of your device.

### 2. Creating a SPIFFS Image
- **Step 1**: After successfully connecting to the device, the `Create SPIFFS Image` button will be enabled.
- **Step 2**: Click `Create SPIFFS Image`.
- **Step 3**: Choose the directory containing the files you want to include in the SPIFFS image.
- **Step 4**: Save the SPIFFS image to your desired location.

### 3. Uploading the SPIFFS Image
- **Step 1**: Click `Upload SPIFFS Image`.
- **Step 2**: Select the SPIFFS image you created earlier.
- **Step 3**: The tool will upload the image to your M5Dial device.

## Notes
- **Admin Rights**: Running the tool with administrator privileges may be necessary for accessing COM ports and flashing the device.
- **COM Port Selection**: Ensure the correct COM port is selected before connecting to avoid connection issues.
- **Logs**: The log window will display real-time feedback, including successful operations and any errors encountered.
- **Serial Monitors**: All connections to the M5Dial should be closed before attempting to connect vua M5Dial SPIFFS Uploader. 

## License

**M5Dial SPIFFS Uploader**  
**Copyright © dagnazty**

All rights reserved.

### License Terms

1. **Use**: This software is provided free of charge for personal and commercial use. You may use this software on any number of devices for your own use.

2. **Distribution**: You may distribute this software freely, provided that the original software is not modified and that this license is included with all distributed copies.

3. **Modification**: You may not modify, adapt, or reverse-engineer this software in any way.

4. **Source Code**: The source code for this software is provided.

5. **Warranty Disclaimer**: This software is provided "as-is" without any warranty of any kind. The author is not liable for any damages arising from the use of this software.

6. **Support**: No official support or maintenance is provided for this software. However, updates may be released at the discretion of the author.

## Credits

Developed by [dagnazty](https://linktr.ee/dagnazty).
