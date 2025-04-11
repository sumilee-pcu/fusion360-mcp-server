"""
Script template for the LoftProfiles tool.

This file demonstrates how to add a new script template to the script_generator.py file.
To use this template, add it to the SCRIPT_TEMPLATES dictionary in script_generator.py
and add parameter processing logic to the _process_parameters function.
"""

# Template for the LoftProfiles tool
LOFT_PROFILES_TEMPLATE = """
# Loft profiles
profiles = []
{profile_collection_code}
lofts = component.features.loftFeatures
loftInput = lofts.createInput(adsk.fusion.FeatureOperations.{operation_code}FeatureOperation)
loftInput.loftSections.addProfiles(profiles)
{closed_code}
loft = lofts.add(loftInput)
"""

# Example of how to add this template to the SCRIPT_TEMPLATES dictionary in script_generator.py:
"""
SCRIPT_TEMPLATES = {
    # ... existing templates ...
    
    "LoftProfiles": LOFT_PROFILES_TEMPLATE,
    
    # ... other templates ...
}
"""

# Example of how to add parameter processing logic to the _process_parameters function in script_generator.py:
"""
def _process_parameters(tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    # ... existing parameter processing ...
    
    elif tool_name == "LoftProfiles":
        # Process profile_indices
        profile_indices = processed.get("profile_indices", [])
        if not profile_indices:
            raise ValueError("profile_indices is required and must not be empty")
        
        # Generate code to collect profiles
        profile_code_lines = []
        for idx in profile_indices:
            profile_code_lines.append(f"prof = sketch.profiles.item({idx})")
            profile_code_lines.append("profiles.append(prof)")
        processed["profile_collection_code"] = "\\n".join(profile_code_lines)
        
        # Process operation
        operation = processed.get("operation", "new").lower()
        if operation == "new":
            processed["operation_code"] = "NewBodyFeatureOperation"
        elif operation == "join":
            processed["operation_code"] = "JoinFeatureOperation"
        elif operation == "cut":
            processed["operation_code"] = "CutFeatureOperation"
        elif operation == "intersect":
            processed["operation_code"] = "IntersectFeatureOperation"
        else:
            raise ValueError(f"Invalid operation: {operation}. Must be one of: new, join, cut, intersect")
        
        # Process is_closed
        is_closed = processed.get("is_closed", False)
        if is_closed:
            processed["closed_code"] = "loftInput.isClosed = True"
        else:
            processed["closed_code"] = "# Not a closed loft"
    
    # ... other parameter processing ...
    
    return processed
"""

# Example usage of the LoftProfiles tool:
"""
{
  "tool_name": "LoftProfiles",
  "parameters": {
    "profile_indices": [0, 1, 2],
    "operation": "new",
    "is_closed": false
  }
}
"""

# This would generate a script like:
"""
# Loft profiles
profiles = []
prof = sketch.profiles.item(0)
profiles.append(prof)
prof = sketch.profiles.item(1)
profiles.append(prof)
prof = sketch.profiles.item(2)
profiles.append(prof)
lofts = component.features.loftFeatures
loftInput = lofts.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
loftInput.loftSections.addProfiles(profiles)
# Not a closed loft
loft = lofts.add(loftInput)
"""
