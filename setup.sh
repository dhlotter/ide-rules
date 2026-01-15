#!/bin/bash

# ============================================================================
# IDE Rules Setup Script
# ============================================================================
# Downloads and installs IDE rules from the central repository to your project.
#
# Usage:
#   Via curl (remote):
#     curl -sSL https://raw.githubusercontent.com/dhlotter/ide-rules/main/setup.sh | bash
#
#   Or clone and run locally:
#     ./setup.sh
#
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Configuration
REPO_URL="https://github.com/dhlotter/ide-rules"
REPO_RAW="https://raw.githubusercontent.com/dhlotter/ide-rules/main"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" 2>/dev/null)" && pwd 2>/dev/null || pwd)"
TEMP_DIR=""

# ===========================================================================
# Helper Functions
# ===========================================================================

print_header() {
    echo "" >&2
    echo -e "${BOLD}${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}" >&2
    echo -e "${BOLD}${CYAN}║                    IDE Rules Setup Script                      ║${NC}" >&2
    echo -e "${BOLD}${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}" >&2
    echo "" >&2
}

print_step() {
    echo -e "${BLUE}▶${NC} $1" >&2
}

print_success() {
    echo -e "${GREEN}✓${NC} $1" >&2
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1" >&2
}

print_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

print_file() {
    echo -e "  ${CYAN}↳${NC} $1" >&2
}

cleanup() {
    if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}

trap cleanup EXIT

# ===========================================================================
# Source Detection
# ===========================================================================

detect_source() {
    # Check if we're running from within the ide-rules repo itself
    if [ -d "$SCRIPT_DIR/.agent/rules" ] && [ -d "$SCRIPT_DIR/.agent/workflows" ] && [ -f "$SCRIPT_DIR/setup.sh" ]; then
        echo "local_agent"
        return
    fi

    echo "remote"
}

# ===========================================================================
# Copy Functions
# ===========================================================================

copy_rules() {
    local source_dir="$1"
    local target_dir="$2"
    local target_name="$3"
    local count=0
    
    mkdir -p "$target_dir"
    
    if [ -d "$source_dir" ]; then
        # Copy files recursively
        find "$source_dir" -type f -name "*.md" | while read -r file; do
            local rel_path="${file#$source_dir/}"
            local dest_file="$target_dir/$rel_path"
            local dest_dir="$(dirname "$dest_file")"
            
            mkdir -p "$dest_dir"
            cp "$file" "$dest_file"
            print_file "$rel_path → $target_name"
        done
        
        count=$(find "$source_dir" -type f -name "*.md" | wc -l | tr -d ' ')
    fi
    
    echo "$count"
}

copy_workflows() {
    local source_dir="$1"
    local target_dir="$2"
    local target_name="$3"
    local count=0
    
    mkdir -p "$target_dir"
    
    if [ -d "$source_dir" ]; then
        for file in "$source_dir"/*.md; do
            [ -e "$file" ] || continue
            local filename="$(basename "$file")"
            cp "$file" "$target_dir/$filename"
            print_file "$filename → $target_name"
            ((count++)) || true
        done
    fi
    
    echo "$count"
}

# ===========================================================================
# Setup Functions for Each IDE
# ===========================================================================

setup_antigravity() {
    local source_rules="$1"
    local source_workflows="$2"
    local target_root="$3"
    
    echo "" >&2
    print_step "Setting up ${BOLD}Antigravity${NC} (.agent/)"
    
    local rules_dir="$target_root/.agent/rules"
    local workflows_dir="$target_root/.agent/workflows"
    
    # Clear existing directories to ensure a clean sync
    rm -rf "$rules_dir" "$workflows_dir"
    mkdir -p "$rules_dir" "$workflows_dir"
    
    # Copy rules (with nested structure)
    if [ -d "$source_rules" ]; then
        cp -R "$source_rules"/* "$rules_dir/" 2>/dev/null || true
        local rule_count=$(find "$rules_dir" -type f -name "*.md" | wc -l | tr -d ' ')
        print_success "Copied $rule_count rule files"
    fi
    
    # Copy workflows
    if [ -d "$source_workflows" ]; then
        cp -R "$source_workflows"/* "$workflows_dir/" 2>/dev/null || true
        local workflow_count=$(find "$workflows_dir" -type f -name "*.md" | wc -l | tr -d ' ')
        print_success "Copied $workflow_count workflow files"
    fi
}

setup_claude() {
    local source_rules="$1"
    local source_workflows="$2"
    local target_root="$3"
    
    echo "" >&2
    print_step "Setting up ${BOLD}Claude${NC} (.claude/)"
    
    local claude_root="$target_root/.claude"
    local rules_dir="$claude_root/rules"
    local commands_dir="$claude_root/commands"
    local agent_rules="$target_root/.agent/rules"
    local agent_workflows="$target_root/.agent/workflows"

    # Clear existing directories to ensure a clean sync
    rm -rf "$rules_dir" "$commands_dir"
    mkdir -p "$claude_root"

    if [ -d "$agent_rules" ] && [ -d "$agent_workflows" ]; then
        ln -s "../.agent/rules" "$rules_dir"
        ln -s "../.agent/workflows" "$commands_dir"
        print_success "Linked .claude/ to .agent/ for rules and commands"
    else
        mkdir -p "$rules_dir" "$commands_dir"

        # Copy rules (with nested structure)
        if [ -d "$source_rules" ]; then
            cp -R "$source_rules"/* "$rules_dir/" 2>/dev/null || true
            local rule_count=$(find "$rules_dir" -type f -name "*.md" | wc -l | tr -d ' ')
            print_success "Copied $rule_count rule files"
        fi

        # Copy workflows as commands
        if [ -d "$source_workflows" ]; then
            cp -R "$source_workflows"/* "$commands_dir/" 2>/dev/null || true
            local command_count=$(find "$commands_dir" -type f -name "*.md" | wc -l | tr -d ' ')
            print_success "Copied $command_count command files"
        fi
    fi

    # Note about Cursor compatibility
    print_warning "Note: Cursor also reads rules from .claude/ and the .cursorrules file"
}



# ===========================================================================
# Download from Remote
# ===========================================================================

download_from_github() {
    local target_dir="$1"
    
    print_step "Downloading latest rules from GitHub..."
    
    TEMP_DIR=$(mktemp -d)
    
    # Check if gh CLI is available
    if command -v gh &> /dev/null; then
        print_step "Using GitHub CLI..."
        if gh repo clone dhlotter/ide-rules "$TEMP_DIR/rules_repo" --depth 1 &>/dev/null; then
            if [ -d "$TEMP_DIR/rules_repo" ]; then
                print_success "Cloned repository successfully"
                echo "$TEMP_DIR/rules_repo"
                return 0
            else
                print_warning "Clone succeeded but directory not found"
            fi
        else
            print_warning "GitHub CLI clone failed, trying git..."
        fi
    fi
    
    # Fall back to git
    if command -v git &> /dev/null; then
        print_step "Using git..."
        if git clone --depth 1 "$REPO_URL.git" "$TEMP_DIR/rules_repo" &>/dev/null; then
            if [ -d "$TEMP_DIR/rules_repo" ]; then
                print_success "Cloned repository successfully"
                echo "$TEMP_DIR/rules_repo"
                return 0
            else
                print_error "Git clone succeeded but directory not found"
                exit 1
            fi
        else
            print_warning "Git clone failed, falling back to curl..."
        fi
    fi
    
    # Fall back to curl for individual files
    print_warning "Git not available, downloading files individually..."
    mkdir -p "$TEMP_DIR/rules/reference" "$TEMP_DIR/workflows"
    
    # Download rules
    curl -sSL "$REPO_RAW/rules/king.md" -o "$TEMP_DIR/rules/king.md" 2>/dev/null || true
    
    # Download reference rules
    for ref in api-standards security tech-stack ui-components workflow; do
        curl -sSL "$REPO_RAW/rules/reference/${ref}.md" -o "$TEMP_DIR/rules/reference/${ref}.md" 2>/dev/null || true
    done
    
    # Download workflows
    for wf in design featurebase git-commit git-deploy troubleshoot; do
        curl -sSL "$REPO_RAW/workflows/${wf}.md" -o "$TEMP_DIR/workflows/${wf}.md" 2>/dev/null || true
    done
    
    echo "$TEMP_DIR"
}

# ===========================================================================
# Main Menu
# ===========================================================================



# ===========================================================================
# Main Execution
# ===========================================================================

main() {
    print_header
    
    # Determine target directory (where to install rules)
    local target_root="${1:-$(pwd)}"
    
    # Resolve to absolute path
    target_root="$(cd "$target_root" 2>/dev/null && pwd)"
    
    echo -e "Target project: ${BOLD}$target_root${NC}" >&2
    
    # Detect source
    local source_type=$(detect_source)
    local source_dir=""
    
    case "$source_type" in
        local_agent)
            print_success "Running from local repository (.agent/ source)"
            source_dir="$SCRIPT_DIR"
            ;;
        remote)
            source_dir=$(download_from_github "$target_root")
            ;;
    esac
    
    # Verify source directories exist
    local rules_src="$source_dir/.agent/rules"
    local workflows_src="$source_dir/.agent/workflows"
    
    if [ ! -d "$rules_src" ]; then
        print_error "Rules directory not found: $rules_src"
        exit 1
    fi
    
    if [ ! -d "$workflows_src" ]; then
        print_error "Workflows directory not found: $workflows_src"
        exit 1
    fi
    
    echo "" >&2
    print_success "Found $(find "$rules_src" -type f -name "*.md" | wc -l | tr -d ' ') rule files"
    print_success "Found $(ls -1 "$workflows_src"/*.md 2>/dev/null | wc -l | tr -d ' ') workflow files"
    
    # Clear old .cursor directory if it exists (consolidating to .claude)
    if [ -d "$target_root/.cursor" ]; then
        rm -rf "$target_root/.cursor"
        print_warning "Removed legacy .cursor directory (consolidated to .claude)"
    fi

    # Default to installing for all IDEs
    setup_antigravity "$rules_src" "$workflows_src" "$target_root"
    setup_claude "$rules_src" "$workflows_src" "$target_root"
    
    echo "" >&2
    echo -e "${GREEN}${BOLD}════════════════════════════════════════════════════════════════${NC}" >&2
    echo -e "${GREEN}${BOLD}                    Setup Complete! 🎉                          ${NC}" >&2
    echo -e "${GREEN}${BOLD}════════════════════════════════════════════════════════════════${NC}" >&2
    echo "" >&2
    echo -e "Rules have been copied to: ${BOLD}$target_root${NC}" >&2
    echo "" >&2
    echo -e "${YELLOW}Tip:${NC} To update rules in the future, run this script again." >&2
    echo -e "     Fixes should be made in the main repository:" >&2
    echo -e "     ${CYAN}$REPO_URL${NC}" >&2
    echo "" >&2
}

# Run main with optional target directory argument
main "$@"
