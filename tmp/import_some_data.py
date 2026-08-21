import os
import yaml

base_path = os.path.dirname(__file__)
os.chdir(base_path)

for filename in os.listdir('exported_data'):
    file = open(f'exported_data/{filename}')
    data = yaml.safe_load(file)
    print(data)