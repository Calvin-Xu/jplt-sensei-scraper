from bs4 import BeautifulSoup
import requests
import time
import shutil

for i in range(1, 5 + 1):
	url = "https://jlptsensei.com/jlpt-n3-grammar-list/page/" + str(i) + "/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, "lxml")
	
	table = soup.find(id = "jl-grammar")
	table_body = table.find("tbody")
	rows = table_body.find_all("tr")
	for row in rows:
		try:
			indexColumn = row.find_all("td", {"class": "jl-td-num align-middle text-center"})[0]
			japaneseColumn = row.find_all("td", {"class": "jl-td-gj align-middle"})[0]
			englishColumn = row.find_all("td", {"class": "jl-td-gm align-middle"})[0]
			
			index = indexColumn.text
			japanese = japaneseColumn.a.text
			english = englishColumn.text
			
			# for continue in the middle
			if int(index) > 0:
				f = open("n3.txt", "a")
				f.write(index + "|" + japanese + "|" + english + "\n")
				f.close()
				
				# get image
				try:
					japaneseHref = japaneseColumn.a["href"]
					flashCardPage = requests.get(japaneseHref)
					flashCardSoup = BeautifulSoup(flashCardPage.text, "lxml")
					imageDiv = flashCardSoup.find_all("div", {"class": "text-center mt-4 grammar-thumbnail-cont"})[0]
					imageUrl = next(imageDiv.children, None).a["href"]
					img_data = requests.get(imageUrl).content
					with open(str(index) + ".png", "wb") as handler:
						handler.write(img_data)
				except AttributeError:
					print("Unable to find image for", index)
				time.sleep(1)
		except IndexError:
			print("Unable to parse row")
		
#		print(index, japanese, english)