#!/bin/bash

# This script is used to initialize the environment for the project in runpod

WORKSPACE_DIR=/workspace

cd "$WORKSPACE_DIR" || exit

apt update
apt install -y pkg-config libssl-dev gcc unzip

# Install Rust

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
source "$HOME/.cargo/env"

# Create virtual environment

python3 -m venv "$WORKSPACE_DIR/venv"
source venv/bin/activate

# Install protobuf

PROTOC_ZIP=protoc-21.12-linux-x86_64.zip
curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v21.12/$PROTOC_ZIP
unzip -o $PROTOC_ZIP -d /usr/local bin/protoc
unzip -o $PROTOC_ZIP -d /usr/local 'include/*'
rm -f $PROTOC_ZIP

# Clone and install text-generation-inference
CLONE_DIR="$WORKSPACE_DIR/text-generation-inference"
git clone https://github.com/huggingface/text-generation-inference.git "$CLONE_DIR"

cd "$CLONE_DIR" || exit
BUILD_EXTENSIONS=True make install