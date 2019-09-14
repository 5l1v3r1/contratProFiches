import urllib.request
from lxml import etree
import datetime

def extract():
		
	#output = open("output.xml","w") 
	rq=urllib.request.Request('http://chronos.iut-velizy.uvsq.fr/EDTISTY/g112050.xml')
	rq.add_header("Authorization", "Basic ZXR1aXN0eTppc3R5") # user:pass base64 encoded
	site=urllib.request.urlopen(rq)
	xmlResult=site.read().decode('utf8')
	#print(xmlResult)
	
	tree = etree.fromstring(xmlResult)
	semaines = {}
	for semaine in tree.xpath("/timetable/span"):

		semaines[semaine.findtext('alleventweeks')]={}
		semaines[semaine.findtext('alleventweeks')]["date"]=semaine.findtext('description')[-10:]
		semaines[semaine.findtext('alleventweeks')]["num"]=semaine.findtext('title')
		semaines[semaine.findtext('alleventweeks')]["matieres"]=[]
	#print(semaines)
	result="<matieres>\n"
	#print("<matieres>\n");
	
	for event in tree.xpath("/timetable/event"):
		#print("\nELEMENT ################")

		#print(event.findtext('starttime'))
		#print(event.findtext('endtime'))
		#print(semaines[event.findtext('rawweeks')])
		dateSemaine = datetime.datetime.strptime(semaines[event.findtext('rawweeks')]["date"], "%d/%m/%Y")
		jour = dateSemaine + datetime.timedelta(days=int(event.findtext('day')))
		#print(str(jour)[:10])
	
		resources=event.find("resources");
		try:
			matiere=resources.find("module").findtext("item")
		except AttributeError:
			matiere="ISTY"
		try:
			salle=resources.find("room").findtext("item")
		except AttributeError:
			salle="ISTY"
	
		try:
			prof=resources.find("staff").findtext("item")
		except AttributeError:
			prof="ISTY"
	
		#print(matiere)
		#print(salle)
		#print(prof)

		mat={}
		mat["date"]=str(jour)[:10]
		mat["debut"]=event.findtext('starttime')
		mat["fin"]=event.findtext('endtime')
		mat["nom"]=matiere
		mat["prof"]=prof
		mat["salle"]=salle
		semaines[event.findtext('rawweeks')]["matieres"].append(mat)

		
		
	
	
	return str(semaines)

if __name__ == '__main__':
	print(extract())



