import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        
        # Get the active component in the design
        component = design.rootComponent
        
        # Create a new sketch on the xy plane
        sketches = component.sketches
        xyPlane = component.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        
        
        # Draw a rectangle
        rectangle = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(0 + 10, 0 + 10, 0)
        )
        
        
        # Extrude the profile
        prof = sketch.profiles.item(0)
        extrudes = component.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(5)
        extInput.setDistanceExtent(False, distance)
        extrude = extrudes.add(extInput)
        
        
        # Fillet edges
        fillets = component.features.filletFeatures
        edgeCollection = adsk.core.ObjectCollection.create()
        body = component.bRepBodies.item(0)
        for edge in body.edges:
            edgeCollection.add(edge)
        filletInput = fillets.createInput()
        filletInput.addConstantRadiusEdgeSet(edgeCollection, adsk.core.ValueInput.createByReal(0.5), True)
        fillet = fillets.add(filletInput)
        
        ui.messageBox('Operation completed successfully')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
