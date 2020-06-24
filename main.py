#esto es un 0?
#esto es una prueba de merge para git
#esto es un 1
#esto deberia ser una inconcistencia
from Libs import *
from kivy.clock import *
from MainPage import  CreateMainKV, MainScreen
from ProfilesPage import CreateProfilesKV, ProfilesScreen
from ProfilePage import CreateProfileKV, ProfileScreen
from ScreenManagment import CreateManager
from NavDrawer import CreateNavKV
from AnnouncePage import CreateAnnounceKV, AnnounceScreen
from PacksPage import CreatePacksKV,PacksScreen,ProfilePacksScreen

root_kv = """

<Snackbar>:

    BoxLayout:
        id: box
        size_hint_y: None
        height: dp(58)
        spacing: dp(5)
        padding: dp(10)
        y: -self.height

        canvas:
            Color:
                rgba: rgba("#f54242")
            Rectangle:
                pos: self.pos
                size: self.size

        MDLabel:
            id: text_bar
            size_hint_y: None
            height: self.texture_size[1]
            text: root.text
            font_size: root.font_size
            theme_text_color: 'Custom'
            text_color: get_color_from_hex('ffffff')
            shorten: True
            shorten_from: 'right'
            pos_hint: {'center_y': .5}

<Working>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0, 0, 1
            origin: root.center
    canvas.after:
        PopMatrix


    Image:
        # color : 1,0,0,1
        source: "images/icon.png"
        size_hint: None, None
        size: 150, 150
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

<AsyncImg@AsyncImage>:
    # size_hint: self.image_ratio, 1
    keep_ratio: False
    allow_stretch: True

<custom_description_label@MDLabel>:
    theme_text_color: "Custom"
    text_color: rgba("#f54242")

<SplashScreen>:
    name: "SplashScreen"
    MDBoxLayout:
        md_bg_color : rgba("#f54242")

"""

class SplashScreen(Screen):
    pass


class RegisterButton(MDRaisedButton):
    pass

class custom_description_label(MDLabel):
    pass

class LoginButton(MDRaisedButton):
    pass

class LogoutButton(MDRaisedButton):
    pass

class AsyncImg(AsyncImage):
    pass

class CustomDialog(MDDialog):

    opened = BooleanProperty(False)

    def open(self,**k):
        
        super(CustomDialog,self).open()
        self.opened = True

    def dismiss(self,**k):

        super(CustomDialog,self).dismiss()
        from threading import Timer
        t = Timer(15, self.timeout)
        t.start()

    def timeout(self):
        self.opened = False

class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Encuentros"
        super().__init__(**kwargs)
        
    def build(self):
        self.sm = CreateManager()
        # self.sm.current_user = {}
        self.sm.SplashScreen = SplashScreen()
        self.AddBox = CustomDialog()

        self.RootKV = Builder.load_string(root_kv)
        self.MainKV = Builder.load_string(CreateMainKV())
        self.NavKV = Builder.load_string(CreateNavKV())
        self.ProfilesKV = Builder.load_string(CreateProfilesKV())

        self.sm.MainScreen = MainScreen(sm=self.sm,
                                    callback=lambda status: self.ScreenAddAndRemove(self.sm.MainScreen,self.sm.SplashScreen,status))
        
        self.sm.ProfilesScreen = ProfilesScreen()
        self.sm.add_widget(self.sm.MainScreen)        
        self.sm.add_widget(self.sm.ProfilesScreen)
        self.theme_cls.primary_palette = "Red"

        return self.sm

    def on_resume(self,**kwargs):
        # super(MainApp,self).on_resume(**kwargs)
        pass
        # self.Paused = 0
        # if not self.AddBox.opened:
        #     self.AddBox.text="esto te aparece si salis y volves"
        #     self.AddBox.open()

    def on_start(self,**kwargs):
        pass
        
    def ScreenAddAndRemove(self,add,remove,status):
        if not status:            
            box = MDBoxLayout(orientation="vertical",padding=(0,0,0,0))
            title = MDLabel(font_style="H3",theme_text_color= "Custom",text_color=(1,1,1,1),halign="center",text="Encuentros")
            repalabel = MDLabel(font_style="H5",theme_text_color= "Custom",text_color=(1,1,1,1),halign="center",text="Estamos realizando mantenimiento en el servidor")
            repalabel2 = MDLabel(font_style="Subtitle2",theme_text_color= "Custom",text_color=(1,1,1,1),halign="center",text="Vuelve a intentar mas tarde...")
            reparaciones = AsyncImage(source="http://fgpresentaciones.com/images/app/reparaciones.gif")
            box.add_widget(title)
            box.add_widget(reparaciones)
            box.add_widget(repalabel)
            box.add_widget(repalabel2)
            self.sm.SplashScreen.add_widget(box)
            self.sm.add_widget(self.sm.SplashScreen)
            self.sm.current = "SplashScreen"
            return

        self.ProfileKV = Builder.load_string(CreateProfileKV())
        self.AnnounceKV = Builder.load_string(CreateAnnounceKV())
        self.AnnounceKV = Builder.load_string(CreatePacksKV())


        self.sm.ProfileScreen = ProfileScreen()
        self.sm.AnnounceScreen = AnnounceScreen()
        self.sm.PacksScreen = PacksScreen()
        self.sm.ProfilePacksScreen = ProfilePacksScreen()

        self.sm.add_widget(self.sm.AnnounceScreen)
        self.sm.add_widget(self.sm.ProfileScreen)
        self.sm.add_widget(self.sm.PacksScreen)
        self.sm.add_widget(self.sm.ProfilePacksScreen)
        self.root.remove_widget(remove)
        self.root.current = add.name

MainApp().run()
