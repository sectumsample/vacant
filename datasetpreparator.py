import json
import os.path
import random
random.seed(205)
from outils import *
import stemmer


srcFolder = 'vacancies/'
dstFolder = 'dataset/'
allSkillsFileName = 'skills'
datasetFileName = 'dataset'

vacanciesNames = [srcFolder+item for item in os.listdir(srcFolder)]

jsons = [load_json_vacancy(name) for name in vacanciesNames]
                       
skills = set()
dataset = list()
                       
for vac in jsons:
    skills.update(vac['skills'])
skills = list(skills)

for vac in jsons:
    content = vac['company'] + ' ' + vac['title'] + ' ' + vac['content']
    content = stemmer.stemmize(content)
                       
    existing_skills = vac['skills']
    target = [1.0 if skill in existing_skills else 0.0 for skill in skills]
    dataset.append({'target': target, 'content': content})

save_json_file(allSkillsFileName, list(skills))
save_json_file(datasetFileName, dataset)
