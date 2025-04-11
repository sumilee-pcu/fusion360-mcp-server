#!/usr/bin/env python3
"""
Example of how to use the Fusion 360 MCP Server HTTP API directly.

This script demonstrates how to make HTTP requests to the server to generate Fusion 360 scripts.
"""

import json
import requests
import argparse
import os

# Server URL
SERVER_URL = "http://127.0.0.1:8000"

def list_tools():
    """List all available tools."""
    response = requests.get(f"{SERVER_URL}/tools")
    if response.status_code == 200:
        data = response.json()
        print(f"Available tools ({len(data['tools'])}):")
        for tool in data["tools"]:
            print(f"  - {tool['name']}: {tool['description']}")
            print(f"    Parameters:")
            for name, param in tool["parameters"].items():
                required = "required" if "default" not in param else "optional"
                default = f", default: {param.get('default')}" if "default" in param else ""
                print(f"      - {name} ({param['type']}, {required}{default}): {param['description']}")
            print()
    else:
        print(f"Error: {response.status_code} - {response.text}")

def call_tool(tool_name, parameters, output_file=None):
    """
    Call a single tool and generate a Fusion 360 script.
    
    Args:
        tool_name: The name of the tool to call.
        parameters: A dictionary of parameters for the tool.
        output_file: The file to save the generated script to.
    """
    request_data = {
        "tool_name": tool_name,
        "parameters": parameters
    }
    
    response = requests.post(f"{SERVER_URL}/call_tool", json=request_data)
    
    if response.status_code == 200:
        data = response.json()
        script = data["script"]
        
        if output_file:
            with open(output_file, "w") as f:
                f.write(script)
            print(f"Script saved to {output_file}")
        else:
            print("Generated script:")
            print("=" * 80)
            print(script)
            print("=" * 80)
    else:
        print(f"Error: {response.status_code} - {response.text}")

def call_tools(tool_calls, output_file=None):
    """
    Call multiple tools in sequence and generate a Fusion 360 script.
    
    Args:
        tool_calls: A list of dictionaries, each containing 'tool_name' and 'parameters' keys.
        output_file: The file to save the generated script to.
    """
    request_data = {
        "tool_calls": tool_calls
    }
    
    response = requests.post(f"{SERVER_URL}/call_tools", json=request_data)
    
    if response.status_code == 200:
        data = response.json()
        script = data["script"]
        
        if output_file:
            with open(output_file, "w") as f:
                f.write(script)
            print(f"Script saved to {output_file}")
        else:
            print("Generated script:")
            print("=" * 80)
            print(script)
            print("=" * 80)
    else:
        print(f"Error: {response.status_code} - {response.text}")

def create_box_with_rounded_corners(width=10, depth=10, height=5, radius=0.5, output_file=None):
    """
    Create a box with rounded corners.
    
    Args:
        width: Width of the box in mm.
        depth: Depth of the box in mm.
        height: Height of the box in mm.
        radius: Radius of the fillets in mm.
        output_file: The file to save the generated script to.
    """
    tool_calls = [
        {
            "tool_name": "CreateSketch",
            "parameters": {
                "plane": "xy"
            }
        },
        {
            "tool_name": "DrawRectangle",
            "parameters": {
                "width": width,
                "depth": depth,
                "origin_x": 0,
                "origin_y": 0,
                "origin_z": 0
            }
        },
        {
            "tool_name": "Extrude",
            "parameters": {
                "profile_index": 0,
                "height": height,
                "operation": "new"
            }
        },
        {
            "tool_name": "Fillet",
            "parameters": {
                "body_index": 0,
                "radius": radius,
                "edge_indices": []
            }
        }
    ]
    
    call_tools(tool_calls, output_file)

def create_cylinder(radius=5, height=10, output_file=None):
    """
    Create a cylinder.
    
    Args:
        radius: Radius of the cylinder in mm.
        height: Height of the cylinder in mm.
        output_file: The file to save the generated script to.
    """
    tool_calls = [
        {
            "tool_name": "CreateSketch",
            "parameters": {
                "plane": "xy"
            }
        },
        {
            "tool_name": "DrawCircle",
            "parameters": {
                "center_x": 0,
                "center_y": 0,
                "center_z": 0,
                "radius": radius
            }
        },
        {
            "tool_name": "Extrude",
            "parameters": {
                "profile_index": 0,
                "height": height,
                "operation": "new"
            }
        }
    ]
    
    call_tools(tool_calls, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example of how to use the Fusion 360 MCP Server HTTP API.")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List tools command
    list_parser = subparsers.add_parser("list", help="List all available tools")
    
    # Call tool command
    call_parser = subparsers.add_parser("call", help="Call a single tool")
    call_parser.add_argument("tool_name", help="Name of the tool to call")
    call_parser.add_argument("--params", help="JSON string of parameters for the tool")
    call_parser.add_argument("--output", help="File to save the generated script to")
    
    # Create box command
    box_parser = subparsers.add_parser("box", help="Create a box with rounded corners")
    box_parser.add_argument("--width", type=float, default=10, help="Width of the box in mm")
    box_parser.add_argument("--depth", type=float, default=10, help="Depth of the box in mm")
    box_parser.add_argument("--height", type=float, default=5, help="Height of the box in mm")
    box_parser.add_argument("--radius", type=float, default=0.5, help="Radius of the fillets in mm")
    box_parser.add_argument("--output", help="File to save the generated script to")
    
    # Create cylinder command
    cylinder_parser = subparsers.add_parser("cylinder", help="Create a cylinder")
    cylinder_parser.add_argument("--radius", type=float, default=5, help="Radius of the cylinder in mm")
    cylinder_parser.add_argument("--height", type=float, default=10, help="Height of the cylinder in mm")
    cylinder_parser.add_argument("--output", help="File to save the generated script to")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_tools()
    elif args.command == "call":
        parameters = {}
        if args.params:
            try:
                parameters = json.loads(args.params)
            except json.JSONDecodeError:
                print("Error: Invalid JSON parameters")
                exit(1)
        call_tool(args.tool_name, parameters, args.output)
    elif args.command == "box":
        create_box_with_rounded_corners(args.width, args.depth, args.height, args.radius, args.output)
    elif args.command == "cylinder":
        create_cylinder(args.radius, args.height, args.output)
    else:
        parser.print_help()
