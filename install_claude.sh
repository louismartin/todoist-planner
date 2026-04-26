#!/bin/bash

set -e

echo "=================================================="
echo "  Claude Code + Vertex AI + Mistral Vibe Setup"
echo "=================================================="
echo ""

# Step 1: Install Claude Code
echo "[1/5] Installing Claude Code..."
curl -fsSL https://claude.ai/install.sh | bash
echo "Claude Code installed successfully!"
echo ""

# Step 2: Install Google Cloud CLI
echo "[2/5] Installing Google Cloud CLI..."

GCLOUD_INSTALL_DIR="$HOME"
GCLOUD_ARCHIVE="google-cloud-cli-linux-x86_64.tar.gz"

# Check if gcloud is already installed
if command -v gcloud &> /dev/null; then
    echo "Google Cloud CLI is already installed."
else
    cd "$GCLOUD_INSTALL_DIR"

    # Download Google Cloud CLI
    echo "Downloading Google Cloud CLI..."
    curl -O "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/$GCLOUD_ARCHIVE"

    # Extract the archive
    echo "Extracting Google Cloud CLI..."
    tar -xf "$GCLOUD_ARCHIVE"

    # Run the install script (non-interactive)
    echo "Running Google Cloud CLI installer..."
    ./google-cloud-sdk/install.sh --quiet --path-update true --command-completion true

    # Clean up the archive
    rm -f "$GCLOUD_ARCHIVE"

    echo "Google Cloud CLI installed successfully!"
fi

# Source the gcloud path for current session
if [ -f "$HOME/google-cloud-sdk/path.bash.inc" ]; then
    source "$HOME/google-cloud-sdk/path.bash.inc"
fi

echo ""

# Step 3: Authenticate with Google Cloud
echo "[3/5] Authenticating with Google Cloud..."
echo "Please complete the authentication in your browser when prompted."
echo ""

gcloud auth application-default login --project code-model-vertex

echo ""
echo "Authentication complete!"
echo ""

# Step 4: Add Claude Code environment variables to bashrc
echo "[4/5] Adding Claude Code environment variables to ~/.bashrc..."

BASHRC="$HOME/.bashrc"

# Define the environment variables to add
ENV_VARS='
# Claude Code Vertex AI Configuration
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=code-model-vertex
export ANTHROPIC_MODEL='\''claude-opus-4-5@20251101'\''
export ANTHROPIC_SMALL_FAST_MODEL='\''claude-haiku-4-5@20251001'\''
'

# Check if the variables are already in bashrc
if grep -q "CLAUDE_CODE_USE_VERTEX" "$BASHRC" 2>/dev/null; then
    echo "Environment variables already exist in ~/.bashrc. Skipping..."
else
    echo "$ENV_VARS" >> "$BASHRC"
    echo "Environment variables added to ~/.bashrc"
fi

# Source bashrc for current session
source "$BASHRC"

echo ""

# Step 5: Install Mistral Vibe
echo "[5/5] Installing Mistral Vibe..."
curl -LsSf https://mistral.ai/vibe/install.sh | bash
echo "Mistral Vibe installed successfully!"
echo ""

echo "=================================================="
echo "  Installation Complete!"
echo "=================================================="
echo ""
echo "The following environment variables have been set:"
echo "  CLAUDE_CODE_USE_VERTEX=1"
echo "  CLOUD_ML_REGION=global"
echo "  ANTHROPIC_VERTEX_PROJECT_ID=code-model-vertex"
echo "  ANTHROPIC_MODEL=claude-opus-4-5@20251101"
echo "  ANTHROPIC_SMALL_FAST_MODEL=claude-haiku-4-5@20251001"
echo ""
echo "Please restart your terminal or run:"
echo "  source ~/.bashrc"
echo ""
echo "Then you can start using:"
echo "  claude      - Claude Code with Vertex AI"
echo "  vibe        - Mistral Vibe"
echo ""

