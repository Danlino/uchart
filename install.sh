#!/usr/bin/env bash
set -euo pipefail

PROJECT_NAME="uchart.py"
CMD_NAME="uchart"
REPO="Danlino/uchart"
RELEASE_URL="https://raw.githubusercontent.com/${REPO}/main"

ARCH="$(uname -m)"

case "${ARCH}" in
    x86_64)  ARCH="amd64" ;;
    aarch64) ARCH="arm64" ;;
    armv7l)  ARCH="armhf" ;;
    i686)    ARCH="386" ;;
    *)       echo "Unsupported architecture: ${ARCH}" >&2; exit 1 ;;
esac

DOWNLOAD_URL="${RELEASE_URL}/${PROJECT_NAME}"

INSTALL_DIR="/usr/local/bin"
if [[ ! -w "$INSTALL_DIR" ]]; then
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
fi

if [[ "$INSTALL_DIR" == "$HOME/.local/bin" ]] && [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "Adding $INSTALL_DIR to PATH (current session only)"
    export PATH="$INSTALL_DIR:$PATH"
    echo
    echo "To make it permanent, run:"
    echo "   echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc   # or ~/.zshrc"
    echo
fi

echo "Downloading $DOWNLOAD_URL ..."
curl -L -# -o "$INSTALL_DIR/$CMD_NAME" "$DOWNLOAD_URL"

echo "Making it executable..."
chmod +x "$INSTALL_DIR/$CMD_NAME"

echo
echo "✓ $PROJECT_NAME successfully installed!"
echo "   Run it with: $CMD_NAME"
echo
echo "Test:"
$CMD_NAME -h 2>/dev/null || echo "   (no help output - that's fine)"