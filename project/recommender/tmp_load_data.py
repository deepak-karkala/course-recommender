import csv
#from recommender.models import Course

dataReader = csv.reader(open('recommender/formations_with_price.csv'), delimiter=';')

modeStrArr = ['Distance', 'Continu', 'Cours du soir', 'Cours d\'emploi', 'Partiellement présentiel', 'Sport-études']
levelStrArr = ['Advance', 'Cours spécialisés', 'Formation professionnelle supérieure', 'Hautes écoles']

sectorReader = csv.reader(open('recommender/sectors.csv'), delimiter=';')
sectorStrArr = []
for line in sectorReader:
    sectorStrArr.append(line[4])

for line in dataReader:
  if line[0] != 'Id': # Ignore the header line

    sectorStr = sectorStrArr[int(line[4])-186]

    c = Course(name=line[5], sector=line[4], mode=line[8], level=line[6], degree=line[7], price=line[9], 
        duration=line[11], duration_id=line[12], sectorStr=sectorStr, sectorStrMap=sectorStrMap, modeStr=modeStrArr[line[8]-1], 
        levelStr=levelStrArr[line[6]-1])
    c.save()
