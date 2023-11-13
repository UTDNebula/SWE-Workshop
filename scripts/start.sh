#!/bin/bash

# This script starts the text generation inference service

# Change to the directory where the project is located

WORKSPACE_DIR=/workspace
CLONE_DIR="$WORKSPACE_DIR/text-generation-inference"


# Activate the environments

source "$HOME/.cargo/env"
source "$WORKSPACE_DIR/venv/bin/activate"

# Start falcon LLM

cd "$CLONE_DIR" || exit

make run-falcon-7b-instruct