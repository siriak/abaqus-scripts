from abaqus import *
from abaqusConstants import *
import visualization

VIEWPORT_NAME = 'Viewport: 1'
JOB_NAME_BASE = 'Job'

def create_job(model_name, job_name):
    return mdb.Job(name=job_name, model=model_name, numCpus=16, numDomains=128)

def run_job(job, job_name):
    job.submit()
    job.waitForCompletion()
    return visualization.openOdb(path=job_name + '.odb')

def display_results(odb, viewport):
    # Open the output database and display a default contour plot.
    viewport.setValues(displayedObject=odb)
    viewport.odbDisplay.display.setValues(plotState=CONTOURS_ON_DEF)
    viewport.odbDisplay.commonOptions.setValues(renderStyle=FILLED)

def delete_points(odb, part, untouchable_nodes, load_step_name, remove_percent):
    # Find elements where stress is minimal and delete them
    results = [x for x in odb.steps[load_step_name].frames[-1].fieldOutputs["S"].values if x.elementLabel not in untouchable_nodes]
    all_points = sorted(results, key = lambda x: x.mises)
    print('total: ' + str(len(all_points)))
    print('removed: ' + str(int(remove_percent * len(all_points) / 100)))
    minStressPoints = [x.elementLabel for x in all_points][:int(remove_percent * len(all_points) / 100)]
    elements = [x for x in part.elements if x.label in minStressPoints]
    part.deleteElement(elements=elements, deleteUnreferencedNodes=ON)

def get_max_stress(odb, load_step_name):
    return max([x.mises for x in odb.steps[load_step_name].frames[-1].fieldOutputs["S"].values])

def optimize_topology(session, part, model_name, load_step_name, stress_multiplier, remove_percent_per_step):
    untouchable_nodes = set()
    for set_name in part.sets.keys():
        untouchable_nodes.update([node.label for node in part.sets[set_name].nodes])

    i = 0
    max_stress_initial = None
    while True:
        job_name = JOB_NAME_BASE + '_' + str(i)
        job = create_job(model_name, job_name)
        odb = run_job(job, job_name)
        display_results(odb, session.viewports[VIEWPORT_NAME])
        max_stress = get_max_stress(odb, load_step_name)
        if max_stress_initial is None:
            max_stress_initial = max_stress
        if max_stress > stress_multiplier * max_stress_initial:
            break
        delete_points(odb, part, untouchable_nodes, load_step_name, remove_percent_per_step)
        i += 1

if (__name__ == '__main__'):
    model = mdb.models[mdb.models.keys()[0]]
    part = model.parts[model.parts.keys()[0]]
    optimize_topology(session, part, 'Model-1', 'Load', 1.25, 5)
