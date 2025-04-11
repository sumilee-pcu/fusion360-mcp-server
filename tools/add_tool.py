#!/usr/bin/env python3
"""
Tool Registry Manager for Fusion 360 MCP Server.

This script helps users add new tools to the tool registry.
"""

import json
import os
import sys
import argparse
from pathlib import Path

def get_tool_registry_path(server_path=None):
    """
    Get the path to the tool registry file.
    
    Args:
        server_path: Path to the Fusion 360 MCP Server directory.
        
    Returns:
        The path to the tool registry file.
    """
    if server_path is None:
        server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    return os.path.join(server_path, "src", "tool_registry.json")

def load_tool_registry(registry_path=None):
    """
    Load the tool registry.
    
    Args:
        registry_path: Path to the tool registry file.
        
    Returns:
        The tool registry as a list of dictionaries.
    """
    if registry_path is None:
        registry_path = get_tool_registry_path()
    
    with open(registry_path, "r") as f:
        return json.load(f)

def save_tool_registry(registry, registry_path=None):
    """
    Save the tool registry.
    
    Args:
        registry: The tool registry as a list of dictionaries.
        registry_path: Path to the tool registry file.
    """
    if registry_path is None:
        registry_path = get_tool_registry_path()
    
    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)

def add_tool(name, description, parameters, docs, registry_path=None):
    """
    Add a new tool to the registry.
    
    Args:
        name: The name of the tool.
        description: A description of what the tool does.
        parameters: A dictionary of parameters for the tool.
        docs: A link to documentation for the tool.
        registry_path: Path to the tool registry file.
        
    Returns:
        True if the tool was added successfully, False otherwise.
    """
    # Load the registry
    registry = load_tool_registry(registry_path)
    
    # Check if the tool already exists
    for tool in registry:
        if tool["name"] == name:
            print(f"❌ Tool already exists: {name}")
            return False
    
    # Add the new tool
    registry.append({
        "name": name,
        "description": description,
        "parameters": parameters,
        "docs": docs
    })
    
    # Save the registry
    save_tool_registry(registry, registry_path)
    
    print(f"✅ Tool added: {name}")
    return True

def add_tool_interactive(registry_path=None):
    """
    Add a new tool to the registry interactively.
    
    Args:
        registry_path: Path to the tool registry file.
        
    Returns:
        True if the tool was added successfully, False otherwise.
    """
    print("Adding a new tool to the registry...")
    
    # Get the tool name
    name = input("Tool name: ")
    if not name:
        print("❌ Tool name is required")
        return False
    
    # Get the tool description
    description = input("Tool description: ")
    if not description:
        print("❌ Tool description is required")
        return False
    
    # Get the tool parameters
    parameters = {}
    print("Tool parameters (leave name blank to finish):")
    while True:
        param_name = input("  Parameter name: ")
        if not param_name:
            break
        
        param_type = input("  Parameter type (string, number, integer, boolean, array): ")
        if not param_type:
            print("❌ Parameter type is required")
            continue
        
        param_description = input("  Parameter description: ")
        if not param_description:
            print("❌ Parameter description is required")
            continue
        
        param_default = input("  Parameter default value (leave blank for required): ")
        
        parameters[param_name] = {
            "type": param_type,
            "description": param_description
        }
        
        if param_default:
            # Convert the default value to the appropriate type
            if param_type == "number":
                try:
                    param_default = float(param_default)
                except ValueError:
                    print("❌ Invalid number")
                    continue
            elif param_type == "integer":
                try:
                    param_default = int(param_default)
                except ValueError:
                    print("❌ Invalid integer")
                    continue
            elif param_type == "boolean":
                param_default = param_default.lower() in ("true", "yes", "y", "1")
            elif param_type == "array":
                try:
                    param_default = json.loads(param_default)
                except json.JSONDecodeError:
                    print("❌ Invalid JSON array")
                    continue
            
            parameters[param_name]["default"] = param_default
    
    # Get the tool documentation
    docs = input("Tool documentation URL: ")
    if not docs:
        print("❌ Tool documentation URL is required")
        return False
    
    # Add the tool
    return add_tool(name, description, parameters, docs, registry_path)

def add_tool_from_json(json_file, registry_path=None):
    """
    Add a new tool to the registry from a JSON file.
    
    Args:
        json_file: Path to the JSON file containing the tool definition.
        registry_path: Path to the tool registry file.
        
    Returns:
        True if the tool was added successfully, False otherwise.
    """
    # Load the JSON file
    with open(json_file, "r") as f:
        tool = json.load(f)
    
    # Check if the tool has the required fields
    if "name" not in tool:
        print("❌ Tool name is required")
        return False
    
    if "description" not in tool:
        print("❌ Tool description is required")
        return False
    
    if "parameters" not in tool:
        print("❌ Tool parameters are required")
        return False
    
    if "docs" not in tool:
        print("❌ Tool documentation URL is required")
        return False
    
    # Add the tool
    return add_tool(tool["name"], tool["description"], tool["parameters"], tool["docs"], registry_path)

def list_tools(registry_path=None):
    """
    List all tools in the registry.
    
    Args:
        registry_path: Path to the tool registry file.
    """
    # Load the registry
    registry = load_tool_registry(registry_path)
    
    # Print the tools
    print(f"Tools in registry ({len(registry)}):")
    for tool in registry:
        print(f"  - {tool['name']}: {tool['description']}")
        print(f"    Parameters:")
        for name, param in tool["parameters"].items():
            required = "required" if "default" not in param else "optional"
            default = f", default: {param.get('default')}" if "default" in param else ""
            print(f"      - {name} ({param['type']}, {required}{default}): {param['description']}")
        print(f"    Documentation: {tool['docs']}")
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool Registry Manager for Fusion 360 MCP Server.")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List tools command
    list_parser = subparsers.add_parser("list", help="List all tools in the registry")
    list_parser.add_argument("--registry", help="Path to the tool registry file")
    
    # Add tool command
    add_parser = subparsers.add_parser("add", help="Add a new tool to the registry")
    add_parser.add_argument("--name", help="Name of the tool")
    add_parser.add_argument("--description", help="Description of what the tool does")
    add_parser.add_argument("--parameters", help="JSON string of parameters for the tool")
    add_parser.add_argument("--docs", help="Link to documentation for the tool")
    add_parser.add_argument("--registry", help="Path to the tool registry file")
    
    # Add tool from JSON command
    add_json_parser = subparsers.add_parser("add-json", help="Add a new tool to the registry from a JSON file")
    add_json_parser.add_argument("json_file", help="Path to the JSON file containing the tool definition")
    add_json_parser.add_argument("--registry", help="Path to the tool registry file")
    
    # Add tool interactively command
    add_interactive_parser = subparsers.add_parser("add-interactive", help="Add a new tool to the registry interactively")
    add_interactive_parser.add_argument("--registry", help="Path to the tool registry file")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_tools(args.registry)
    elif args.command == "add":
        if not args.name or not args.description or not args.parameters or not args.docs:
            print("❌ All arguments are required")
            exit(1)
        
        try:
            parameters = json.loads(args.parameters)
        except json.JSONDecodeError:
            print("❌ Invalid JSON parameters")
            exit(1)
        
        add_tool(args.name, args.description, parameters, args.docs, args.registry)
    elif args.command == "add-json":
        add_tool_from_json(args.json_file, args.registry)
    elif args.command == "add-interactive":
        add_tool_interactive(args.registry)
    else:
        parser.print_help()
