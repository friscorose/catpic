#!/usr/bin/env bash
set -e

# Test all language implementations by reading their test-config.toml files
# This script discovers and runs tests for each language implementation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
EXIT_CODE=0

# Color output for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Parse TOML (simple parser for our needs)
parse_toml() {
    local file=$1
    local section=$2
    local key=$3
    
    # Extract value from TOML file
    # This is a simple parser - for production, consider using a proper TOML parser
    awk -v section="$section" -v key="$key" '
        /^\[.*\]/ { current_section = substr($0, 2, length($0)-2) }
        current_section == section && $0 ~ "^" key " *= *" {
            sub("^" key " *= *", "")
            gsub(/^"/, "")
            gsub(/"$/, "")
            print
        }
    ' "$file"
}

# Test a single language implementation
test_implementation() {
    local lang_dir=$1
    local lang_name=$(basename "$lang_dir")
    local config_file="$lang_dir/test-config.toml"
    
    log_info "Testing $lang_name implementation..."
    
    if [ ! -f "$config_file" ]; then
        log_warning "No test-config.toml found for $lang_name, skipping"
        return 0
    fi
    
    cd "$lang_dir"
    
    # Parse configuration
    local build_cmd=$(parse_toml "$config_file" "build" "command")
    local test_cmd=$(parse_toml "$config_file" "test" "command")
    local compliance_cmd=$(parse_toml "$config_file" "compliance" "command")
    local working_dir=$(parse_toml "$config_file" "test" "working_dir")
    local expected_exit=$(parse_toml "$config_file" "compliance" "expected_exit")
    
    # Default values
    [ -z "$working_dir" ] && working_dir="."
    [ -z "$expected_exit" ] && expected_exit="0"
    
    # Change to working directory if specified
    if [ "$working_dir" != "." ]; then
        cd "$working_dir"
    fi
    
    # Build step (if specified)
    if [ -n "$build_cmd" ]; then
        log_info "  Building $lang_name..."
        if eval "$build_cmd"; then
            log_success "  Build successful"
        else
            log_error "  Build failed for $lang_name"
            return 1
        fi
    fi
    
    # Run tests
    if [ -n "$test_cmd" ]; then
        log_info "  Running $lang_name tests..."
        if eval "$test_cmd"; then
            log_success "  Tests passed"
        else
            log_error "  Tests failed for $lang_name"
            return 1
        fi
    fi
    
    # Run compliance tests
    if [ -n "$compliance_cmd" ]; then
        log_info "  Running $lang_name compliance tests..."
        eval "$compliance_cmd"
        local actual_exit=$?
        
        if [ "$actual_exit" -eq "$expected_exit" ]; then
            log_success "  Compliance tests passed"
        else
            log_error "  Compliance tests failed for $lang_name (exit code: $actual_exit, expected: $expected_exit)"
            return 1
        fi
    fi
    
    log_success "$lang_name: All tests passed!"
    return 0
}

# Main execution
main() {
    log_info "Starting test suite for all implementations..."
    echo ""
    
    cd "$PROJECT_ROOT"
    
    # Find all language directories (those containing test-config.toml)
    local implementations=()
    for dir in */; do
        # Skip non-implementation directories
        if [[ "$dir" == "docs/" ]] || [[ "$dir" == "spec/" ]] || \
           [[ "$dir" == "scripts/" ]] || [[ "$dir" == ".github/" ]] || \
           [[ "$dir" == "benchmarks/" ]]; then
            continue
        fi
        
        if [ -f "${dir}test-config.toml" ]; then
            implementations+=("${dir%/}")
        fi
    done
    
    if [ ${#implementations[@]} -eq 0 ]; then
        log_error "No implementations found with test-config.toml"
        exit 1
    fi
    
    log_info "Found ${#implementations[@]} implementation(s): ${implementations[*]}"
    echo ""
    
    # Test each implementation
    local failed_implementations=()
    for impl in "${implementations[@]}"; do
        if ! test_implementation "$PROJECT_ROOT/$impl"; then
            failed_implementations+=("$impl")
            EXIT_CODE=1
        fi
        echo ""
    done
    
    # Summary
    echo "========================================"
    if [ ${#failed_implementations[@]} -eq 0 ]; then
        log_success "All implementations passed testing!"
    else
        log_error "Failed implementations: ${failed_implementations[*]}"
        exit $EXIT_CODE
    fi
}

main "$@"
