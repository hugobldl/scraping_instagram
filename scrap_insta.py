#================================================================= Library =====================================================
import requests
from bs4 import BeautifulSoup
import json
import random
import urllib.request
import os


#================================================================= Functions =====================================================

#Fonction extraction images
def extract_img(id, first, pseudo):

	if not os.path.exists(pseudo + '/images'):
		os.mkdir(pseudo + '/images')

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
		print("Téléchargement des images en cours : " + str(arrondi) + ' % / 100 %')

	os.system("cls")
	print(">Images bien téléchargés ! =======================================>")
	#print(lst)

#Fonction moyennes
def moyenne(id, first, pseudo):

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
			outf.write('Nombre de posts , '+str(posts)+'\n')
			outf.write('Nombre d\'abonnés , '+ str(followers)+ '\n')
			outf.write('Nombre d\'abonnement , '+str(follow)+'\n')
			outf.write('Compte récent  , '+str(compte_recent)+'\n')
			outf.write('Catégorie de compte  , '+str(categorie_compte)+'\n')
			outf.write('Biographie  , '+str(biography)+'\n')

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
			outf.write('Biographie  , '+str(biography)+'\n')

		print(">Moyenne inscrite dans le fichier ! =======================================>")

#Fonction nouveau pseudo
def new_pseudo(user_data):

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

#================================================================= Style =====================================================
print("=======================================")
print("===Bienvenue dans le Scraping Insta====")
print("=======================================")
pseudo  = input(">Entrez un nom de compte insta: ")
lst_pseudo = []
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
	biography = user_data['biography']

	id = user_data['id']
	first = posts

	if status == True:
		print("/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\")
		print("/!\\/!\\/!\\/!\\/!\\/!\\ Attention ce profil est privée. /!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\")
		print("/!\\/!\\/!\\ Les possibilités d'extraction/capitalisation sont réduites /!\\/!\\/!\\")
		print("/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\/!\\")

	if os.path.exists(pseudo) and os.path.exists(pseudo+'/images') and os.path.exists(pseudo+'/moyennes.csv') :

		print("/!\\/!\\/!\\ Toutes les données ont été extraites. /!\\/!\\/!\\/!\\/!\\/!\\")

	print("=============================")
	print("=== Options ( "+pseudo+" ) ===")
	print("=============================")
	print("- 1. Extraire les images")
	print("- 2. Moyennes")
	print("- 3. Tout")
	print("- 4. Trouver un profil (listes)")
	print("- 5. Choisir un autre profil")
	print("- 6. Quitter")
	print("=============================")
	choix = input("Faites votre choix > ")
	choix = str(choix)

	if choix == '1':
		extract_img(id, first, pseudo)

	elif choix == '2':
		 moyenne(id, first, pseudo)

	elif choix == '3':
		moyenne(id, first, pseudo)
		extract_img(id, first, pseudo)

	elif choix == '4':
		new_pseudo(user_data)
		print(lst_pseudo)
		choix_pseudo = input("Entrez un des pseudo: ")
		pseudo = str(choix_pseudo)

	elif choix == '5':
		print("---------------------------------------")
		pseudo  = input(">Entrez un nom de compte insta: ")

	elif choix == '6':
		print("> A bientôt ! =====-----_____ :)")
		flag = False

	else:
		#NOTHING
		flag = True
