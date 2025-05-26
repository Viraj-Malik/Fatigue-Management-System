## Prerequisites

*   **Hardware:**
    *   Raspberry Pi (Raspberry Pi 5)
    *   A compatible webcam.
    *   USB-Drive
*   **Software:**
    *   Raspberry Pi OS.
    *   Python 3.
    *   Other dependencies will be installed by the `start_fms.sh` script.

## Setup and Installation

The `start_fms.sh` script automates the installation of system dependencies, Python libraries, and the required dlib facial landmark model.

1.  **Clone or Download the Project:**
    Obtain all project files from GitHub and place them in the following directory "/home/$USER-ID$" for your Raspberry Pi 5. 
    Make sure the "start_fms.sh" file is outside the "FMS_DEMO-V1-Final" folder, and the folder and "start_fms.sh" file are in the above-mentioned directory. 

2.  **Make Setup Script Executable:**
    Open a new terminal window and run the following command.
    ```chmod +x setup_fms_project.sh```

3. **Setup on Startup Execution:**
    Type the following command in a terminal window
    ```crontab -e```
    Navigate to the bottom of this file and add the following 
    ```@reboot sudo /home/$USER-ID$/.start_fms.sh > /home/$USER-ID$/fms_cron_startup.log 2>&1```

4. **Validate:**
    Setup is now complete. Disconnect the monitor and all other devices. Connect the Raspberry Pi to power and the webcam. Light will blink blue in 30-45 seconds. 
