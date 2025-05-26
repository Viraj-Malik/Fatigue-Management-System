
## Prerequisites

*   **Hardware:**
    *   Raspberry Pi (Raspberry Pi 5)
    *   A compatible webcam.
*   **Software:**
    *   Raspberry Pi OS.
    *   Python 3.
    *   Other dependencies will be installed by the `setup_fms_project.sh` script.

## Setup and Installation

The `setup_fms_project.sh` script automates the installation of system dependencies, Python libraries, and the required dlib facial landmark model.

1.  **Clone or Download the Project:**
    Obtain all project files (`FMS-Demo-v1.py`, `setup_fms_project.sh`, `run_fms_demo.sh`, and your `alert_sys_v1.py`) and place them in a single directory.

2.  **Navigate to the Project Directory:**
    Open a terminal and change to the directory where you saved the files:
    ```bash
    cd /path/to/your/project_directory
    ```

3.  **Make Setup Script Executable:**
    ```bash
    chmod +x setup_fms_project.sh
    ```

4.  **Run the Setup Script:**
    ```bash
    ./setup_fms_project.sh
    ```
    *   This script will use `sudo` to install system packages, so you might be prompted for your password.
    *   It will create a Python virtual environment named `fms_env` in the project directory.
    *   It will install Python libraries (OpenCV, dlib, NumPy, SciPy, imutils) into this virtual environment.
    *   It will download `shape_predictor_68_face_landmarks.dat`.

    **IMPORTANT:** The installation of `dlib` (especially on a Raspberry Pi) involves compiling from source and can take a **very long time** (potentially 30 minutes to over an hour). Please be patient and ensure your Raspberry Pi has adequate cooling.

## Usage

Once the setup is complete:

1.  **Make Run Script Executable (if not already done):**
    ```bash
    chmod +x run_fms_demo.sh
    ```

2.  **Run the Application:**
    ```bash
    ./run_fms_demo.sh
    ```
    This script will:
    *   Activate the `fms_env` virtual environment.
    *   Execute the `FMS-Demo-v1.py` script.
    *   Deactivate the virtual environment when the application is closed.

3.  **Interacting with the Application:**
    *   A window titled "Drowsiness Detector" will appear showing the webcam feed with overlays.
    *   Press **'q'** or **ESC** in the OpenCV window (or Ctrl+C in the terminal) to quit the application.

### Command-Line Arguments for `FMS-Demo-v1.py`

The `FMS-Demo-v1.py` script (and thus `run_fms_demo.sh`) accepts the following arguments:

*   `-w` or `--webcam`: Index of the webcam on your system (default: `0`).
    *   Example: `./run_fms_demo.sh --webcam 1` (if your desired webcam is at index 1)
*   `-p` or `--shape-predictor`: Path to the facial landmark predictor file (default: `shape_predictor_68_face_landmarks.dat` in the current directory). The setup script downloads this to the correct default location.

## How It Works

1.  **Video Capture:** Captures frames from the specified webcam using OpenCV.
2.  **Face Detection:** Uses dlib's HOG-based frontal face detector to locate faces in each frame.
3.  **Facial Landmark Prediction:** For each detected face, dlib's shape predictor (using `shape_predictor_68_face_landmarks.dat`) identifies 68 facial landmarks.
4.  **Eye Aspect Ratio (EAR):**
    *   Calculates the EAR for both eyes using the coordinates of the eye landmarks.
    *   Averages the EAR from both eyes.
    *   Applies smoothing to the EAR over a small window of frames.
    *   If the smoothed EAR falls below `EYE_AR_THRESH` for `EYE_AR_CONSEC_FRAMES`, a drowsiness alert is triggered.
5.  **Yawn Detection:**
    *   Calculates the vertical distance between the mean points of the upper and lower inner lip landmarks.
    *   If this distance exceeds `YAWN_THRESH` for `YAWN_CONSEC_FRAMES`, a yawn alert is triggered.
6.  **Alert System:**
    *   When an alert condition is met, the script calls `os.system("sudo python3 alert_sys_v1.py")`.
    *   You need to provide your own `alert_sys_v1.py` script to handle the actual alert mechanism (e.g., play a sound, flash an LED via GPIO). **Ensure `alert_sys_v1.py` is executable and handles any `sudo` requirements if it accesses hardware.**

## Customization

You can modify the following constants at the beginning of `FMS-Demo-v1.py`:

*   `EYE_AR_THRESH`: Threshold for EAR to consider eyes closed/closing.
*   `EYE_AR_CONSEC_FRAMES`: Number of consecutive frames with low EAR to trigger a drowsiness alert.
*   `YAWN_THRESH`: Threshold for lip distance to consider a yawn.
*   `YAWN_CONSEC_FRAMES`: Number of consecutive frames with high lip distance to trigger a yawn alert.
*   `EAR_SMOOTHING_WINDOW`: Number of frames for EAR smoothing.

## Troubleshooting

*   **"dlib installation failed" or very slow:** Ensure your Raspberry Pi has enough RAM, disk space, and is adequately cooled during the `setup_fms_project.sh` script execution. Consider using a swap file if RAM is limited, but this will be slow.
*   **"No module named 'cv2' / 'dlib' / etc.":** Make sure you are running the application using `run_fms_demo.sh`, which activates the correct virtual environment. If you ran `setup_fms_project.sh` and it completed, the libraries should be in `fms_env/`.
*   **Webcam not working:**
    *   Ensure the webcam is properly connected.
    *   Try a different webcam index with the `--webcam` argument (e.g., `./run_fms_demo.sh --webcam 1`).
    *   Check if other applications can access the webcam (e.g., `guvcview` on Linux).
*   **`alert_sys_v1.py` not working:**
    *   Ensure the file `alert_sys_v1.py` exists in the same directory.
    *   Ensure it's executable and works when called directly (e.g., `sudo python3 alert_sys_v1.py`).
    *   The call `os.system("sudo python3 alert_sys_v1.py")` is blocking. For a more responsive UI, consider running the alert in a separate thread or process.

## Dependencies

Managed by `setup_fms_project.sh`.

*   **Python Libraries:**
    *   `numpy`
    *   `scipy`
    *   `imutils`
    *   `dlib`
    *   `opencv-python`
*   **System Libraries (examples, actual list in setup script):**
    *   `build-essential`, `cmake`, `pkg-config`
    *   `libjpeg-dev`, `libpng-dev`, `libtiff-dev`
    *   `libavcodec-dev`, `libavformat-dev`, `libswscale-dev`, `libv4l-dev`
    *   `libgtk-3-dev`
    *   `libatlas-base-dev`, `gfortran`
    *   `libboost-python-dev`
    *   `wget`, `bzip2`