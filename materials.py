STEEL = 'Steel'


def add_steel(model):
    # Create a material.
    steel = model.Material(name=STEEL)

    # Create the elastic properties: youngsModulus is 209.E3 and poissonsRatio is 0.3
    elasticProperties = (209.E3, 0.3)
    steel.Elastic(table=(elasticProperties, ))

    return steel


def add_all(model):
    add_steel(model)


if (__name__ == "__main__"):
    add_all(mdb.models[mdb.models.keys()[0]])
