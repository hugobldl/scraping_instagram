#================================================================= Library =====================================================
import requests
from bs4 import BeautifulSoup
import json
import urllib.request
import os
import time

#================================================================= Functions =====================================================

#Fonction extraction images
def extract_img(id, first, pseudo, profil_pic):

	if not os.path.exists(pseudo + '/images'):
		os.mkdir(pseudo + '/images')

	if int(first) == 0:
		print("/!\\/!\\/!\\ Ce compte ne contient aucun post. /!\\/!\\/!\\")

	url_img = 'https://www.instagram.com/graphql/query/?query_hash=15bf78a4ad24e33cbd838fdb31353ac1&variables={"id":"' + str(id) + '","first":' + str(first) + '}'

	response_img = requests.get(url_img)
	json_data_img = json.loads(response_img.text)
	links = json_data_img['data']['user']['edge_owner_to_timeline_media']['edges']

	lst = []
	lst.append(profil_pic)
	#with open('instajson.txt', 'w') as file:
	for link in links:
		lst.append(link['node']['display_url'])
			#file.write(link['node']['display_url'] + '\n')

	pourcent = 100 / (int(first) + 1)

	for element in lst:

		img_name = pseudo + '_' + str(lst.index(element))
		full_name = str(img_name) + '.jpg'
		urllib.request.urlretrieve(element, pseudo + '/images/' + full_name)

		multi = int(lst.index(element)) * float(pourcent)
		arrondi = "{0:.2f}".format(round(multi,2))
		os.system("cls")
		print("Téléchargement des images de "+pseudo+" en cours : " + str(arrondi) + ' % / 100 %')

	print(">Images bien téléchargés ! =======================================>")
	time.sleep(1)
	#print(lst)

#Fonction moyennes
def moyenne(id, first, pseudo, followers, follow, compte_recent, categorie_compte):

	url_moy = 'https://www.instagram.com/graphql/query/?query_hash=15bf78a4ad24e33cbd838fdb31353ac1&variables={"id":"' + str(id) + '","first":' + str(first) + '}'
	response_moy = requests.get(url_moy)
	json_data_moy = json.loads(response_moy.text)

	if int(first) == 0:
		#Ecriture dans CSV
		print("/!\\/!\\/!\\ Ce compte ne contient aucun post. /!\\/!\\/!\\")
		with open( pseudo + '/moyennes.csv', 'w') as outf:
			outf.write('Moyenne de likes , '+ str(first)+'\n')
			outf.write('Moyenne de commentaires , '+str(first)+'\n')
			outf.write('Fidélitée de l\'audience , '+str(first)+'% \n')
			outf.write('Nombre de posts , '+str(first)+'\n')
			outf.write('Nombre d\'abonnés , '+ str(followers)+ '\n')
			outf.write('Nombre d\'abonnement , '+str(follow)+'\n')
			outf.write('Compte récent  , '+str(compte_recent)+'\n')
			outf.write('Catégorie de compte  , '+str(categorie_compte)+'\n')
			#outf.write('Biographie  , '+str(biography)+'\n')

	else:
		#Moyenne de like
		likes = json_data_moy['data']['user']['edge_owner_to_timeline_media']['edges']
		total_like = 0
		for like in likes:
			total_like += like['node']['edge_media_preview_like']['count']
		moy_like = int(total_like) / int(first) 

		#Moyenne de commentaires
		coms = json_data_moy['data']['user']['edge_owner_to_timeline_media']['edges']
		total_com = 0
		for com in coms:
			total_com += com['node']['edge_media_to_comment']['count']
		moy_com = int(total_com) / int(first) 

		#Fidélitée de l'audience
		fide = (int(total_com) + int(total_like)) / int(followers)

		#Ecriture dans CSV
		with open( pseudo + '/moyennes.csv', 'w') as outf:
			outf.write('Moyenne de likes , '+ str(moy_like)+'\n')
			outf.write('Moyenne de commentaires , '+str(moy_com)+'\n')
			outf.write('Fidélitée de l\'audience , '+str(fide)+'% \n')
			outf.write('Nombre de posts , '+str(posts)+'\n')
			outf.write('Nombre d\'abonnés , '+ str(followers)+ '\n')
			outf.write('Nombre d\'abonnement , '+str(follow)+'\n')
			outf.write('Compte récent  , '+str(compte_recent)+'\n')
			outf.write('Catégorie de compte  , '+str(categorie_compte)+'\n')
			#outf.write('Biographie  , '+str(biography)+'\n')

		print(">Moyenne inscrite dans le fichier ! =======================================>")
		time.sleep(1)

#Fonction nouveau pseudo *a titre d'exemple car variable local* cf. choix == '4'
def new_pseudo(id, first, pseudo):

	"""
	data_pseudo = str(user_data)
	for loop in range(50):
		find_pseudo =   data_pseudo.find('@')

		new_pseudo = data_pseudo[int(find_pseudo):int(find_pseudo) + 25]
		find_end_pseudo =   new_pseudo.find('. ')

		if find_end_pseudo < 0:
				find_end_pseudo =   new_pseudo.find('"')
				if find_end_pseudo < 0:
					find_end_pseudo =   new_pseudo.find(',')
					if find_end_pseudo < 0:
						find_end_pseudo =   new_pseudo.find('\'')
						if find_end_pseudo < 0:
							find_end_pseudo =   new_pseudo.find(' ')

		clean_new_pseudo = new_pseudo[1 :int(find_end_pseudo)]
		data_pseudo = data_pseudo.replace('@', '', 1)

		if clean_new_pseudo not in lst_pseudo:
			lst_pseudo.append(clean_new_pseudo)

	#print(clean_new_pseudo)
	"""

	url_pseudo = 'https://www.instagram.com/graphql/query/?query_hash=15bf78a4ad24e33cbd838fdb31353ac1&variables={"id":"' + str(id) + '","first":' + str(first) + '}'
	response_pseudo = requests.get(url_pseudo)
	json_data_pseudo = json.loads(response_pseudo.text)

	if int(first) == 0:
		print("/!\\/!\\/!\\ Ce compte ne contient aucun post. /!\\/!\\/!\\")

	lst = []

	coms = json_data_pseudo['data']['user']['edge_owner_to_timeline_media']['edges']

	for com in coms:
		posts = com['node']['edge_media_to_comment']['edges']

		for post in posts:
			owner = post['node']['owner']['username']

			if owner not in lst:
				lst.append(owner)

	with open( pseudo + '/amis.csv', 'w') as outf:
		for ami in lst:
			outf.write(ami +'\n')

	print(">Liste d'amis créer ! =======================================>")
	time.sleep(1)

def pivot(pseudo, first, id):

	url_amis = 'https://www.instagram.com/graphql/query/?query_hash=15bf78a4ad24e33cbd838fdb31353ac1&variables={"id":"' + str(id) + '","first":' + str(first) + '}'
	response_amis = requests.get(url_amis)
	json_data_amis = json.loads(response_amis.text)

	lst_amis = []

	coms = json_data_amis['data']['user']['edge_owner_to_timeline_media']['edges']

	for com in coms:
		posts = com['node']['edge_media_to_comment']['edges']

		for post in posts:
			owner = post['node']['owner']['username']

			if owner not in lst_amis:
				lst_amis.append(owner)

	print("La liste d'amis est composée de "+str(len(lst_amis))+" personnes !")
	time.sleep(1)
	print("Début des extractions ...")
	time.sleep(1)

	url_pivot = 'https://www.instagram.com/graphql/query/?query_hash=15bf78a4ad24e33cbd838fdb31353ac1&variables={"id":"' + str(id) + '","first":' + str(first) + '}'
	response_pivot = requests.get(url_pivot)
	json_data_pivot = json.loads(response_pivot.text)

	nbr = 0 

	coms = json_data_pivot['data']['user']['edge_owner_to_timeline_media']['edges']

	for com in coms:
		posts = com['node']['edge_media_to_comment']['edges']

		for post in posts:
			owner = post['node']['owner']['username']

			if not os.path.exists(owner) and  nbr < int(len(lst_amis)):

				nbr += 1

				url_pivot_bis = 'https://www.instagram.com/' + str(owner) + '/'

				os.mkdir(str(owner))

				response_pivot = requests.get(url_pivot_bis)
				soup_pivot  = BeautifulSoup(response_pivot.text, 'lxml')

				script_pivot  = str(soup_pivot.findAll('script', {'type': 'text/javascript'})[3])
				raw_data_pivot  = script_pivot.replace(';' ,'').replace('window._sharedData =','').replace('<script type="text/javascript"> ','').replace('</script>','')
				json_data_pivot  = json.loads(raw_data_pivot)
				user_data_pivot  = json_data_pivot['entry_data']['ProfilePage'][0]['graphql']['user']

				status_pivot = user_data_pivot['is_private']
				profil_pic_pivot = user_data_pivot['profile_pic_url_hd']
				id_pivot = user_data_pivot['id']
				first_pivot = user_data_pivot['edge_owner_to_timeline_media']['count']

				followers_pivot = user_data_pivot['edge_followed_by']['count']
				follow_pivot = user_data_pivot['edge_follow']['count']
				compte_recent_pivot = user_data_pivot['is_joined_recently']
				categorie_compte_pivot = user_data_pivot['business_category_name']

				print(">Récupération des informations du compte : " + str(owner))


				if status == True:
					print("/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\")
					print("/!\\/!\\/!\\/!\\/!\\/!\\ Attention ce profil est privée. /!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\")
					print("/!\\/!\\/!\\ Les possibilités d'extraction/capitalisation sont réduites /!\\/!\\/!\\")
					print("/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\")

				moyenne(id_pivot, first_pivot, owner, followers_pivot, follow_pivot, compte_recent_pivot, categorie_compte_pivot)
				extract_img(id_pivot, first_pivot, owner, profil_pic_pivot)
				new_pseudo(id_pivot, first_pivot, owner)
				time.sleep(1)

	if nbr == 0:
		print(">Tout les données des amis potentielles ont été extraites ! ==========================================>")
		time.sleep(2)


#================================================================= Style =====================================================
os.system("cls")
print("=======================================")
print("===Bienvenue dans le Scraping Insta====")
print("=======================================")
pseudo  = input(">Entrez un nom de compte insta: ")
#lst_pseudo = []
flag  = True
while flag != False:
	os.system("cls")
	url = 'https://www.instagram.com/' + pseudo + '/'
	print("Récupération des informations du compte : " + url)

	if not os.path.exists(pseudo):
		os.mkdir(str(pseudo))

	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')

	script =str(soup.findAll('script', {'type': 'text/javascript'})[3])
	raw_data = script.replace(';' ,'').replace('window._sharedData =','').replace('<script type="text/javascript"> ','').replace('</script>','')
	json_data = json.loads(raw_data)
	user_data = json_data['entry_data']['ProfilePage'][0]['graphql']['user']


	posts = user_data['edge_owner_to_timeline_media']['count']
	followers = user_data['edge_followed_by']['count']
	follow = user_data['edge_follow']['count']
	profil_pic = user_data['profile_pic_url_hd']
	status = user_data['is_private']
	compte_recent = user_data['is_joined_recently']
	categorie_compte = user_data['business_category_name']
	#biography = user_data['biography']

	id = user_data['id']
	first = posts

	if status == True:
		print("/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\")
		print("/!\\/!\\/!\\/!\\/!\\/!\\ Attention ce profil est privée. /!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\")
		print("/!\\/!\\/!\\ Les possibilités d'extraction/capitalisation sont réduites /!\\/!\\/!\\")
		print("/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\")

	if os.path.exists(pseudo) and os.path.exists(pseudo+'/images') and os.path.exists(pseudo+'/moyennes.csv') and os.path.exists(pseudo+'/amis.csv') :

		print("/!\\/!\\/!\\ Toutes les données ont été extraites. /!\\/!\\/!\\/!\\/!\\/!\\")

	print("=============================")
	print("=== Options ( "+pseudo+" ) ===")
	print("=============================")
	print("- 1. Extraire les images")
	print("- 2. Moyennes")
	print("- 3. Extraire une liste d'amis")
	print("- 4. Tout")
	print("- 5. Choisir un autre profil")
	print("- 6. Pivoter")
	print("- 7. Quitter")
	print("=============================")
	choix = input("Faites votre choix > ")
	choix = str(choix)

	if choix == '1':
		extract_img(id, first, pseudo, profil_pic)

	elif choix == '2':
		 moyenne(id, first, pseudo, followers, follow, compte_recent, categorie_compte)

	elif choix == '3':
		new_pseudo(id, first, pseudo)
		"""
		new_pseudo(user_data)
		print(lst_pseudo)
		choix_pseudo = input("Entrez un des pseudo: ")
		pseudo = str(choix_pseudo)
		"""

	elif choix == '4':
		moyenne(id, first, pseudo, followers, follow, compte_recent, categorie_compte)
		extract_img(id, first, pseudo, profil_pic)
		new_pseudo(id, first, pseudo)

	elif choix == '5':
		print("---------------------------------------")
		pseudo  = input(">Entrez un nom de compte insta: ")

	elif choix == '6':
		pivot(pseudo, first, id)

	elif choix == '7':
		print("> A bientôt ! =====-----_____ :)")
		flag = False

	else:
		#NOTHING
		flag = True
