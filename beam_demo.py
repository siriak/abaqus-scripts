# Add working directory to path so that custom modules can be imported from there
import optimizations
import materials
from abaqusConstants import *
from abaqus import *
import sys
sys.path.append('D:\\Abaqus\\abaqus-scripts')


VIEWPORT_NAME = 'Viewport: 1'
MODEL_NAME = 'Model-1'
SKETCH_NAME = 'BeamSketch'
PART_NAME = 'BeamPart'
MATERIAL_NAME = 'Steel'
SECTION_NAME = 'BeamSection'
INSTANCE_NAME = 'BeamInstance'
LOAD_STEP_NAME = 'Load'
INITIAL_STEP_NAME = 'Initial'
BOUNDARY_CONDITION_NAME = 'BCFixedSide'
PRESSURE_NAME = 'Pressure'
JOB_NAME_BASE = 'BeamJob'


def createSketch(model, sketchName):
    # Create a sketch for the base feature.
    mySketch = model.ConstrainedSketch(name=sketchName, sheetSize=250.)

    # Create the rectangle.
    mySketch.rectangle(point1=(-100, 10), point2=(100, -10))

    return mySketch


def createPart(model, sketch, partName):
    # Create a three-dimensional, deformable part.
    myPart = model.Part(
        name=partName, dimensionality=THREE_D, type=DEFORMABLE_BODY)

    # Create the part's base feature by extruding the sketch through a distance of 25.0.
    myPart.BaseSolidExtrude(sketch=sketch, depth=25.0)

    return myPart


def createBottomUpExtrudedMesh(part):
    import regionToolset
    # Set mesh controls.
    pickedRegions = part.cells.getSequenceFromMask(mask=('[#1 ]', ), )
    part.setMeshControls(regions=pickedRegions, technique=BOTTOM_UP)

    # Mesh top side.
    part.seedPart(size=5.0, deviationFactor=0.1, minSizeFactor=0.1)
    pickedRegions = part.faces.getSequenceFromMask(mask=('[#8 ]', ), )
    part.generateMesh(regions=pickedRegions, boundaryPreview=ON)

    # Extrude mesh.
    faces = part.faces.getSequenceFromMask(mask=('[#8 ]', ), )
    pickedGeomSourceSide = regionToolset.Region(faces=faces)
    v = part.vertices
    vector = (v[0], v[1])
    return part.generateBottomUpExtrudedMesh(cell=part.cells[0], geometrySourceSide=pickedGeomSourceSide, extrudeVector=vector, numberOfLayers=4)


def createSection(model, part, materialName, sectionName):
    # Create the solid section.
    mySection = model.HomogeneousSolidSection(
        name=sectionName, material=materialName, thickness=1.0)

    # Assign the section to the region. The region refers to the single cell in this model.
    region = (part.cells,)
    part.SectionAssignment(region=region, sectionName=sectionName)

    return mySection


def createSets(part):
    nodes = part.nodes.getSequenceFromMask(mask=('[#1 #200 #40000 #8000000 #0 #10 #2000',
                                                 ' #400000 #80000000 #0 #100 #20000 #4000000 #0',
                                                 ' #8 #1000 #200000 #40000000 #0 #80 #10000',
                                                 ' #2000000 #0 #4 #800 #100000 #20000000 #0',
                                                 ' #40 #8000 #1000000 #0 #2 #400 #80000', ' #10000000 #0 #20 ]', ), )
    part.Set(nodes=nodes, name='SetBCFixedSide')

    nodes = part.nodes.getSequenceFromMask(mask=('[#ffffffff:7 #3fffff ]', ), )
    part.Set(nodes=nodes, name='SetLoadPressure')


def createInstance(assembly, part, instanceName):
    # Create a part instance.
    return assembly.Instance(name=instanceName, part=part, dependent=ON)


def createLoadStep(model, loadStepName, previousStepName):
    # Create a step. The time period of the static step is 1.0,
    # and the initial incrementation is 0.1; the step is created
    # after the initial step.
    return model.StaticStep(name=loadStepName, previous=previousStepName, timePeriod=1.0, initialInc=0.1)


def createEncastreBoundaryCondition(instance, model, createStepName, boundaryConditionName):
    region = instance.sets['SetBCFixedSide']
    return model.EncastreBC(name=boundaryConditionName,
                            createStepName=createStepName, region=region)


def createPressure(model, instance, createStepName, pressureName):
    # Find the top face using coordinates.
    topFaceCenter = (0, 10, 12.5)
    topFace = instance.faces.findAt((topFaceCenter,))

    # Create a pressure load on the top face of the beam.
    topSurface = ((topFace, SIDE1), )
    return model.Pressure(name=pressureName, createStepName=createStepName, region=topSurface, magnitude=0.5)


model = mdb.models[mdb.models.keys()[0]]
sketch = createSketch(model, SKETCH_NAME)
part = createPart(model, sketch, PART_NAME)
materials.add_all(model)
mesh = createBottomUpExtrudedMesh(part)
section = createSection(model, part, MATERIAL_NAME, SECTION_NAME)
createSets(part)
assembly = model.rootAssembly
instance = createInstance(assembly, part, INSTANCE_NAME)
loadStep = createLoadStep(model, LOAD_STEP_NAME, INITIAL_STEP_NAME)
encastreBoundaryCondition = createEncastreBoundaryCondition(
    instance, model, INITIAL_STEP_NAME, BOUNDARY_CONDITION_NAME)
pressure = createPressure(model, instance, LOAD_STEP_NAME, PRESSURE_NAME)

optimizations.optimize_topology(
    session, part, MODEL_NAME, LOAD_STEP_NAME, 1.25, 2.5)
