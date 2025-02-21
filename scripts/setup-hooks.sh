#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HOOKS_DIR="$SCRIPT_DIR/../.git/hooks"
REPO_HOOKS_DIR="$SCRIPT_DIR/../.git/hooks"

# Create hooks directory if it doesn't exist
mkdir -p "$HOOKS_DIR"

echo -e "${CYAN}Setting up git hooks...${NC}"

# Copy pre-push hook
cp "$REPO_HOOKS_DIR/pre-push" "$HOOKS_DIR/pre-push"
chmod +x "$HOOKS_DIR/pre-push"

echo -e "${GREEN}Git hooks installed successfully!${NC}"
echo -e "${CYAN}The following hooks are now active:${NC}"
echo "- pre-push (runs tests before pushing)"