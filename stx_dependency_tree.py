
import glob

files = glob.glob('./**/*.spec', recursive=True)

graph = {}

for f in files:
    with open(f) as spec:
        packagespec = f.split('/')[-1].split('.')[0]
        graph[packagespec] = []
        #import pdb; pdb.set_trace()
        for line in spec.readlines():
            if 'BuildRequires' in line:
                graph[packagespec].append(line.split(':')[-1].strip())

print(graph)
