import csv
#from recommender.models import Course

dataReader = csv.reader(open('recommender/formation.csv'), delimiter=';')
modeStrArr = ['Distance', 'Continu', 'Cours du soir', 'Cours d\'emploi', 'Partiellement présentiel', 'Sport-études', 'Non renseigné']
levelStrArr = ['Advance', 'Cours spécialisés', 'Formation professionnelle supérieure', 'Hautes écoles']

sectorReader = csv.reader(open('recommender/sectors.csv'), delimiter=';')
sectorStrArr = []
for l in sectorReader:
    sectorStrArr.append(l[4])

degreeReader = csv.reader(open('recommender/degrees.csv'), delimiter=';')
degreeStrArr = []
for l in degreeReader:
    degreeStrArr.append(l[4])

dataReader = csv.reader(open('recommender/formation.csv'), delimiter=';')

for line in dataReader:
    sectorStr = sectorStrArr[int(line[4])-186]
    degreeStr = degreeStrArr[int(line[7])-155]
    print(line)
    c = Course(name=line[5], sector=line[4], mode=line[8], level=line[6], degree=line[7], price=line[9], 
        duration=line[11], duration_id=line[12], sectorStr=sectorStr, modeStr=modeStrArr[int(line[8])-1], 
        levelStr=levelStrArr[int(line[6])-1], degreeStr=degreeStr)
    c.save()
