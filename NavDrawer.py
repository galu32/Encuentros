from Libs import *

def CreateNavKV():
    nav_kv = """

<NavDrawerItems@OneLineIconListItem>:
    text_color: rgba("#f54242")
    theme_text_color: "Custom"
    on_release : self.parent.parent.ScreenSwitcher(root.text)

<RedIconLeft@IconLeftWidget>
    text_color: rgba("#f54242")
    theme_text_color: "Custom"

<TermsCheck@MDCheckbox>:
    selected_color : rgba("#f54242")

<NavDrawer>
    
    login_card : LoginCard.__self__


    id : NavDrawer
    orientation : "vertical"
    # close_on_click : False
    MDGridLayout:
        id : NavDrawerGrid
        cols :  1

        MDToolbar:
            id : NavDrawerToolbar
            title : "Encuentros"
            pos_hint : {"top" : 1}
            right_action_items : [['close', lambda x : NavDrawer.set_state("close")]]

        NavDrawerItems:
            id : MainPage
            text : "Personas"

            RedIconLeft:
                icon : "human-male-female"

        NavDrawerItems:
            id : PacksPage
            text : "Packs"
            # on_release : root.ScreenSwitcher(self.id)
            RedIconLeft:
                icon : "camera"

        NavDrawerItems:
            id : AnnouncePage
            text : "Publicitar"
            RedIconLeft:
                icon : "publish"

    MDCard:
        id : LoginCard
        size_hint : None, .4
        width : root.width

        MDBoxLayout:
            id: LoginBox
            orientation : "vertical"
            padding : 30,10,30,10
            spacing : 3

            MDTextField:
                id : UserField
                pos_hint : {"top" : 1}
                hint_text : "Usuario..."

            MDTextField:
                id : PassField
                pos_hint : {"top" : 1}
                hint_text : "Contrsaeña..."
                password : True

            MDBoxLayout:
                id : ButtonsBox
                # size_hint : None,None
                # padding : 30,10,30,10
                spacing : 10

                MDRaisedButton:
                    id : RegisterButton
                    pos_hint :  {"center_x": .5, "center_y": .5}
                    text : "Registrarse"
                    on_release : root.CreateRegisterBox()

                MDRaisedButton:
                    id : LoginButton
                    pos_hint :  {"center_x": .5, "center_y": .5}
                    text : "Ingresar"
                    on_release : root.CreateLoggedBox()

"""
    return nav_kv

class AsyncImg(AsyncImage):
    pass

class custom_description_label(MDLabel):
    pass
        
class NavDrawerItems(OneLineIconListItem):
    pass

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

class TermsCheck(MDCheckbox):
    pass

class NavDrawer(MDNavigationDrawer):

    login_card = ObjectProperty(None)
    working = BooleanProperty(False)

    def __init__(self,**kwargs):
        super(NavDrawer,self).__init__(**kwargs)
        self.CurrentUser = None

    def on_touch_down(self,x):
        if not self.working:
            return super(NavDrawer,self).on_touch_down(x)

    def on_touch_move(self,x):
        if not self.working:
            return super(NavDrawer,self).on_touch_move(x)        

    def on_working(self,screen,value):
        if value:
            self.parent.add_widget(Working())
        else:
            self.parent.remove_widget(self.parent.children[0])

    def CreateRegisterBox(self):
        self.remove_widget(self.login_card)
        self.RegisterBox = MDBoxLayout(orientation="vertical",padding=(30,10,30,10), spacing=3)
        self.RegisterCard = MDCard(size_hint_y=1.5)
        self.RegUser = MDTextField(pos_hint = {"top" : 1})
        self.RegUser.hint_text="Usuario.."
        self.Email = MDTextField(pos_hint = {"top" : 1})
        self.Email.hint_text="Email.."
        self.Name = MDTextField(pos_hint = {"top" : 1})
        self.Name.hint_text="Nombre.."
        # self.Date = MDRaisedButton(pos_hint = {"center_x": .5, "center_y": .5},text="Fecha de Nacimiento")
        # self.Date.on_release = lambda  : MDDatePicker(callback=self.SetDateButton).open()
        # self.Terminos = MDChip(label='Check with icon',check= True)
        boxterminos = MDBoxLayout()
        boxterminos.add_widget(custom_description_label(text="Acepto los terminos"))
        self.Terminos = TermsCheck(pos_hint = {'center_x': .4, 'center_y': .5},size_hint_x=None)        
        boxterminos.add_widget(self.Terminos)
        self.ValidationCode = custom_description_label(text=f"{random.randint(100000, 999999)}",halign="center")
        self.Validation = MDTextField(pos_hint = {"top" : 1})#, helper_text= "Helper text on focus", helper_text= "This will disappear when you click off", helper_text_mode = "on_focus")
        self.Validation.hint_text="Escribe el codigo de arriba.."
        self.RegisterButtonBox = MDBoxLayout(spacing=10)
        self.GoBack = MDRaisedButton(pos_hint = {"center_x": .5, "center_y": .5},text="Volver")
        self.GoBack.on_release = self.GoBackLogin
        self.SendRegister = MDRaisedButton(pos_hint = {"center_x": .5, "center_y": .5},text="Enviar")
        self.SendRegister.on_release = self.SendRegisterRequest
        self.SendRegister.on_release = lambda : self.SendRegisterRequest()
        self.RegisterBox.add_widget(self.RegUser)
        self.RegisterBox.add_widget(self.Email)
        self.RegisterBox.add_widget(self.Name)
        self.RegisterBox.add_widget(boxterminos)
        self.RegisterBox.add_widget(self.ValidationCode)
        self.RegisterBox.add_widget(self.Validation)
        self.RegisterButtonBox.add_widget(self.GoBack)
        self.RegisterButtonBox.add_widget(self.SendRegister)
        self.RegisterBox.add_widget(self.RegisterButtonBox)
        self.RegisterCard.add_widget(self.RegisterBox)
        self.add_widget(self.RegisterCard)

    def SendRegisterRequest(self):
        User = self.RegUser.text
        Name = self.Name.text
        Email = self.Email.text
        if not User or not Name or not Email:
            return Snackbar(text="Debe completar todos los campos.", duration=1).show()
        if len(Email.split("@")) == 1: 
            return Snackbar(text="El formato del mail es incorrecto.", duration=2).show()
        if len(Email.split(".")) == 1:
            return Snackbar(text="El formato del mail es incorrecto.", duration=2).show()
        if self.ValidationCode.text != self.Validation.text:
            return Snackbar(text="El codigo de verificacion no es correcto.", duration=2).show()
        if not self.Terminos.active:
            return Snackbar(text="Debe aceptar los terminos", duration=2).show()
        import json
        import certifi
        cert = certifi.where()
        headers = {'Content-type': 'application/json', 'Accept': 'text/json'}
        body = json.dumps({"User" : User, "Name" : Name, "Email" : Email})
        self.working = True
        self.RegisterRequest = UrlRequest("https://fgpresentaciones.com/register", 
            on_success=self.GetRegisterRequest,
            req_body=body,
            req_headers=headers,
            ca_file=cert)

    def GetRegisterRequest(self,req,res):
        self.working = False
        if not res["Registered"]:
            return Snackbar(text="El Email o el Usuario ingresado ya se encuentra registrado.").show()  
        self.remove_widget(self.RegisterCard)
        Snackbar(text="Listo! Recibiras tu contraseña via E-Mail.",duration=3).show()
        self.add_widget(self.login_card)


    def SetDateButton(self,d):
        self.Date.text = f"Fecha: {str(d)}"

    def GoBackLogin(self):
        self.remove_widget(self.RegisterCard)
        self.add_widget(self.login_card)

    def CreateLoggedBox(self):
        Pass = self.ids.PassField.text
        User = self.ids.UserField.text
        print(Pass,User)
        if not Pass or not User:
            return Snackbar(text="Se debe completar el Usuario y la Contraseña.", duration=1).show()
        self.working = True
        import json
        import certifi
        cert = certifi.where()
        headers = {'Content-type': 'application/json', 'Accept': 'text/json'}        
        body = json.dumps({"User" : User, "Pass" : Pass})
        self.LoginRequest = UrlRequest("https://fgpresentaciones.com/login", 
            on_success=self.SetLoggedBox,
            req_body=body,
            req_headers=headers,
            ca_file=cert)

    def SetLoggedBox(self,req,res):
        self.working = False
        if not res["Status"]:
            return Snackbar(text="El usuario o la contraseña son incorrectos").show()     
        self.CurrentUser = res["Status"][0]   
        self.remove_widget(self.login_card)
        self.ProfileCard = MDCard(id="ProfileCard",size_hint=(None,.4),width=self.width)
        self.ProfileBox = MDGridLayout(id="ProfileBox",padding=(30,10,30,10))#, spacing=5)
        self.ProfileBox.cols = 2
        self.ProfileBox.rows = 3
        self.ProfileBox.spacing = 3
        self.ProfileBox.padding = (5,5,5,5)
        self.ProfileImage = AsyncImg(id="ProfileImage",source="images/profile.png", size_hint=(None,.5), width=self.ProfileCard.width / 2.5)
        self.ProfileBox.add_widget(self.ProfileImage)
        self.ProfileEdit = MDRaisedButton(id="ProfileEdit",text="Cambiar Contraseña")
        self.Logout = MDRaisedButton(id="ProfileLogout",text="Cerrar Sesion")
        self.Logout.on_release = self.LogoutUser
        self.NameLabel = custom_description_label(text=self.CurrentUser["Name"])
        self.ProfileBox.add_widget(self.NameLabel)
        self.ProfileBox.add_widget(self.ProfileEdit)
        self.ProfileBox.add_widget(self.Logout)
        self.ProfileCard.add_widget(self.ProfileBox)
        self.add_widget(self.ProfileCard)

    def LogoutUser(self):
        self.CurrentUser = None
        self.remove_widget(self.ProfileCard)
        self.add_widget(self.login_card)

    def ScreenSwitcher(self,screen):
        if not self.CurrentUser and screen not in  ["Personas","Publicitar"]:
            return Snackbar(text="Debes ingresar con tu usuario y contraseña primero").show()
        if screen not in  ["Personas","Publicitar"]:
            # if screen == "Publicitar":
            #     self.parent.parent.current = "AnnounceScreen"
            if screen == "Packs":
                self.parent.working = True
                import json
                import certifi
                cert = certifi.where()
                headers = {'Content-type': 'application/json', 'Accept': 'text/json'}
                body = json.dumps({"Genero":"Mujer"})
                self.SearchProfilesRquest = UrlRequest("https://fgpresentaciones.com/get_packs",
                                         on_success=lambda x,y : self.parent.parent.PacksScreen.UpdateProfiles(self.parent.parent,x,y,True),
                                        req_body=body,req_headers=headers,ca_file=cert)

            self.set_state("close")