# from ScreenManagment import CreateManager
# from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.loader import Loader
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.scrollview import ScrollView
from kivymd import images_path
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.banner import MDBanner
from kivymd.uix.bottomnavigation import MDBottomNavigationItem,MDBottomNavigation,MDBottomNavigationHeader,MDTab
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.button import MDFlatButton,MDRaisedButton,MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine, MDExpansionPanel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel 
from kivymd.uix.list import OneLineListItem,OneLineIconListItem,IconLeftWidget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.progressloader import MDProgressLoader
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.taptargetview import MDTapTargetView
from kivymd.uix.toolbar import MDToolbar
from kivymd.utils.fitimage import FitImage
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.list import MDList
from kivymd.uix.textfield import MDTextField,MDTextFieldRect
from kivymd.uix.picker import MDDatePicker
from kivy.properties import *
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivymd.uix.chip import MDChip
from kivymd.uix.selectioncontrol import MDCheckbox
from kivmob import KivMob,TestIds
import webbrowser
import certifi
# import os
import random

class Working(FloatLayout):
    angle = NumericProperty(0)
    def __init__(self, **kwargs):
        super(Working, self).__init__(**kwargs)
        anim = Animation(angle = 360, duration=2) 
        anim += Animation(angle = 360, duration=2)
        anim.repeat = True
        anim.start(self)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0

class CustomScreen(Screen):
    
    working = BooleanProperty(defaultvalue=False)

    def __init__(self,**kwargs):
        super(CustomScreen,self).__init__(**kwargs)

    def on_touch_down(self,x):
        if not self.working:
            return super(CustomScreen,self).on_touch_down(x)

    def on_touch_move(self,x):
        if not self.working:
            return super(CustomScreen,self).on_touch_move(x)        

    def on_working(self,screen,value):
        if value:
            self.add_widget(Working())
        else:
            self.remove_widget(self.children[0])