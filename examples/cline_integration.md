# Cline Integration Example

This document demonstrates how to use the Fusion 360 MCP Server with Cline.

## Setup

1. First, ensure the Fusion 360 MCP Server is added to your Cline MCP settings configuration file:

```json
{
  "mcpServers": {
    "fusion360": {
      "command": "python",
      "args": ["/path/to/fusion360-mcp-server/src/main.py", "--mcp"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

2. Restart Cline to load the new MCP server.

## Example Prompts

Here are some example prompts you can use with Cline to generate Fusion 360 scripts:

### Simple Box

```
Create a script to make a simple box in Fusion 360 with dimensions 10x10x5 mm.
```

### Box with Rounded Corners

```
Create a script to make a box with rounded corners in Fusion 360. The box should be 10x10x5 mm with a fillet radius of 0.5 mm on all edges.
```

### Cylinder

```
Create a script to make a cylinder in Fusion 360 with a radius of 5 mm and a height of 10 mm.
```

### Complex Shape

```
Create a script to make a complex shape in Fusion 360:
1. Start with a sketch on the XY plane
2. Draw a rectangle 20x10 mm
3. Draw a circle with radius 3 mm at the center of the rectangle
4. Extrude the profile (with the hole) to a height of 5 mm
5. Add a 1 mm fillet to all edges
```

## How It Works

1. Cline processes your natural language prompt.
2. Cline identifies the Fusion 360 operations needed.
3. Cline calls the appropriate tools on the Fusion 360 MCP Server.
4. The server generates a Python script.
5. Cline returns the script to you.
6. You can then run the script in Fusion 360.

## Running the Generated Script

To run the generated script in Fusion 360:

1. Copy the script to a file with a `.py` extension.
2. Open Fusion 360.
3. Click on the "Scripts and Add-Ins" button in the toolbar.
4. Click the "+" button to add a new script.
5. Select the file you created.
6. Click "Run".

## Advanced Usage

You can also create more complex designs by combining multiple tool calls. For example:

```
Create a script to make an assembly in Fusion 360:
1. Create a base plate (rectangle 50x30x5 mm)
2. Create a cylinder (radius 5 mm, height 10 mm) at position (10, 10, 5)
3. Create another cylinder (radius 5 mm, height 10 mm) at position (40, 10, 5)
4. Create a box (10x20x3 mm) at position (25, 15, 5)
```

Cline will break this down into multiple tool calls and generate a script that creates the entire assembly.
