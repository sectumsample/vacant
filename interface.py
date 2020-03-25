import hhparser
import hierarchy
import stemmer
import datasetpreparator

skills = {'java':10,'sql':15,'oracle':8}

vacs = hhparser.HeadhunterParser(hhparser.url_init, hhparser.headers).hh_get_vacancies(list(skills.keys())[0], 30)

for vac in vacs:
    print(vac['title'])
    print(vac['content'])

targetprobs = list()
for i in range(len(vacs)):
    targetprobs.append(skills)

targetprobs = datasetpreparator.netFit(skills, vacs)

print(targetprobs)


