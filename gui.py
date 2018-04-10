import kivy
from kivy.app import App
from kivy.config import Config
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
import json

kivy.require('1.10.0')

# Makes window unable to be fullscreen and sets the size
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '850')
Config.set('graphics', 'height', '600')
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')


class LoginPage(Screen):
    inputStringUsername = ObjectProperty()
    inputStringPassword = ObjectProperty()

    def output_username(self):  # Handle the username from login screen
        print(self.inputStringUsername.text)

    def output_password(self):  # Handle the password from login screen
        print(self.inputStringPassword.text)

    def username_and_password_check(self, username, password):  # if statement to handle good and bad login attempts
        if username == " " and password == " ":
            self.manager.current = 'menu'
            self.clear_details()
        else:
            Factory.BadDetailsPopup().open()

    def clear_details(self):
        self.inputStringUsername.text = ""
        self.inputStringPassword.text = ""


class MainMenuPage(Screen):
    pass


class AddFirearmPage(Screen):
    inputStringLicenceNumber: ObjectProperty()  # THESE VARIABLE NAMES HAVE CHANGED
    inputStringTransactionNumber: ObjectProperty()
    inputStringFirearmModel: ObjectProperty()
    inputStringSerialNumber: ObjectProperty()
    inputStringStoreID: ObjectProperty()
    inputStringEmployeeID: ObjectProperty()

    verified = False

    def output_form_details(self, username, password):  # NEED THIS TO CHECK A LIST WITH STORED LOGIN DETAILS
        if username == " " and password == " ":
            self.verified = True
        else:
            Factory.BadDetailsPopup().open()

    def add_to_the_blockchain(self):  # ADD CODE TO ADD INPUT INFO TO THE BLOCK IN THIS FUNCTION
        if self.verified is True:
            print("Added to the block")
        else:
            Factory.NotVerifiedPopup().open()

        def add_txn(self):
            pass


class ViewBlockchainPage(Screen):
    outputStringBlockID: ObjectProperty()
    outputStringLicenceNumber: ObjectProperty()
    outputStringTransactionNumber: ObjectProperty()
    outputStringFirearmModel: ObjectProperty()
    outputStringSerialNumber: ObjectProperty()
    outputStringStoreID: ObjectProperty()
    outputStringEmployeeID: ObjectProperty()

    test_blockID = "123"  # TEST VALUES
    test_licenceNumber = "00000001"  # TEST VALUES
    test_transactionNumber = "748575"  # TEST VALUES

    def get_chain(self):
        req = UrlRequest("http://localhost:5000/chain")
        req.wait(delay=0.05)
        return str(req.result["length"])

    def output_to_label(self):
        self.outputStringBlockID.text = self.test_blockID
        self.outputStringLicenceNumber.text = self.test_licenceNumber
        self.outputStringTransactionNumber.text = self.test_transactionNumber
        self.outputStringEmployeeID.text = self.get_chain()  # THIS IS FROM YOUR CODE AND CAUSES A CRASH


class Manager(ScreenManager):
    screen_one = ObjectProperty(None)  # Login Page
    screen_two = ObjectProperty(None)  # Main Menu Page
    screen_three = ObjectProperty(None)  # Add Firearm Page
    screen_four = ObjectProperty(None)  # View Blockchain Page


class GroupProjectApp(App):

    def build(self):
        m = Manager(transition=WipeTransition())
        return m


if __name__ == '__main__':
    GroupProjectApp().run()
