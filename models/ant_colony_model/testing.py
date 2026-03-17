from models.ant_system.ant_system.model import AntScenario, AntModel

model = AntModel(scenario=AntScenario())

print(model.grid.food)