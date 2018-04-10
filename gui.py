import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.network.urlrequest import UrlRequest
import json
kivy.require('1.10.0')

# Makes window unable to be fullscreen
Config.set('graphics', 'resizable', False)


class LoginPage(Screen):
    inputStringUsername = ObjectProperty()
    inputStringPassword = ObjectProperty()

    def output_username(self):                  # Handle the username from login screen
        print(self.inputStringUsername.text)

    def output_password(self):                  # Handle the password from login screen
        print(self.inputStringPassword.text)


class MainMenuPage(Screen):
    pass


class AddFirearmPage(Screen):
    inputStringFirstName: ObjectProperty()
    inputStringSurName: ObjectProperty()
    inputStringSerialNumber: ObjectProperty()

    def output_form_details(self):
        print(self.inputStringFirstName.text)
        print(self.inputStringSurName.text)
        print(self.inputStringSerialNumber.text)

    def add_txn(self):
        pass

class ViewBlockchainPage(Screen):
    outputStringDetails:  ObjectProperty()
    test_string = "First Name: " + "" + "\nSurname: " + "" + "\nSerial Number: " + "" + ""
    def output_to_label(self):
            self.outputStringDetails.text = self.get_chain()

class Manager(ScreenManager):
    screen_one = ObjectProperty(None)       # Login Page
    screen_two = ObjectProperty(None)       # Main Menu Page
    screen_three = ObjectProperty(None)     # Add Firearm Page
    screen_four = ObjectProperty(None)      # View Blockchain Page


class GroupProjectApp(App):

    def build(self):
        m = Manager(transition=WipeTransition())
        return m


if __name__ == '__main__':
    GroupProjectApp().run()

