#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_NAME="fms_env"
PYTHON_SCRIPT_NAME="FMS-Demo-v1.py" # Make sure this matches your Python script name

# Check if virtual environment exists
if [ ! -d "${SCRIPT_DIR}/${VENV_NAME}" ]; then
    echo "[ERROR] Virtual environment '${VENV_NAME}' not found in ${SCRIPT_DIR}."
    echo "Please run 'setup_fms_project.sh' first."
    exit 1
fi

# Check if Python script exists
if [ ! -f "${SCRIPT_DIR}/${PYTHON_SCRIPT_NAME}" ]; then
    echo "[ERROR] Python script '${PYTHON_SCRIPT_NAME}' not found in ${SCRIPT_DIR}."
    exit 1
fi

echo "[INFO] Activating virtual environment: ${SCRIPT_DIR}/${VENV_NAME}"
source "${SCRIPT_DIR}/${VENV_NAME}/bin/activate"

echo "[INFO] Running FMS Demo: ${PYTHON_SCRIPT_NAME}"
echo "Press Ctrl+C in the terminal or 'q' or 'ESC' in the OpenCV window to quit."

# Execute the Python script, passing along any arguments given to this shell script
# e.g., ./run_fms_demo.sh --webcam 1
python3 "${SCRIPT_DIR}/${PYTHON_SCRIPT_NAME}" "$@"

echo "[INFO] FMS Demo finished. Deactivating virtual environment."
deactivate