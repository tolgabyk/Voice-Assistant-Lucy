from playsound import playsound
import speech_recognition as sr
from gtts import gTTS
import pyaudio
import random
import os
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import google.generativeai as genai
import api_key

r = sr.Recognizer() # All vocalization operations will be facilitated by this command (bütün seslendirme işlemlerini bu komut sağlayacak)

class Voice_Asisstant():
    def audio(self,text): # The introduction of the assistant's voice (asistan sesi tanıtımı) 

        xtts = gTTS(text=text,lang="tr")
        file = "file"+str(random.randint(1,912392719382))+".mp3"
        xtts.save(file)
        playsound(file)             
        os.remove(file)

    def save_audio(self): # Perception of user' s voice (Kullanıcının sesini algılama) 
        
        with sr.Microphone() as source:
            listen = r.listen(source)
            voice = " "
            
            try:
                voice = r.recognize_google(listen,language = "tr-TR")
                print("Sizi dinliyorum") 
            
            except sr.UnknownValueError: 
                self.audio("Ne söylediğinizi anlayamadım")
            
            except sr.RequestError as e: #Connection Error (İnternet bağlantı hatası)
                print(f"Google Konuşma Tanıma servisinden sonuçları isteyemedi; {e}")

            return voice
        


    def sound(self,incoming_voice): 
        
        if "selam" in incoming_voice:
            self.audio("Size de selamlar tolga bey")
        
        elif "merhaba" in incoming_voice:
            self.audio("Size de merhaba tolga efendi")
        
        elif "video aç" in incoming_voice or "youtube aç" in incoming_voice or "müzik aç" in incoming_voice:
            self.audio("Ne açmamı istersiniz")
            data = self.save_audio()
            url = "https://www.youtube.com/results?search_query={}".format(data)
            scanner = webdriver.Chrome("C:/Users/USER/Desktop/chromedriver-win64/chromedriver.exe")
            scanner.get(url)
            button = scanner.find_element_by_xpath("//*[@id='video-title']").click()
            self.audio("istediğiniz içerik bu mu ")
            incoming_command = self.save_audio()
            if (incoming_command in "Hayır"):
                sayac = 2
                scanner.back()
                while (sayac < 5):
                    diger_videolar = scanner.find_element_by_xpath("//*[@id='contents']/ytd-video-renderer[{}]".format(sayac)).click()
                    time.sleep(5)
                    self.audio("istediğiniz içerik bu mu")
                    komut = self.mikrofon()

                    if (komut in "Evet"):
                        self.audio("keyifli vakit geçirmeler...")
                        break
                    else:
                        self.audio("o zaman diğer videolara bakalım")
                        scanner.back()
                        sayac += 1
                else:
                    self.seslendirme("keyifli vakit geçirmeler...")


        elif "google aç" in incoming_voice or "arama yap" in incoming_voice:
            self.audio("Ne aramamı istersiniz")
            data = self.save_audio()
            self.audio("{} için bunları buldum".format(data))
            url = "https://www.google.com/search?q={}".format(data)
            scanner = webdriver.Chrome("C:/Users/USER/Desktop/chromedriver-win64/chromedriver.exe")
            scanner.get(url)
            url2 = "//*[@id=rso']/div[1]/div/div/div/div/div/div/div/div[1]/div/span/a"
            button = scanner.find_element_by_xpath("//*[@id='rso']/div[1]/div/div/div/div/div/div/div/div[1]/div/span/a").click()

        elif "film aç" in incoming_voice:
            self.audio("Hangi tür film izlemek istersiniz")
            data = self.save_audio()
            self.audio("{} türü için bulduğum filmleri listeliyorum".format(data))
            url = "https://hdfilmcehennemi.cx/tur/{}".format(data)
            scanner = webdriver.Chrome("C:/Users/USER/Desktop/chromedriver-win64/chromedriver.exe")
            scanner.get(url)

            self.audio("Film önerisinde bulunmamı ister misiniz")
            answer = self.save_audio()
            print(answer)
            time.sleep(2)
            if answer=="evet":
                self.audio("Hemen önerimi gösteriyorum")
                random_number = random.randint(1,24)
                button = scanner.find_element_by_xpath("//*[@id='listehizala']/div[{}]/div/div[3]/a/div/span".format(random_number)).click()
            elif answer=="hayır":
                self.audio("İyi seyirler")

        elif "teşekkürler" in incoming_voice or "teşekkür ederim" in incoming_voice:
            self.audio("Rica ederim ne demek")

        elif "hava durumu" in incoming_voice or "hava durumu tahmini" in incoming_voice:
            self.audio("Hangi şehrin hava durumunu göstereyim")
            answer = self.save_audio()
            url = "https://www.ntv.com.tr/{}-hava-durumu".format(answer)

            request = requests.get(url)

            html = request.content

            soup = BeautifulSoup(html,"html.parser")

            max_degrees = soup.find_all("p",{"class":"hava-durumu--detail-data-item-bottom-temp-max"})
            min_degrees = soup.find_all("p",{"class":"hava-durumu--detail-data-item-bottom-temp-min"})
            degree_text = soup.find_all("div",{"class":"container hava-durumu--detail-data-item-bottom-desc"})

            maxs = []
            mins = []
            texts = []
            for i in max_degrees:
                i = i.text
                maxs.append(i)

            for y in min_degrees:
                y = y.text
                mins.append(y)

            for x in degree_text:
                x = x.text
                texts.append(x)

            all_in_one = f"{answer} için yarınki hava raporu şöyle: gündüz sıcaklığı {maxs[0]} derece, gece sıcaklığı {mins[0]} derece"
            
            self.audio(all_in_one)
            print(all_in_one)                
            
        
        elif "akıllı ol" in incoming_voice:
           
            self.audio("Zeka seviyemi artırıyorum")
            genai.configure(api_key=api_key.api)
            while True:
                    model = genai.GenerativeModel('gemini-pro')
                    self.audio("Konuşabilirsiniz")
                    prompt = self.save_audio()
                    if "kapat" in prompt or "zekanı azalt" in prompt:
                        break
                    
                    else:
                        response = model.generate_content(prompt)
                        print(response.text)
                        self.audio("Bilgileri ekrana yazdırdım. Seslendirmemi ister misiniz")
                        voicedprompt = self.save_audio()
                        if "evet" in voicedprompt.lower():
                            self.audio(response.text[:150])
                            time.sleep(2)
                            self.audio("Seslendirmeye devam edeyim mi")
                            continuee = self.save_audio()
                            if "evet" in continuee.lower():
                                self.audio(response.text[150:])
                            elif "hayır" in continuee.lower():
                                self.audio("Seslendirmeyi sonlandırıyorum")
                                break
                            else:
                                self.audio("Anlamadım. Seslendirmeyi sonlandırıyorum")
                                break
                        elif "Hayır" in voicedprompt.lower():
                            self.audio("Tamamdır")

        elif "oyun aç" in incoming_voice or "oyun" in incoming_voice:
            self.audio("Hangi oyunu başlatayım")
            choose_game = self.save_audio()
            if "lol" in choose_game or "league of legends" in choose_game or "lol aç" in choose_game:
                self.audio("hemen başlatıyorum")
                game_path = "C:/Riot Games/Riot Client/RiotClientServices.exe"
                os.startfile(game_path)
            else: # I have no other game if you want you can add (Bende başka oyun yok isterseniz ekleyebilirsiniz)
                self.audio("Böyle bir oyun bulunamadı")
        
        



assistant = Voice_Asisstant()

def wake_up(text): # waking function (uyandırma fonksiyonu)
    if(text=="hey lucy" or text=="lucy"):
        assistant.audio("Sizi dinliyorum") # not gonna run without saying hey lucy (hey lucy diyene kadar çalışmaz)
        answer = assistant.save_audio()
        if (answer !=""):
            assistant.sound(answer)

while True:
    voice = assistant.save_audio()
    
    if voice!=" ":
        voice = voice.lower()   
        print(voice)
        wake_up(voice)




