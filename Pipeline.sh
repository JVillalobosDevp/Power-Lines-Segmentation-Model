#!/bin/bash
set -e
start_time=$(date +%s)
# Base directories
BASE_DIR="."
SCRIPTS_DIR="${BASE_DIR}/utils"
MAIN_SCRIPT="${BASE_DIR}/evaluate.py"

# Data paths
LOCAL_DATA_DIR="${BASE_DIR}/data"
# LOCAL_DATA_DIR="${BASE_DIR}/data/*.las"
LOCAL_OUTPUT_DIR="${BASE_DIR}/data/output"

# Preprocessing scripts (run in order)
SCRIPT_1="${SCRIPTS_DIR}/Normalize_offset.py"
SCRIPT_2="${SCRIPTS_DIR}/process_las.py"
SCRIPT_3="${SCRIPTS_DIR}/restCoord.py"

# Script arguments - easily configurable
# CLEANING_ARGS="--remove-nulls --normalize"
# FEATURE_ARGS="--create-embeddings --scale-features"
# VALIDATION_ARGS="--check-schema --validate-ranges"
# INFERENCE_ARGS="--model-path ${MODEL_PATH} --batch-size 32 --output-format json"

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
    
    # Data cleaning
    run_python_script "${SCRIPT_1}" "--input_file /home/binahlab/AI-Labs/clever-data/electrical-elements/data/inmel/GRANSABANA/processed/classify/aerial-math-classify/v2/vx-02/000006.las --output_file ${BASE_DIR}/data/normalized_cloud.las"
    
    # Feature engineering
    run_python_script "${SCRIPT_2}" "--input_file ${BASE_DIR}/data/normalized_cloud.las --output_dir ${BASE_DIR}/data/preprocessed_clss"
    
    # Data validation
    #run_python_script "${PREPROCESS_SCRIPTS[2]}" "--input ${BASE_DIR}/data/temp/features_data.csv $VALIDATION_ARGS"
    
    log_message "=== PREPROCESSING COMPLETED ==="
    
    # Run main inference
    log_message "=== STARTING INFERENCE PHASE ==="
    run_python_script "$MAIN_SCRIPT" "--evaluate"
    log_message "=== INFERENCE COMPLETED ==="
    
    # Cleanup temporary files (optional)
    if [ -d "${BASE_DIR}/data/preprocessed_clss" ]; then
        log_message "Cleaning up temporary files..."
        rm -rf "${BASE_DIR}/data/preprocessed_clss"
    fi
    rm -rf "${BASE_DIR}/data/outdir"
    

    log_message "=== PIPELINE COMPLETED SUCCESSFULLY ==="
    log_message "Results saved to: $LOCAL_OUTPUT_DIR"
    log_message "Log file: $LOG_FILE"
}

# Run main function
main "$@"