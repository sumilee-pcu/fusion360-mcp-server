#!/usr/bin/env python3
"""
Setup script for the Fusion 360 MCP Server.

This script helps users install the MCP server in their Cline configuration.
"""

import json
import os
import sys
import argparse
from pathlib import Path

def get_default_config_path():
    """Get the default path to the Cline MCP settings file."""
    if sys.platform == "win32":
        return os.path.expanduser("~/AppData/Roaming/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json")
    elif sys.platform == "darwin":
        return os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")
    else:
        return os.path.expanduser("~/.config/Claude/claude_desktop_config.json")

def setup_mcp_server(config_path=None, server_path=None):
    """
    Set up the Fusion 360 MCP Server in the Cline configuration.
    
    Args:
        config_path: Path to the Cline MCP settings file.
        server_path: Path to the Fusion 360 MCP Server directory.
    """
    # Get the config path
    if config_path is None:
        config_path = get_default_config_path()
    
    # Get the server path
    if server_path is None:
        server_path = os.path.abspath(os.path.dirname(__file__))
    
    # Check if the config file exists
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        print("Please make sure Cline is installed and has been run at least once.")
        return False
    
    # Load the config file
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print(f"❌ Failed to parse config file: {config_path}")
        return False
    
    # Check if the mcpServers key exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    # Add the Fusion 360 MCP Server
    main_script_path = os.path.join(server_path, "src", "main.py")
    
    # Use the appropriate command based on the platform
    if sys.platform == "win32":
        command = "python"
    else:
        command = "python3"
    
    config["mcpServers"]["fusion360"] = {
        "command": command,
        "args": [main_script_path, "--mcp"],
        "env": {},
        "disabled": False,
        "autoApprove": []
    }
    
    # Save the config file
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"❌ Failed to save config file: {e}")
        return False
    
    print(f"✅ Fusion 360 MCP Server added to Cline configuration: {config_path}")
    print("Please restart Cline to load the new MCP server.")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set up the Fusion 360 MCP Server in the Cline configuration.")
    parser.add_argument("--config", help="Path to the Cline MCP settings file.")
    parser.add_argument("--server", help="Path to the Fusion 360 MCP Server directory.")
    args = parser.parse_args()
    
    setup_mcp_server(args.config, args.server)
