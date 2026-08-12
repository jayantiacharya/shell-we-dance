#!/bin/bash
################################################################################
# orchestrator.sh - Main Bash orchestration script
# CS 3030 - Project 7: Final Capstone
#
# Collects system health metrics — disk usage, CPU load, process count,
# log directory size, and Docker container status — and writes them to
# raw_metrics.json for the Python aggregator to process into health.json.
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

# Populated by load_config; used by collect_log_size and write_raw_metrics
LOG_DIRECTORY=""
RAW_METRICS_PATH=""

# load_config — validate the config file exists/readable, then parse the
# values orchestrator.sh actually needs out of it
# Args: $1 = path to config file
# Returns: 0 on success, exits 2 on missing/unreadable/invalid config
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

    LOG_DIRECTORY=$(grep '^log_directory:' "$config_file" | awk '{print $2}')
    RAW_METRICS_PATH=$(grep '^raw_metrics_path:' "$config_file" | awk -F'"' '{print $2}')

    if [[ -z "$LOG_DIRECTORY" ]]; then
        log_error "log_directory not set in $config_file"
        exit 2
    fi

    if [[ -z "$RAW_METRICS_PATH" ]]; then
        log_warn "raw_metrics_path not set — defaulting to raw_metrics.txt"
        RAW_METRICS_PATH="raw_metrics.txt"
    fi

    log_debug "Parsed config — log_directory: ${LOG_DIRECTORY}, raw_metrics_path: ${RAW_METRICS_PATH}"
}

# ------------------------------------------------------------------------------
# Core logic — replace these stubs with your actual tool's functionality
# ------------------------------------------------------------------------------

# collect_disk_usage — root filesystem usage as a percentage
# Args: none
# Returns: prints the disk usage percentage (e.g. "42")
collect_disk_usage() {
    local pct
    log_debug "Raw df output: $(df -P /)"
    pct=$(df -P / | awk 'NR==2 { for (i=1; i<=NF; i++) if ($i ~ /%$/) { gsub("%","",$i); print $i } }')
    echo "$pct"
}

# collect_cpu_load — 1-minute system load average
# Args: none
# Returns: prints the 1-minute load average (e.g. "0.85")
collect_cpu_load() {
    local load
    log_debug "Raw loadavg: $(cat /proc/loadavg)"
    load=$(awk '{print $1}' /proc/loadavg)
    echo "$load"
}

# collect_process_count — total number of running processes
# Args: none
# Returns: prints the process count (e.g. "187")
collect_process_count() {
    local count
    count=$(ps aux | wc -l)
    echo "$count"
}

# collect_log_size — size in KB of the configured log directory
# Args: none — reads LOG_DIRECTORY (set by load_config)
# Returns: prints the size in kilobytes (e.g. "1024"), or "0" if unavailable
collect_log_size() {
    local size
    size=$(du -sk "$LOG_DIRECTORY" 2>/dev/null | awk '{print $1}') || size=0
    echo "${size:-0}"
}


# collect_docker_available — whether Docker is installed and reachable
# Args: none
# Returns: prints "true" or "false"
collect_docker_available() {
    if docker info &>/dev/null; then
        echo "true"
    else
        echo "false"
    fi
}

# collect_docker_container_count — number of currently running containers
# Args: none
# Returns: prints a count, or "0" if Docker is unavailable
collect_docker_container_count() {
    local count
    if ! docker info &>/dev/null; then
        echo "0"
        return 0
    fi
    count=$(docker ps -q | wc -l)
    echo "$count"
}


# write_raw_metrics — collect all metrics and write them as key=value lines
# Args: none
# Returns: 0 on success
write_raw_metrics() {
    local output_file="${SCRIPT_DIR}/../${RAW_METRICS_PATH}"
    local disk cpu procs logsize docker_avail docker_count

    if [[ "$DRY_RUN" == true ]]; then
        log_info "[DRY RUN] Would write metrics to ${output_file} — skipping."
        return 0
    fi

    disk=$(collect_disk_usage)
    cpu=$(collect_cpu_load)
    procs=$(collect_process_count)
    logsize=$(collect_log_size)
    docker_avail=$(collect_docker_available)
    docker_count=$(collect_docker_container_count)

    log_info "Disk usage: ${disk}%"
    log_info "CPU load (1min): ${cpu}"
    log_info "Process count: ${procs}"
    log_info "Log directory size: ${logsize}KB"
    log_info "Docker available: ${docker_avail}, running containers: ${docker_count}"

    cat > "$output_file" <<EOF
disk_usage_percent=${disk}
cpu_load_1min=${cpu}
process_count=${procs}
log_size_kb=${logsize}
docker_available=${docker_avail}
docker_container_count=${docker_count}
EOF

    log_success "Wrote raw metrics to ${output_file}"
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

    # Adjust the python_script path and arguments to match your project.
    python3 "$python_script" "${python_args[@]}"
}

# ------------------------------------------------------------------------------
# Argument parsing
# ------------------------------------------------------------------------------

usage() {
    cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS]

Collects disk usage, CPU load, process count, log directory size, and
Docker container status. Writes results to raw_metrics.json.

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

    # Update this list with the tools your script actually needs.
    check_dependencies python3

    load_config "$CONFIG_FILE"

    # Call your functions in the correct order.
    write_raw_metrics

    # Uncomment and update once your Python processor is ready.
    # call_python "${SCRIPT_DIR}/processor.py" --input "${SCRIPT_DIR}/../raw_metrics.json" --output "${SCRIPT_DIR}/../health.json"

    log_success "=== ${SCRIPT_NAME} finished successfully ==="
}

main "$@"
