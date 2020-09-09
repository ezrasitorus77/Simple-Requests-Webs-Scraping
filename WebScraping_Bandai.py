from bs4 import BeautifulSoup # import modul yang diperlukan
import requests, json, string

req = requests.get("http://www.scifijapan.com/articles/2015/10/04/bandai-ultraman-ultra-500-figure-list/") # request untuk scrap website

if req.status_code == 200: # cek jika website bisa di akses (status code request == 200)
    soup = BeautifulSoup(req.text, "html.parser")
else: # jika tidak maka error ditampilkan kepada user
    raise ConnectionError("Can not access the website. Please re - check the url.")

ultraMans, UM, MON = soup.find_all("strong"), {}, {} # menyatakan 3 variabel penting untuk proses selanjutnya, dimana UM adalah tempat untuk menyimpan nama - nama Ultra Man, sedangkan MON untuk monster
for index, um in enumerate(ultraMans): # memakai enumerate karena ingin mengakses index
    i = 1
    if "Ultra Hero" in um.text: # karena ultraMans.text tidak hanya mengandung nama - nama Ultra Man dan Monster, maka klausul ini perlu dinyatakan
        while ultraMans[index + i].text[0:2].isdigit(): # nama - nama Ultra Man berada di persis di bawah judul "Ultra Hero" dan berakhir saat item selanjutnya sudah tidak mengandung angka (nomor Ultra Man) di awal str
            UM[ultraMans[index + i].text[0:2]] = ultraMans[index + i].text[3:] # append elemen selanjutnya dari tiap elemen sebelumnya
            i += 1
       
        continue # jika kondisi sudah terpenuhi (tidak ada lagi str diawali nomor monster / digit) maka loop dilanjutkan. Dengan kata lain, urutan untuk Ultra Man sudah habis

    elif "Ultra Monster" in um.text: # kondisi diberi karena nama - nama Monster muncul setelah judul "Ultra Monster"
        while ultraMans[index + i].text[0:2].isdigit(): # proses selanjutnya identik dengan proses Ultra Man di atas
            MON[ultraMans[index + i].text[0:2]] = ultraMans[index + i].text[3:]
            i += 1
        
        break # sebenarnya break juga bisa tidak digunakan dengan asumsi tidak ada lagi str - str lainnya yang mengandung str "Ultra Hero" atau "Ultra Monster". Namun, untuk menghadapi segala kemungkinan, maka break dirasa perlu ditulis

res = [{"Ultra Man" : UM, "Monster" : MON}] # memasukkan ke dalam list agar memenuhi kaidah bentuk JSON

with open("WebScraping_Bandai.json", "w") as f: # menulis list tersebut ke dalam format JSON dan menyimpannya
    json.dump(res, f)