#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

PROJECT_DIR=$(pwd) # Assumes script is run from the project directory
VENV_NAME="fms_env"
SHAPE_PREDICTOR_URL="http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
SHAPE_PREDICTOR_BZ2="shape_predictor_68_face_landmarks.dat.bz2"
SHAPE_PREDICTOR_DAT="shape_predictor_68_face_landmarks.dat"

echo "--- FMS Project Setup Script ---"
echo "Project directory: ${PROJECT_DIR}"
echo "Virtual environment will be: ${PROJECT_DIR}/${VENV_NAME}"
echo ""

# --------------------------------------------------------------------------
# 1. Install System Dependencies
# --------------------------------------------------------------------------
echo "[INFO] Updating package lists..."
sudo apt-get update

echo "[INFO] Installing system dependencies for OpenCV and dlib..."
# General build tools
sudo apt-get install -y build-essential cmake pkg-config
# Image I/O libraries
sudo apt-get install -y libjpeg-dev libpng-dev libtiff-dev
# Video I/O libraries
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
# GUI library (GTK for OpenCV windows)
sudo apt-get install -y libgtk-3-dev
# Optimization libraries (for NumPy, SciPy, OpenCV)
sudo apt-get install -y libatlas-base-dev gfortran
# dlib specific dependency
sudo apt-get install -y libboost-python-dev
# For downloading and decompressing the model
sudo apt-get install -y wget bzip2

# --------------------------------------------------------------------------
# 2. Install Python pip and venv
# --------------------------------------------------------------------------
echo "[INFO] Installing Python3 pip and venv..."
sudo apt-get install -y python3-pip python3-venv

# --------------------------------------------------------------------------
# 3. Create Python Virtual Environment
# --------------------------------------------------------------------------
if [ -d "${PROJECT_DIR}/${VENV_NAME}" ]; then
    echo "[INFO] Virtual environment '${VENV_NAME}' already exists. Skipping creation."
else
    echo "[INFO] Creating Python virtual environment named '${VENV_NAME}'..."
    python3 -m venv "${PROJECT_DIR}/${VENV_NAME}"
    echo "[INFO] Virtual environment created."
fi

# --------------------------------------------------------------------------
# 4. Install Python Libraries into Virtual Environment
# --------------------------------------------------------------------------
echo "[INFO] Activating virtual environment to install packages..."
# Note: We explicitly call the pip from the venv to ensure packages are installed there.
# This is more robust within a script than relying on 'source' and subsequent commands
# if the script is complex or sourced itself.

echo "[INFO] Upgrading pip in the virtual environment..."
"${PROJECT_DIR}/${VENV_NAME}/bin/pip" install --upgrade pip

echo "[INFO] Installing Python libraries..."
"${PROJECT_DIR}/${VENV_NAME}/bin/pip" install numpy scipy imutils dlib opencv-python

# --------------------------------------------------------------------------
# 5. Download and Extract dlib's Facial Landmark Predictor
# --------------------------------------------------------------------------
if [ -f "${PROJECT_DIR}/${SHAPE_PREDICTOR_DAT}" ]; then
    echo "[INFO] '${SHAPE_PREDICTOR_DAT}' already exists. Skipping download."
else
    echo "[INFO] Downloading ${SHAPE_PREDICTOR_DAT}..."
    wget -O "${PROJECT_DIR}/${SHAPE_PREDICTOR_BZ2}" "${SHAPE_PREDICTOR_URL}"
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to download ${SHAPE_PREDICTOR_BZ2}. Please check the URL or your internet connection."
        exit 1
    fi

    echo "[INFO] Decompressing ${SHAPE_PREDICTOR_BZ2}..."
    bzip2 -d "${PROJECT_DIR}/${SHAPE_PREDICTOR_BZ2}"
    if [ $? -ne 0 ] || [ ! -f "${PROJECT_DIR}/${SHAPE_PREDICTOR_DAT}" ]; then
        echo "[ERROR] Failed to decompress or find ${SHAPE_PREDICTOR_DAT}."
        echo "You might need to manually download from ${SHAPE_PREDICTOR_URL} and extract it to ${PROJECT_DIR}."
        # Attempt to clean up the bz2 file if decompression failed but file exists
        if [ -f "${PROJECT_DIR}/${SHAPE_PREDICTOR_BZ2}" ]; then
            rm "${PROJECT_DIR}/${SHAPE_PREDICTOR_BZ2}"
        fi
        exit 1
    fi
    echo "[INFO] '${SHAPE_PREDICTOR_DAT}' is ready."
fi

# --------------------------------------------------------------------------
# 6. Final Instructions
# --------------------------------------------------------------------------
echo ""
echo "[INFO] --- Setup Complete! ---"
echo ""
echo "What was done:"
echo "  - System dependencies installed."
echo "  - Python virtual environment '${VENV_NAME}' created/verified at ${PROJECT_DIR}/${VENV_NAME}"
echo "  - Required Python libraries (numpy, scipy, imutils, dlib, opencv-python) installed into the virtual environment."
echo "  - Facial landmark model '${SHAPE_PREDICTOR_DAT}' downloaded and placed in ${PROJECT_DIR}."
echo ""
echo "To run your FMS demo:"
echo "  1. Make 'run_fms_demo.sh' executable: chmod +x run_fms_demo.sh"
echo "  2. Execute: ./run_fms_demo.sh"
echo ""
echo "[INFO] Note: The first time 'dlib' is installed, compilation can take a VERY long time on Raspberry Pi. Be patient!"
echo "Subsequent runs of this setup script will be much faster if dependencies are already met."