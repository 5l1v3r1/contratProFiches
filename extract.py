import urllib.request
from lxml import etree
import datetime


mat_codes={  
   "Architectures Logicielles":"18SDIAL",
   "Architecture Logicielle":"18SDIAL",
   "High Performance Computing":"18SDIHPC",
   "Calcul Haute Performance et Simulation":"18SDIHPC",
   "Ingénierie des exigences":"18SDIIEM",
   "Performance du processus d'informatisation":"18SDIPPI",
   "Sécurité systèmes mobiles et communicants":"18STISR",
   "Réseaux mobiles":"18STIRM",
   "Réseaux véhiculaires":"18STINRV",
   "Cloud computing":"18STICC",
   "Algorithmique distribuée":"18STIAD",
   "Service Web et système de Workflow":"18STIWG",
   "Base de l'administration système":"18STIASE",
   "Bases de l'Administration Système":"18STIASE",
   "Big data 2":"18STIBGD",
   "Création d'entreprise et défis de l'innovation":"18SHCEMS",
   "Anglais - S9":"18SHANS9",
   "Langues Vivantes":"18SHANS9",
   "Management de projet":"18SHMP"
   

}

def mat_code(mat):
	for code in mat_codes:
		if(mat.lower()[:len(code)]==code.lower()):
			return mat_codes[code]
	return ""

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
		semaines[semaine.findtext('alleventweeks')]["date_fin"]=str(int(semaine.findtext('description')[-10:][:2])+7)+semaine.findtext('description')[-10:][2:]
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
			matiere=mat_code(resources.find("module").findtext("item"))
		except AttributeError:
			matiere=""

		try:
			salle=resources.find("room").findtext("item")
		except AttributeError:
			salle=""
	
		try:
			prof=resources.find("staff").findtext("item")
		except AttributeError:
			prof=""
	
		#print(matiere)
		#print(salle)
		#print(prof)

		mat={}
		mat["date"]=str(jour)[:10].split("-")
		mat["date"]=mat["date"][2]+"/"+mat["date"][1]+"/"+mat["date"][0]
		mat["debut"]=event.findtext('starttime')
		mat["fin"]=event.findtext('endtime')
		mat["nom"]=matiere
		mat["prof"]=prof
		mat["salle"]=salle
		semaines[event.findtext('rawweeks')]["matieres"].append(mat)

		
	
	
	for sem in semaines:
		to_delete=[]
		for i in range(1,len(semaines[sem]["matieres"])):
			if semaines[sem]["matieres"][i-1]["date"] == semaines[sem]["matieres"][i]["date"] and semaines[sem]["matieres"][i-1]["nom"] == semaines[sem]["matieres"][i]["nom"] and semaines[sem]["matieres"][i]["nom"] != "":
				semaines[sem]["matieres"][i-1]["fin"]=semaines[sem]["matieres"][i]["fin"]
				to_delete.insert(0,i)
		for i in to_delete:
			del(semaines[sem]["matieres"][i])


	return semaines

def create_page(semaine):
	page_content=""
	page_content+="<html>\n"
	page_content+="	<head>\n"
	page_content+="		<style type='text/css'>\n"
	page_content+="			@page \n"
	page_content+="    		{\n"
	page_content+="    		    size:  auto;   /* auto is the initial value */\n"
	page_content+="    		    margin: 1mm;  /* this affects the margin in the printer settings */\n"
	page_content+="    		}\n"
	page_content+="			body {\n"
	page_content+="			width: 21cm;\n"
	page_content+="  			height: 29.7cm; \n"
	page_content+="			margin: 0;\n"
	page_content+="			}\n"
	page_content+="			table { \n"
	page_content+="				white-space: nowrap; \n"
	page_content+="				margin-right:40px;\n"
	page_content+="				margin-left:40px;\n"
	page_content+="			}\n"
	page_content+="			td {\n"
	page_content+="  				-webkit-column-width: 100px; /* Chrome, Safari, Opera */\n"
	page_content+="  				-moz-column-width: 100px; /* Firefox */\n"
	page_content+="  				column-width: 146px;\n"
	page_content+="  				height: 19px;\n"
	page_content+="\n"
	page_content+="			}\n"
	page_content+="			.logo{\n"
	page_content+="				float: right;\n"
	page_content+="				height: 100px;\n"
	page_content+="			}\n"
	page_content+="			.matieres{\n"
	page_content+="				 border-collapse: collapse;\n"
	page_content+="			}\n"
	page_content+="			.matieres th{\n"
	page_content+="  				border: 1px solid black;\n"
	page_content+="			}\n"
	page_content+="			.matieres td{\n"
	page_content+="  				border: 1px solid black;\n"
	page_content+="  				height: 35px;\n"
	page_content+="  				text-align: center;\n"
	page_content+="			}\n"
	page_content+="			.footer{\n"
	page_content+="				position:absolute;\n"
	page_content+="  				bottom:150;\n"
	page_content+="  				width:100%;\n"
	page_content+="  				\n"
	page_content+="   \n"
	page_content+="			}\n"
	page_content+="\n"
	page_content+="		</style>\n"
	page_content+="	</head>\n"
	page_content+="	<body>\n"
	page_content+="		<div class='head'> \n"
	page_content+="		<img class='logo' src='isty.png'>\n"
	page_content+="		<table>\n"
	page_content+="			<tr><td colspan=5></td></tr>\n"
	page_content+="			<tr><td colspan=5></td></tr>\n"
	page_content+="			<tr><td colspan=5></td></tr>\n"
	page_content+="			<tr><td colspan=5><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;IATIC5 - Contrat de Professionnalisation</b></td></tr>\n"		
	page_content+="			<tr><td colspan=5></td></tr>"
	page_content+="			<tr><td><b>NOM :</b></td><td></td><td><b>Prénom :</b></td><td colspan='2'></td></tr>"
	page_content+="			<tr><td></td><td>Du</td><td>Au</td><td colspan='2'></td></tr>"
	page_content+="			<tr><td><b>Semaine %s</b></td><td>%s</td><td>%s</td><td colspan='2'></td></tr>"%(semaine["num"],semaine["date"],semaine["matieres"][-1]["date"])
	page_content+="			<tr><td colspan=5></td></tr>"
	page_content+="			<tr><td colspan=5></td></tr>"
	page_content+="		</table>"
	page_content+="		</div>"
	page_content+="		<div class='bottom'>"
	page_content+="			<table class='matieres'>"
	page_content+="				<tr><th>Date</th><th>Horaires (de ...h à ...h)</th><th>Matière</th><th>Nom de l'enseignant</th><th>Signature de l'enseignants</th></th>"
	i=0
	for matiere in semaine["matieres"]:
		if matiere["nom"]!="" and matiere["prof"]!="":
			page_content+="				<tr><td>%s</td><td>De %s à %s</td><td>%s</td><td>%s</td><td></td></tr>"%(matiere["date"],matiere["debut"],matiere["fin"],matiere["nom"],matiere["prof"])
			i+=1
	for j in range(i, 15):
		page_content+="				<tr><td></td><td></td><td></td><td></td><td></td></tr>"
	page_content+="			</table>"
	page_content+="		</div>"
	page_content+="		<div class='footer'>"
	page_content+="			<table>"

	page_content+="				<tr><td></td><td></td><td></td><td></td></tr>"
	page_content+="				<tr><td></td><td>A Vélizy-Villacoubay, le</td><td></td><td></td></tr>"
	page_content+="				<tr><td></td><td></td><td></td><td></td></tr>"
	page_content+="				<tr><td></td><td>L'étudiant,</td><td></td><td>Le responsable pédagogique,</td></tr>"
	page_content+="				<tr><td></td><td></td><td></td><td></td></tr>"
	page_content+="				<tr><td></td><td></td><td></td><td></td></tr>"
	page_content+="				<tr><td></td><td></td><td></td><td></td></tr>"
	page_content+="				<tr><td></td><td></td><td></td><td></td></tr>"	
	page_content+="				<tr><td></td><td></td><td></td><td></td></tr>"
	page_content+="			</table>"
	page_content+="		</div>"
	page_content+="	</body>"
	page_content+="</html>"
	with open(semaine["num"]+".html","w+") as fichier:
		fichier.write(page_content)
		fichier.close()

def create_pages(semaines):
	for semaine in semaines:
		create_page(semaines[semaine])

if __name__ == '__main__':
	create_pages(extract())



