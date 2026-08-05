#!/bin/bash
################################################################################
# orchestrator.sh - Main Bash orchestration script
# CS 3030 - Project 7: Final Capstone
#
# TODO: Replace this header with a description of what YOUR tool does.
#
# Usage:
#   ./orchestrator.sh [--config <file>] [--dry-run] [--verbose]
#
# Exit Codes:
#   0 - Success
#   1 - General error
#   2 - Configuration error
#   3 - Dependency error
################################################################################

set -euo pipefail

# ------------------------------------------------------------------------------
# Global constants — update paths to match your project layout
# ------------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly SCRIPT_NAME
readonly LOG_DIR="${SCRIPT_DIR}/../logs"
readonly LOG_FILE="${LOG_DIR}/${SCRIPT_NAME%.sh}.log"
readonly DEFAULT_CONFIG="${SCRIPT_DIR}/../config.yaml"

# Color codes
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'

readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

# Runtime flags (set by parse_args)
CONFIG_FILE="$DEFAULT_CONFIG"
DRY_RUN=false
VERBOSE=false

# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------

# Initialize the log directory and file
init_logging() {
    mkdir -p "$LOG_DIR" || {
        echo "ERROR: Cannot create log directory: $LOG_DIR" >&2
        exit 1
    }
    touch "$LOG_FILE"
}

# log_info "message"  — write an INFO entry to the log file and stdout
log_info() {
    local message="$1"
    local timestamp
    timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "${timestamp} [INFO]  ${SCRIPT_NAME}: ${message}" | tee -a "$LOG_FILE"
}

# log_warn "message"  — write a WARN entry (yellow on console)
log_warn() {
    local message="$1"
    local timestamp
    timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "${timestamp} [WARN]  ${SCRIPT_NAME}: ${message}" | tee -a "$LOG_FILE"
    echo -e "${YELLOW}WARN: ${message}${NC}" >&2
}

# log_error "message"  — write an ERROR entry (red on console) and to stderr
log_error() {
    local message="$1"
    local timestamp
    timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "${timestamp} [ERROR] ${SCRIPT_NAME}: ${message}" | tee -a "$LOG_FILE" >&2
    echo -e "${RED}ERROR: ${message}${NC}" >&2
}

# log_success "message"  — write a success confirmation (green on console)
log_success() {
    local message="$1"
    local timestamp
    timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "${timestamp} [INFO]  ${SCRIPT_NAME}: ${message}" | tee -a "$LOG_FILE"
    echo -e "${GREEN}✓ ${message}${NC}"
}

# log_debug "message"  — only prints when --verbose is set (blue on console)
log_debug() {
    local message="$1"
    local timestamp

    if [[ "$VERBOSE" == true ]]; then
        timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
        echo "${timestamp} [DEBUG] ${SCRIPT_NAME}: ${message}" | tee -a "$LOG_FILE"
        echo -e "${BLUE}DEBUG: ${message}${NC}" >&2
    fi
}

# ------------------------------------------------------------------------------
# Dependency and environment checks
# ------------------------------------------------------------------------------

# check_dependencies — verify required external commands are available
# Args: space-separated list of command names
# Returns: 0 if all present, exits with code 3 if any are missing
check_dependencies() {
    local deps=("$@")
    local missing=()

    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &>/dev/null; then
            missing+=("$dep")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "Missing required dependencies: ${missing[*]}"
        log_error "Install them and try again."
        exit 3
    fi

    log_info "All dependencies present: ${deps[*]}"
}

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

# load_config — validate that the config file exists and is readable
# TODO: Expand this function to actually parse your config (YAML, JSON, or env vars)
load_config() {
    local config_file="$1"

    if [[ ! -f "$config_file" ]]; then
        log_error "Config file not found: $config_file"
        exit 2
    fi

    if [[ ! -r "$config_file" ]]; then
        log_error "Config file is not readable: $config_file"
        exit 2
    fi

    log_info "Loaded configuration from: $config_file"

    # TODO: Parse config values into variables. Example for a YAML key:
    #   MY_SETTING=$(grep '^my_setting:' "$config_file" | awk '{print $2}')
}

# ------------------------------------------------------------------------------
# Core logic — replace these stubs with your actual tool's functionality
# ------------------------------------------------------------------------------

# run_step_one — TODO: replace with your first major operation
# Args: none
# Returns: 0 on success, 1 on failure
run_step_one() {
    log_info "Starting step one..."

    # TODO: Implement your first major operation here.
    #
    # Tips:
    #   - Use 'local' for all variables inside functions
    #   - Return 1 (don't exit) on non-fatal errors so the caller can decide
    #   - Write meaningful log messages at each stage
    #
    # Example pattern:
    #   local input_dir="$1"
    #   if [[ ! -d "$input_dir" ]]; then
    #       log_error "Input directory does not exist: $input_dir"
    #       return 1
    #   fi

    if [[ "$DRY_RUN" == true ]]; then
        log_info "[DRY RUN] Would execute step one — skipping."
        return 0
    fi

    # YOUR CODE HERE

    log_success "Step one complete."
}

# run_step_two — TODO: replace with your second major operation
# Args: none
# Returns: 0 on success, 1 on failure
run_step_two() {
    log_info "Starting step two..."

    if [[ "$DRY_RUN" == true ]]; then
        log_info "[DRY RUN] Would execute step two — skipping."
        return 0
    fi

    # YOUR CODE HERE

    log_success "Step two complete."
}

# call_python — invoke the Python processor component
# Args: $1 = path to Python script, remaining args passed through
# Returns: Python script's exit code
call_python() {
    local python_script="$1"
    shift
    local python_args=("$@")

    if [[ ! -f "$python_script" ]]; then
        log_error "Python script not found: $python_script"
        return 1
    fi

    log_info "Calling Python processor: $python_script ${python_args[*]:-}"

    # TODO: Adjust the python_script path and arguments to match your project.
    python3 "$python_script" "${python_args[@]}"
}

# ------------------------------------------------------------------------------
# Argument parsing
# ------------------------------------------------------------------------------

usage() {
    cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS]

TODO: Replace this description with what your tool actually does.

Options:
  -c, --config <file>   Path to config file (default: $DEFAULT_CONFIG)
  -n, --dry-run         Show what would be done without making changes
  -v, --verbose         Enable verbose output
  -h, --help            Show this help message

Examples:
  $SCRIPT_NAME
  $SCRIPT_NAME --config custom.yaml --dry-run
  $SCRIPT_NAME --verbose
EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -c|--config)
                CONFIG_FILE="$2"
                shift 2
                ;;
            -n|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
}

# ------------------------------------------------------------------------------
# Main entry point
# ------------------------------------------------------------------------------

main() {
    parse_args "$@"
    init_logging

    log_info "=== ${SCRIPT_NAME} starting ==="
    [[ "$DRY_RUN" == true ]] && log_warn "Dry-run mode enabled — no changes will be made."

    # TODO: Update this list with the tools your script actually needs.
    check_dependencies python3

    load_config "$CONFIG_FILE"

    # TODO: Call your functions in the correct order.
    run_step_one
    run_step_two

    # TODO: Uncomment and update once your Python processor is ready.
    # call_python "${SCRIPT_DIR}/processor.py" --input "$INPUT_PATH"

    log_success "=== ${SCRIPT_NAME} finished successfully ==="
}

main "$@"
