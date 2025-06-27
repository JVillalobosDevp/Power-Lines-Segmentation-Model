#!/bin/bash
set -e
start_time=$(date +%s)
# Base directories
BASE_DIR="."
SCRIPTS_DIR="${BASE_DIR}/utils"
MAIN_SCRIPT="${BASE_DIR}/evaluate.py"

# Data paths
LOCAL_DATA_DIR="${BASE_DIR}/data"
#LOCAL_DATA_DIR="${BASE_DIR}/data/*.las"
LOCAL_OUTPUT_DIR="${BASE_DIR}/data/output"

# Preprocessing scripts (run in order)
SCRIPT_1="${SCRIPTS_DIR}/Normalize_offset.py"
SCRIPT_2="${SCRIPTS_DIR}/process_las.py"
SCRIPT_3="${SCRIPTS_DIR}/txt_to_las.py"

# Logging
LOG_FILE="${BASE_DIR}/logs/pipeline_$(date +%Y%m%d_%H%M%S).log"

# Logging function
log_message() {
    echo "INFO - $(date '+%Y-%m-%d %H:%M:%S') - $1 " | tee -a "$LOG_FILE"
}

LOG_DIR="$(dirname "$LOG_FILE")"
if [ -d "$LOG_DIR" ]; then
    log_message "The folder $(dirname "$LOG_FILE") already exists."
else
    mkdir "$LOG_DIR"
    log_message "The folder $(dirname "$LOG_FILE") has been created."
fi

if [ -d "$LOCAL_OUTPUT_DIR" ]; then
    log_message "The folder "$LOCAL_OUTPUT_DIR" already exists."
else
    mkdir "$LOCAL_OUTPUT_DIR"
    log_message "The folder "$LOCAL_OUTPUT_DIR" has been created."
fi


# Run python script with error handling
run_python_script() {
    local script_path="$1"
    local script_args="$2"
    local script_name=$(basename "$script_path" .py)
    
    log_message "Starting: $script_name"
    log_message "Command: python3 $script_path $script_args"
    
    if python3 "$script_path" $script_args; then
        log_message "Completed: $script_name"
    else
        log_message "Failed: $script_name"
        exit 1
    fi
}

main() {
    log_message "Running wire inference pipeline..."
    log_message "Base directory: $BASE_DIR"

    # Run preprocessing scripts in sequence
    log_message "=== STARTING PREPROCESSING PHASE ==="

    # Data normalization
    run_python_script "${SCRIPT_1}" "--input_file $LOCAL_DATA_DIR/*.LAZ --output_file ${BASE_DIR}/data/normalized_cloud.las"
        
    # Process LAS files
    run_python_script "${SCRIPT_2}" "--input_file ${BASE_DIR}/data/normalized_cloud.las --output_dir ${BASE_DIR}/data/preprocessed_clss" 

    log_message "=== PREPROCESSING COMPLETED ==="
    
    # Run main inference
    log_message "=== STARTING INFERENCE PHASE ==="
    run_python_script "$MAIN_SCRIPT" "--evaluate"
    log_message "=== INFERENCE COMPLETED ==="

    run_python_script "${SCRIPT_3}" "--input_file ${BASE_DIR}/data/output/segmented_file.txt --output_las ${BASE_DIR}/data/output/segmented_file.las"

    
    # Cleanup temporary files (optional)
    if [ -d "${BASE_DIR}/data/preprocessed_clss" ]; then
        log_message "Cleaning up temporary files..."
        rm -rf "${BASE_DIR}/data/preprocessed_clss"
    fi
    rm -rf "${BASE_DIR}/data/outdir"
    
    if [ -d "${BASE_DIR}/data/normalized_cloud.las" ]; then
        rm -rf "${BASE_DIR}/data/normalized_cloud.las"
    fi    

    if [ -d "${BASE_DIR}/runs/shapenet.pvcnn.c0p5" ]; then
        rm -rf "${BASE_DIR}/runs/shapenet.pvcnn.c0p5/segmented_outputs"
    fi   

    log_message "=== PIPELINE COMPLETED SUCCESSFULLY ==="
    log_message "Results saved to: $LOCAL_OUTPUT_DIR"
    log_message "Log file: $LOG_FILE"
}

# Run main function
main "$@"