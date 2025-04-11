#!/usr/bin/env python3
"""
Test script for the Fusion 360 MCP Server.

This script tests the server by making HTTP requests to the API endpoints.
"""

import json
import os
import sys
import requests
from typing import Dict, Any, List

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Server URL
SERVER_URL = "http://127.0.0.1:8000"

def test_root():
    """Test the root endpoint."""
    response = requests.get(f"{SERVER_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Fusion 360 MCP Server is running"
    print("✅ Root endpoint test passed")

def test_list_tools():
    """Test the list_tools endpoint."""
    response = requests.get(f"{SERVER_URL}/tools")
    assert response.status_code == 200
    data = response.json()
    assert "tools" in data
    assert len(data["tools"]) > 0
    print(f"✅ List tools test passed ({len(data['tools'])} tools found)")

def test_call_tool():
    """Test the call_tool endpoint."""
    # Test CreateSketch
    request_data = {
        "tool_name": "CreateSketch",
        "parameters": {
            "plane": "xy"
        }
    }
    response = requests.post(f"{SERVER_URL}/call_tool", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "script" in data
    assert "message" in data
    assert "CreateSketch" in data["script"]
    print("✅ Call tool (CreateSketch) test passed")
    
    # Test DrawRectangle
    request_data = {
        "tool_name": "DrawRectangle",
        "parameters": {
            "width": 10,
            "depth": 10
        }
    }
    response = requests.post(f"{SERVER_URL}/call_tool", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "script" in data
    assert "message" in data
    assert "DrawRectangle" in data["script"]
    print("✅ Call tool (DrawRectangle) test passed")
    
    # Test Extrude
    request_data = {
        "tool_name": "Extrude",
        "parameters": {
            "height": 5
        }
    }
    response = requests.post(f"{SERVER_URL}/call_tool", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "script" in data
    assert "message" in data
    assert "Extrude" in data["script"]
    print("✅ Call tool (Extrude) test passed")

def test_call_tools():
    """Test the call_tools endpoint."""
    request_data = {
        "tool_calls": [
            {
                "tool_name": "CreateSketch",
                "parameters": {
                    "plane": "xy"
                }
            },
            {
                "tool_name": "DrawRectangle",
                "parameters": {
                    "width": 10,
                    "depth": 10
                }
            },
            {
                "tool_name": "Extrude",
                "parameters": {
                    "height": 5
                }
            }
        ]
    }
    response = requests.post(f"{SERVER_URL}/call_tools", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "script" in data
    assert "message" in data
    assert "CreateSketch" in data["script"]
    assert "DrawRectangle" in data["script"]
    assert "Extrude" in data["script"]
    print("✅ Call tools test passed")

def run_tests():
    """Run all tests."""
    print("🧪 Running tests for Fusion 360 MCP Server...")
    try:
        test_root()
        test_list_tools()
        test_call_tool()
        test_call_tools()
        print("✅ All tests passed!")
    except requests.exceptions.ConnectionError:
        print("❌ Failed to connect to the server. Make sure the server is running.")
        print(f"   Server URL: {SERVER_URL}")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    run_tests()
