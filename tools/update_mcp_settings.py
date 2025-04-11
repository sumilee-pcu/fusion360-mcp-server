#!/usr/bin/env python3
"""
Update MCP Settings for Fusion 360 MCP Server.

This script updates the MCP settings configuration file with the Fusion 360 MCP Server.
"""

import json
import os
import sys
import argparse
from pathlib import Path

def get_default_config_path():
    """Get the default path to the MCP settings configuration file."""
    if sys.platform == "win32":
        return os.path.expanduser("~/AppData/Roaming/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json")
    elif sys.platform == "darwin":
        return os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")
    else:
        return os.path.expanduser("~/.config/Claude/claude_desktop_config.json")

def update_mcp_settings(config_path=None, server_path=None, server_name="fusion360", disabled=False):
    """
    Update the MCP settings configuration file with the Fusion 360 MCP Server.
    
    Args:
        config_path: Path to the MCP settings configuration file.
        server_path: Path to the Fusion 360 MCP Server directory.
        server_name: Name of the server in the MCP settings.
        disabled: Whether the server should be disabled by default.
        
    Returns:
        True if the settings were updated successfully, False otherwise.
    """
    # Get the config path
    if config_path is None:
        config_path = get_default_config_path()
    
    # Get the server path
    if server_path is None:
        server_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
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
    
    config["mcpServers"][server_name] = {
        "command": command,
        "args": [main_script_path, "--mcp"],
        "env": {},
        "disabled": disabled,
        "autoApprove": []
    }
    
    # Save the config file
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"❌ Failed to save config file: {e}")
        return False
    
    print(f"✅ Fusion 360 MCP Server added to MCP settings: {config_path}")
    print("Please restart Cline to load the new MCP server.")
    return True

def list_mcp_servers(config_path=None):
    """
    List all MCP servers in the configuration file.
    
    Args:
        config_path: Path to the MCP settings configuration file.
    """
    # Get the config path
    if config_path is None:
        config_path = get_default_config_path()
    
    # Check if the config file exists
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        print("Please make sure Cline is installed and has been run at least once.")
        return
    
    # Load the config file
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print(f"❌ Failed to parse config file: {config_path}")
        return
    
    # Check if the mcpServers key exists
    if "mcpServers" not in config:
        print("No MCP servers found in the configuration file.")
        return
    
    # Print the servers
    print(f"MCP servers in configuration file ({len(config['mcpServers'])}):")
    for name, server in config["mcpServers"].items():
        disabled = "disabled" if server.get("disabled", False) else "enabled"
        print(f"  - {name} ({disabled})")
        print(f"    Command: {server.get('command', 'N/A')}")
        print(f"    Args: {server.get('args', [])}")
        print(f"    Environment variables: {server.get('env', {})}")
        print(f"    Auto-approve: {server.get('autoApprove', [])}")
        print()

def remove_mcp_server(server_name, config_path=None):
    """
    Remove an MCP server from the configuration file.
    
    Args:
        server_name: Name of the server to remove.
        config_path: Path to the MCP settings configuration file.
        
    Returns:
        True if the server was removed successfully, False otherwise.
    """
    # Get the config path
    if config_path is None:
        config_path = get_default_config_path()
    
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
        print("No MCP servers found in the configuration file.")
        return False
    
    # Check if the server exists
    if server_name not in config["mcpServers"]:
        print(f"❌ Server not found: {server_name}")
        return False
    
    # Remove the server
    del config["mcpServers"][server_name]
    
    # Save the config file
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"❌ Failed to save config file: {e}")
        return False
    
    print(f"✅ Server removed: {server_name}")
    print("Please restart Cline to apply the changes.")
    return True

def enable_mcp_server(server_name, config_path=None):
    """
    Enable an MCP server in the configuration file.
    
    Args:
        server_name: Name of the server to enable.
        config_path: Path to the MCP settings configuration file.
        
    Returns:
        True if the server was enabled successfully, False otherwise.
    """
    # Get the config path
    if config_path is None:
        config_path = get_default_config_path()
    
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
        print("No MCP servers found in the configuration file.")
        return False
    
    # Check if the server exists
    if server_name not in config["mcpServers"]:
        print(f"❌ Server not found: {server_name}")
        return False
    
    # Enable the server
    config["mcpServers"][server_name]["disabled"] = False
    
    # Save the config file
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"❌ Failed to save config file: {e}")
        return False
    
    print(f"✅ Server enabled: {server_name}")
    print("Please restart Cline to apply the changes.")
    return True

def disable_mcp_server(server_name, config_path=None):
    """
    Disable an MCP server in the configuration file.
    
    Args:
        server_name: Name of the server to disable.
        config_path: Path to the MCP settings configuration file.
        
    Returns:
        True if the server was disabled successfully, False otherwise.
    """
    # Get the config path
    if config_path is None:
        config_path = get_default_config_path()
    
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
        print("No MCP servers found in the configuration file.")
        return False
    
    # Check if the server exists
    if server_name not in config["mcpServers"]:
        print(f"❌ Server not found: {server_name}")
        return False
    
    # Disable the server
    config["mcpServers"][server_name]["disabled"] = True
    
    # Save the config file
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"❌ Failed to save config file: {e}")
        return False
    
    print(f"✅ Server disabled: {server_name}")
    print("Please restart Cline to apply the changes.")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update MCP Settings for Fusion 360 MCP Server.")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update the MCP settings with the Fusion 360 MCP Server")
    update_parser.add_argument("--config", help="Path to the MCP settings configuration file")
    update_parser.add_argument("--server", help="Path to the Fusion 360 MCP Server directory")
    update_parser.add_argument("--name", default="fusion360", help="Name of the server in the MCP settings")
    update_parser.add_argument("--disabled", action="store_true", help="Disable the server by default")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all MCP servers in the configuration file")
    list_parser.add_argument("--config", help="Path to the MCP settings configuration file")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove an MCP server from the configuration file")
    remove_parser.add_argument("name", help="Name of the server to remove")
    remove_parser.add_argument("--config", help="Path to the MCP settings configuration file")
    
    # Enable command
    enable_parser = subparsers.add_parser("enable", help="Enable an MCP server in the configuration file")
    enable_parser.add_argument("name", help="Name of the server to enable")
    enable_parser.add_argument("--config", help="Path to the MCP settings configuration file")
    
    # Disable command
    disable_parser = subparsers.add_parser("disable", help="Disable an MCP server in the configuration file")
    disable_parser.add_argument("name", help="Name of the server to disable")
    disable_parser.add_argument("--config", help="Path to the MCP settings configuration file")
    
    args = parser.parse_args()
    
    if args.command == "update":
        update_mcp_settings(args.config, args.server, args.name, args.disabled)
    elif args.command == "list":
        list_mcp_servers(args.config)
    elif args.command == "remove":
        remove_mcp_server(args.name, args.config)
    elif args.command == "enable":
        enable_mcp_server(args.name, args.config)
    elif args.command == "disable":
        disable_mcp_server(args.name, args.config)
    else:
        parser.print_help()
