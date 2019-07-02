# Add working directory to path so that custom modules can be imported from there
import sys
sys.path.append('D:\\Abaqus\\abaqus-scripts')
import optimizations
import regionToolset
import __main__
from abaqusConstants import *
from abaqus import *

execfile("D:/Abaqus/abaqus-scripts/materials.py", __main__.__dict__)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                            sheetSize=100.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
session.viewports['Viewport: 1'].view.setValues(nearPlane=68.6958,
                                                farPlane=119.866, width=309.399, height=120.645, cameraPosition=(35.37,
                                                                                                                 -5.47245, 94.2809), cameraTarget=(35.37, -5.47245, 0))
s.rectangle(point1=(-50.0, 50.0), point2=(50.0, -50.0))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D,
                               type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=100.0)
s.unsetPrimaryObject()

del mdb.models['Model-1'].sketches['__profile__']

mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1',
                                              material='Steel', thickness=None)
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(cells=cells)
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0,
                    offsetType=MIDDLE_SURFACE, offsetField='',
                    thicknessAssignment=FROM_SECTION)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
a.Instance(name='Part-1-1', part=p, dependent=ON)
p.seedPart(size=2.0, deviationFactor=0.1, minSizeFactor=0.1)
pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
p.generateMesh(regions=pickedRegions)
p.deleteMesh()
pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
p.setMeshControls(regions=pickedRegions, technique=BOTTOM_UP)
f = p.faces
pickedRegions = f.getSequenceFromMask(mask=('[#8 ]', ), )
p.generateMesh(regions=pickedRegions, boundaryPreview=ON)
mdb.meshEditOptions.setValues(enableUndo=True, maxUndoCacheElements=0.5)
faces = f.getSequenceFromMask(mask=('[#8 ]', ), )
pickedGeomSourceSide = regionToolset.Region(faces=faces)
v1 = p.vertices
v2 = p.vertices
vector = (v1[0], v2[1])
c1 = p.cells
p.generateBottomUpExtrudedMesh(cell=c1[0],
                               geometrySourceSide=pickedGeomSourceSide, extrudeVector=vector,
                               numberOfLayers=50)
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF,
                                                           adaptiveMeshConstraints=ON)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF)
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON,
                                                           predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
session.viewports['Viewport: 1'].view.setValues(nearPlane=247.454,
                                                farPlane=484.254, width=381.423, height=148.73, viewOffsetX=41.448,
                                                viewOffsetY=5.39056)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p1 = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF,
                                                           predefinedFields=OFF, connectors=OFF)
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON,
                                                           predefinedFields=ON, connectors=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=248.599,
                                                farPlane=483.108, width=338.585, height=132.026, viewOffsetX=18.5983,
                                                viewOffsetY=-3.14915)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF,
                                                           bcs=OFF, predefinedFields=OFF, connectors=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF, loads=ON,
                                                           bcs=ON, predefinedFields=ON, connectors=ON)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF,
                                                           predefinedFields=OFF, connectors=OFF)

session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,
                                                       engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF,
                                                       engineeringFeatures=OFF, mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
p.undoMeshEdit()
faces = f.getSequenceFromMask(mask=('[#8 ]', ), )
pickedGeomSourceSide = regionToolset.Region(faces=faces)
v1 = p.vertices
v2 = p.vertices
vector = (v1[0], v2[1])
p.generateBottomUpExtrudedMesh(geometrySourceSide=pickedGeomSourceSide,
                               extrudeVector=vector, numberOfLayers=50)
a.regenerate()
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON,
                                                           predefinedFields=ON, connectors=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=239.77,
                                                farPlane=491.938, width=473.365, height=184.582, viewOffsetX=46.8073,
                                                viewOffsetY=7.12677)
session.viewports['Viewport: 1'].view.setValues(nearPlane=279.237,
                                                farPlane=465.699, width=551.284, height=214.965, cameraPosition=(
                                                    20.5196, 371.965, 55.5363), cameraUpVector=(-0.691576, -0.308161,
                                                                                                -0.653269), cameraTarget=(6.49977, 6.38039, 56.1536),
                                                viewOffsetX=54.512, viewOffsetY=8.29987)
session.viewports['Viewport: 1'].view.setValues(nearPlane=251.494,
                                                farPlane=466.934, width=496.512, height=193.608, cameraPosition=(
                                                    10.5864, 348.442, 137.213), cameraUpVector=(-0.679689, -0.170684,
                                                                                                -0.713365), cameraTarget=(5.95705, -8.25771, 56.0182),
                                                viewOffsetX=49.0961, viewOffsetY=7.47525)
session.viewports['Viewport: 1'].view.setValues(nearPlane=257.022,
                                                farPlane=468.841, width=507.428, height=197.864, cameraPosition=(
                                                    27.2778, 353.707, 127.145), cameraUpVector=(-0.689486, -0.158979,
                                                                                                -0.706637), cameraTarget=(5.29045, -4.61321, 56.6337),
                                                viewOffsetX=50.1753, viewOffsetY=7.63957)
session.viewports['Viewport: 1'].view.setValues(nearPlane=254.785,
                                                farPlane=467.168, width=503.012, height=196.142, cameraPosition=(
                                                    27.2778, 351.711, 127.145), cameraTarget=(5.29045, -6.6093, 56.6337),
                                                viewOffsetX=49.7386, viewOffsetY=7.57308)
session.viewports['Viewport: 1'].view.setValues(nearPlane=245.426,
                                                farPlane=457.266, width=484.536, height=188.938, cameraPosition=(
                                                    27.2778, 341.878, 127.145), cameraTarget=(5.29045, -16.4423, 56.6337),
                                                viewOffsetX=47.9117, viewOffsetY=7.29491)
session.viewports['Viewport: 1'].view.setValues(nearPlane=262.889,
                                                farPlane=450.524, width=519.014, height=202.382, cameraPosition=(
                                                    6.78256, 356.46, 66.8764), cameraUpVector=(-0.679041, -0.321494,
                                                                                               -0.659958), cameraTarget=(6.8092, -9.33341, 60.2566),
                                                viewOffsetX=51.3208, viewOffsetY=7.81397)
session.viewports['Viewport: 1'].view.setValues(nearPlane=259.899,
                                                farPlane=452.805, width=513.111, height=200.08, cameraPosition=(
                                                    -26.777, 356.46, 18.1713), cameraUpVector=(0.00178814, -0.321494,
                                                                                               -0.94691), cameraTarget=(-22.0026, -9.33341, 13.5857),
                                                viewOffsetX=50.7371, viewOffsetY=7.72509)
session.viewports['Viewport: 1'].view.setValues(nearPlane=279.112,
                                                farPlane=433.593, width=278.992, height=108.789, viewOffsetX=38.7791,
                                                viewOffsetY=-29.858)
session.viewports['Viewport: 1'].view.setValues(nearPlane=260.996,
                                                farPlane=458.397, width=260.884, height=101.728, cameraPosition=(
                                                    4.22084, 287.954, 269.932), cameraUpVector=(0.00135245, 0.405623,
                                                                                                -0.914039), cameraTarget=(-21.5524, 23.0476, 18.916),
                                                viewOffsetX=36.2621, viewOffsetY=-27.92)
f1 = a.instances['Part-1-1'].elements
face1Elements1 = f1.getSequenceFromMask(mask=(
    '[#0:31 #f0000000 #7f #1ffc000 #0 #7ff #1ffc0000',
    ' #0 #7ff0 #ffc00000 #1 #7ff00 #fc000000 #1f',
    ' #7ff000 #c0000000 #1ff #7ff0000 #0 #1ffc ]', ), )
region = a.Surface(face1Elements=face1Elements1, name='Surf-1')
mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1',
                               region=region, distributionType=UNIFORM, field='', magnitude=100.0,
                               amplitude=UNSET)
session.viewports['Viewport: 1'].view.setValues(nearPlane=243.126,
                                                farPlane=476.266, width=458.893, height=178.938, viewOffsetX=69.5898,
                                                viewOffsetY=-31.9876)
session.viewports['Viewport: 1'].view.setValues(nearPlane=257.54,
                                                farPlane=497.838, width=486.097, height=189.546, cameraPosition=(
                                                    89.5081, 247.459, 327.957), cameraUpVector=(0.171122, 0.558747,
                                                                                                -0.811492), cameraTarget=(-3.93696, 59.315, 28.4268),
                                                viewOffsetX=73.7153, viewOffsetY=-33.884)
session.viewports['Viewport: 1'].view.setValues(nearPlane=201.546,
                                                farPlane=432.701, width=380.41, height=148.335, cameraPosition=(
                                                    -194.179, -160.871, 292.409), cameraUpVector=(-0.422677, -0.201754,
                                                                                                  -0.883538), cameraTarget=(59.0279, -142.229, 28.9948),
                                                viewOffsetX=57.6881, viewOffsetY=-26.517)
session.viewports['Viewport: 1'].view.setValues(nearPlane=262.136,
                                                farPlane=462.106, width=494.771, height=192.929, cameraPosition=(
                                                    39.633, -378.192, 53.7584), cameraUpVector=(-0.432658, 0.266735,
                                                                                                -0.861196), cameraTarget=(98.5962, -22.3124, -7.24517),
                                                viewOffsetX=75.0307, viewOffsetY=-34.4887)
session.viewports['Viewport: 1'].view.setValues(nearPlane=251.548,
                                                farPlane=463.109, width=474.787, height=185.136, cameraPosition=(
                                                    52.211, -378.192, 58.3305), cameraUpVector=(-0.0375652, 0.266735,
                                                                                                -0.963037), cameraTarget=(131.131, -22.3124, 27.1897),
                                                viewOffsetX=72.0001, viewOffsetY=-33.0956)
session.viewports['Viewport: 1'].view.setValues(nearPlane=263.535,
                                                farPlane=451.122, width=323.88, height=126.292, viewOffsetX=124.602,
                                                viewOffsetY=-0.759095)
session.viewports['Viewport: 1'].view.setValues(nearPlane=265.693,
                                                farPlane=449.445, width=326.533, height=127.327, cameraPosition=(
                                                    51.1789, -378.192, 64.093), cameraUpVector=(0.0269137, 0.266735,
                                                                                                -0.963394), cameraTarget=(132.005, -22.3124, 38.299),
                                                viewOffsetX=125.622, viewOffsetY=-0.765312)
session.viewports['Viewport: 1'].view.setValues(nearPlane=265.885,
                                                farPlane=449.74, width=326.769, height=127.419, cameraPosition=(
                                                    51.1789, -378.442, 64.093), cameraTarget=(132.005, -22.5624, 38.299),
                                                viewOffsetX=125.713, viewOffsetY=-0.765864)
session.viewports['Viewport: 1'].view.setValues(nearPlane=265.6,
                                                farPlane=449.504, width=326.42, height=127.282, cameraPosition=(
                                                    51.1789, -378.174, 64.093), cameraTarget=(132.005, -22.2947, 38.299),
                                                viewOffsetX=125.578, viewOffsetY=-0.765043)
session.viewports['Viewport: 1'].view.setValues(nearPlane=265.109,
                                                farPlane=448.963, width=325.816, height=127.047, cameraPosition=(
                                                    51.1789, -377.644, 64.093), cameraTarget=(132.005, -21.7643, 38.299),
                                                viewOffsetX=125.346, viewOffsetY=-0.763628)
session.viewports['Viewport: 1'].view.setValues(nearPlane=266.66,
                                                farPlane=448.394, width=327.722, height=127.79, cameraPosition=(
                                                    51.1789, -376.989, 16.8562), cameraUpVector=(0.0269137, 0.38255,
                                                                                                 -0.923543), cameraTarget=(132.005, -20.6262, 34.7777),
                                                viewOffsetX=126.079, viewOffsetY=-0.768095)
session.viewports['Viewport: 1'].view.setValues(nearPlane=264.203,
                                                farPlane=449.858, width=324.703, height=126.613, cameraPosition=(
                                                    55.8237, -376.989, 40.9805), cameraUpVector=(0.274604, 0.38255,
                                                                                                 -0.882184), cameraTarget=(128.839, -20.6262, 80.0043),
                                                viewOffsetX=124.917, viewOffsetY=-0.761019)
session.viewports['Viewport: 1'].view.setValues(nearPlane=270.471,
                                                farPlane=430.484, width=332.407, height=129.617, cameraPosition=(
                                                    121.258, -353.87, 80.3275), cameraUpVector=(0.204359, 0.326573,
                                                                                                -0.922815), cameraTarget=(131.226, 11.847, 79.8071),
                                                viewOffsetX=127.881, viewOffsetY=-0.779075)
session.viewports['Viewport: 1'].view.setValues(nearPlane=269.914,
                                                farPlane=431.046, width=331.722, height=129.35, cameraPosition=(
                                                    120.699, -353.87, 82.7593), cameraUpVector=(0.219054, 0.326573,
                                                                                                -0.919438), cameraTarget=(130.674, 11.847, 82.398),
                                                viewOffsetX=127.618, viewOffsetY=-0.77747)
session.viewports['Viewport: 1'].view.setValues(nearPlane=269.009,
                                                farPlane=429.267, width=330.609, height=128.916, cameraPosition=(
                                                    135.823, -347.131, 81.4224), cameraUpVector=(0.205524, 0.339606,
                                                                                                 -0.917838), cameraTarget=(130.02, 18.6745, 82.6064),
                                                viewOffsetX=127.19, viewOffsetY=-0.774863)
session.viewports['Viewport: 1'].view.setValues(nearPlane=269.025,
                                                farPlane=429.344, width=330.629, height=128.924, cameraPosition=(
                                                    139.39, -347.131, 43.3561), cameraUpVector=(-0.00449187, 0.339606,
                                                                                                -0.940557), cameraTarget=(133.997, 18.6745, 45.8053),
                                                viewOffsetX=127.198, viewOffsetY=-0.774909)
session.viewports['Viewport: 1'].view.setValues(nearPlane=269.005,
                                                farPlane=429.309, width=330.605, height=128.914, cameraPosition=(
                                                    137.491, -347.131, 43.3561), cameraTarget=(132.098, 18.6745, 45.8053),
                                                viewOffsetX=127.188, viewOffsetY=-0.774851)
session.viewports['Viewport: 1'].view.setValues(nearPlane=267.467,
                                                farPlane=427.766, width=328.715, height=128.178, cameraPosition=(
                                                    33.0022, -347.131, 43.3561), cameraTarget=(27.6092, 18.6745, 45.8053),
                                                viewOffsetX=126.461, viewOffsetY=-0.770422)
session.viewports['Viewport: 1'].view.setValues(nearPlane=293.735,
                                                farPlane=472.384, width=360.999, height=140.766, cameraPosition=(
                                                    -62.1765, -36.8537, -329.061), cameraUpVector=(0.27738, 0.920455,
                                                                                                   0.275361), cameraTarget=(23.9712, -36.6954, 26.5047),
                                                viewOffsetX=138.881, viewOffsetY=-0.846084)
session.viewports['Viewport: 1'].view.setValues(nearPlane=296.109,
                                                farPlane=470.009, width=285.29, height=111.245, viewOffsetX=63.1827,
                                                viewOffsetY=2.80361)
session.viewports['Viewport: 1'].view.setValues(nearPlane=295.823,
                                                farPlane=471.273, width=285.014, height=111.137, cameraPosition=(
                                                    -57.6074, -39.1069, -329.061), cameraUpVector=(0.0874118, 0.957359,
                                                                                                   0.275361), cameraTarget=(26.7631, -21.6982, 26.5047),
                                                viewOffsetX=63.1216, viewOffsetY=2.8009)
session.viewports['Viewport: 1'].view.setValues(nearPlane=295.741,
                                                farPlane=469.621, width=284.935, height=111.106, cameraPosition=(
                                                    -50.8428, -39.1069, -329.156), cameraUpVector=(0.0826404, 0.957359,
                                                                                                   0.27683), cameraTarget=(27.3707, -21.6982, 27.8149),
                                                viewOffsetX=63.104, viewOffsetY=2.80012)
session.viewports['Viewport: 1'].view.setValues(nearPlane=307.149,
                                                farPlane=458.212, width=181.736, height=70.8652, viewOffsetX=43.207,
                                                viewOffsetY=-18.0539)
session.viewports['Viewport: 1'].view.setValues(nearPlane=304.983,
                                                farPlane=459.962, width=180.454, height=70.3653, cameraPosition=(
                                                    -51.1494, -36.5219, -329.104), cameraUpVector=(0.0723343, 0.956099,
                                                                                                   0.283977), cameraTarget=(27.1229, -20.9412, 27.9385),
                                                viewOffsetX=42.9022, viewOffsetY=-17.9266)
session.viewports['Viewport: 1'].view.setValues(nearPlane=304.969,
                                                farPlane=460.21, width=180.446, height=70.3622, cameraPosition=(
                                                    -51.228, -36.9487, -329.104), cameraUpVector=(0.0583938, 0.957052,
                                                                                                  0.283977), cameraTarget=(26.8089, -20.229, 27.9385),
                                                viewOffsetX=42.9003, viewOffsetY=-17.9258)
session.viewports['Viewport: 1'].view.setValues(nearPlane=304.794,
                                                farPlane=464.241, width=180.342, height=70.3218, cameraPosition=(
                                                    -51.228, -54.863, -328.929), cameraUpVector=(0.0583938, 0.969201,
                                                                                                 0.239252), cameraTarget=(26.8089, -21.5902, 26.9529),
                                                viewOffsetX=42.8757, viewOffsetY=-17.9155)
n1 = a.instances['Part-1-1'].nodes
nodes1 = n1.getSequenceFromMask(mask=(
    '[#0:4063 #c0000000 #ff #7ffffc0 #fe000000 #3fff #fffff000',
    ' #80000001 #fffff #fffc0000 #7f #3ffffe0 #ff000000 #1fff',
    ' #fffff800 #c0000000 #1ff #0:53 #1ff8000 #ff800000 #fff',
    ' #7ffffc00 #e0000000 #3ffff #ffff0000 #1f #fffff8 #ffc00000',
    ' #7ff #3ffffe00 #f0000000 #7f ]', ), )
region = a.Set(nodes=nodes1, name='Set-1')
mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='Step-1',
                                 region=region, localCsys=None)

session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,
                                                       engineeringFeatures=ON, mesh=OFF)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=OFF)
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
e = p.elements
elements = e.getSequenceFromMask(mask=('[#ffffffff:3906 #ff ]', ), )
region = regionToolset.Region(elements=elements)
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0,
                    offsetType=MIDDLE_SURFACE, offsetField='',
                    thicknessAssignment=FROM_SECTION)

optimizations.optimize_topology(session, p, 'Model-1', 'Step-1', 1.25, 10)
