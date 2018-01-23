#Mdoza
#Crawler to obtain new episodes for an anime based on url

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import sqlite3,time
from kivy.uix.screenmanager import ScreenManager, Screen
import requests, html5lib, lxml
from bs4 import BeautifulSoup
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty

#First Screen
class LoginScreen(Screen,GridLayout):
    GridLayout.cols=2

    popup = Popup(title='Login Failed',
                       content=Label(text=' Login did not work '),
                       size_hint=(.5, .5), size=(400, 400))

    def greeting(self,username, password):
        #Connection to already created DB
        with sqlite3.connect("default.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM users WHERE username= ? AND password = ?") #query for username and pass
        cursor.execute(find_user,[(username.text),(password.text)])
        results = cursor.fetchall()

        if results:
            for i in results:
                self.manager.transition.direction = 'left'
                self.manager.transition.duration = 1
                self.manager.current = 'SettingsScreen'
        else:
            self.popup.open() #call for popup when we get incorrect credentials



    def exitbutton(self):
        exit()

# Scrollable class for results from file
class Scrollable (ScrollView):

        file = open('links.txt', 'r') #Opens the file
        linklist = (file.read())
        textlink = linklist
        text = StringProperty(textlink)


#Seccon screen
class SettingsScreen(Screen,FloatLayout):

    def getepisodes (self, **kwargs):

        #In this case we want to links for episodes of a anime
        url = 'https://site.net/anime/5049/dragon-ball-super'

        # Create count for amount of links that we will get from site
        # We will create an event  alert based on number of counts
        currentcount = 0
        lastcount = 0
        baseurl = 'https://Site.net' #BASE URL OF SITE

        #file = open('episodeount.txt', 'r')
        #lastcount = int(file.read())

        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        pages = soup.find_all('a', class_='fa-play-circle')

        #load  file to write the links to
        file = open('links.txt', 'w')

        for page in pages:
            newurl = baseurl + page['href']
            currentcount += 1
            file.write(str(newurl))
            file.write("\n")
            print(newurl)
        file.close()

        if currentcount > lastcount:
            lastcount = currentcount
            file = open('episodeount.txt', 'w')
            file.write(str(lastcount))
            file.close()
        print(lastcount)

        self.clear_widgets()
        self.add_widget(Scrollable()) #call for the scroll widget

    def exitbutton(self):
        exit()


class MyApp(App):
    def build(self):
        #Screenmanager and screens that we will use.
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='SettingsScreen'))
        return sm


if __name__ == '__main__':
    MyApp().run()


