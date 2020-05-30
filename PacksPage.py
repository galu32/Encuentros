from Libs import *
from ProfilesPage import ProfilesScreen
def CreatePacksKV():
    packs_kv = """

<ProfilePacksScreen@ProfilesScreen>:
    id : ProfilePacksScreen
    name : "ProfilePacksScreen"

<AnonimousForm@MDBoxLayout>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDTextField:
        id : useremail
        hint_text: "Tu email.."
        text : root.usermail

    MDTextField:
        id : message
        multiline: True
        text: "Hola vi tu pack %s en Encuentros y me gustaria adquirirlo." % root.packname
        hint_text: "Mensaje.."

    # SendForm:
    #     text : "Enviar"
    #     on_release : self.SendForm()

<PacksScreen@ProfilesScreen>
    id : PacksScreen
    name : "PacksScreen"
    """
    return packs_kv

class custom_one_list(OneLineListItem):
    pass

class RoundedCardBox(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

class AsyncImg(AsyncImage):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)      

class ProfilesCard(MDCard):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

class AnonimousForm(MDBoxLayout):
    packname = StringProperty()
    usermail = StringProperty()
    pass

class SendForm(MDRaisedButton):

    def __init__(self,**kwargs):
        super(SendForm,self).__init__(**kwargs)

    def print(self):
        print(1)
    pass

class PacksScreen(ProfilesScreen):

    def __init__(self,**kwargs):
        super(PacksScreen,self).__init__(**kwargs)
        self.ids.ProfilesToolbar.add_widget(MDRaisedButton(#on_release=self.AvaiblePacks
            pos_hint={"center_x": .5, "center_y": .5},text="Mis Pack Disponibles"))
        self.ids.ProfilesToolbar.title = "Packs"

    def ChangeGender(self,gender):
        import json
        import certifi
        cert = certifi.where()
        headers = {'Content-type': 'application/json', 'Accept': 'text/json'}
        body = json.dumps({"Genero":gender})
        self.working = True
        self.SearchProfilesRquest = UrlRequest("https://fgpresentaciones.com/get_packs",
                                 on_success=lambda x,y : self.UpdateProfiles(self.sm,x,y,True),
                                req_body=body,req_headers=headers,ca_file=cert)

    def OpenProfile(self,card):
        if not "publicidad" in card.id:
            import json
            import certifi
            cert = certifi.where()
            headers = {'Content-type': 'application/json', 'Accept': 'text/json'}
            body = json.dumps({"ID":card.id})
            self.working = True
            self.SearchProfilesRquest = UrlRequest("https://fgpresentaciones.com/get_profile_packs",
                                     on_success=lambda x,y : self.sm.ProfilePacksScreen.UpdateProfiles(self.sm,x,y,True),
                                    req_body=body,req_headers=headers,ca_file=cert)

    def AvaiblePacks(self,instance):
        if not self.parent.MainScreen.ids.NavDrawer.CurrentUser:
            self.sm.current = "MainScreen"
            return
        import json
        import certifi
        Username = self.parent.MainScreen.ids.NavDrawer.CurrentUser["Username"]
        cert = certifi.where()
        headers = {'Content-type': 'application/json', 'Accept': 'text/json'}
        body = json.dumps({"Username":Username})
        self.working = True
        self.AvaiblePacksReq = UrlRequest("https://fgpresentaciones.com/get_avaible_packs",
                                 on_success=lambda x,y : self.sm.ProfilePacksScreen.UpdateProfiles(self.sm,x,y,True),
                                req_body=body,req_headers=headers,ca_file=cert)

    def UpdateProfiles(self,sm,req,res, packs=False):
        if not res:
            self.working = False
            # if packs:
            #     sm.MainScreen.ids.NavDrawer.working = False
            return Snackbar(text="No encontramos perfiles vulve a intentarlo.").show()
        self.sm = sm
        self.ids.ProfilesScrollView.clear_widgets()
        self.ProfilesScrollGrid = MDGridLayout()
        self.ProfilesScrollGrid.id = "ProfilesScrollGrid"
        self.ProfilesScrollGrid.padding = (10,10,10,10)
        self.ProfilesScrollGrid.spacing = 10
        self.ProfilesScrollGrid.cols = 2
        self.ProfilesScrollGrid.size_hint_y = None

        for profile in res:
            height = Window.height / 3.5
            self.Profiles[profile["ID"]] = ProfilesCard(id= profile["ID"],orientation= "vertical",size_hint= (".6", None),height=height,padding=(0,0,0,0))
            self.Boxes[profile["ID"]] = RoundedCardBox(id="box%s" % profile["ID"], size_hint_y=None, height=height,padding=(0,0,0,0),size=self.Profiles[profile["ID"]].size, orientation="vertical")
            self.Images[profile["ID"]] = AsyncImg(id="img%s" % profile["ID"],source="http://fgpresentaciones.com/images/%s" % profile["ProfileImage"],size=self.Profiles[profile["ID"]].size)
            self.ProfileDescription[profile["ID"]] = profile["Descripcion"]
            self.Boxes[profile["ID"]].add_widget(self.Images[profile["ID"]])
            self.Panels[profile["ID"]] = custom_one_list(id=profile["Nombre"],text=profile["Nombre"])#,bg_color= [120,120,120])
            self.Boxes[profile["ID"]].add_widget(self.Panels[profile["ID"]])
            self.Profiles[profile["ID"]].add_widget(self.Boxes[profile["ID"]])
            self.ProfilesScrollGrid.add_widget(self.Profiles[profile["ID"]])
            if hasattr(profile,"facebook"):
                self.Networks[profile["ID"]] = {
                    "facebook" : profile["Facebook"],
                    "instagram" : profile["Instagram"],
                    "whatsapp" : profile["Telefono"],
                    "twitter" : profile["Twitter"],
                }

        import math
        self.ids.ProfilesScrollView.add_widget(self.ProfilesScrollGrid)
        self.ProfilesScrollGrid.height = height * math.ceil(len(res)/2) + 10 * math.ceil(len(res)/2) + 10 

        if packs:
            self.sm.current = "PacksScreen"
        else:
            self.sm.current = "ProfilesScreen"

        self.sm.MainScreen.working = False
        self.working = False




class ProfilePacksScreen(ProfilesScreen):

    AnonimousPack = DictProperty()

    def __init__(self,**kwargs):
        super(ProfilePacksScreen,self).__init__(**kwargs)
        self.ids.ProfilesScreenGrid.remove_widget(self.ids.ProfilesBottomNavigation)
        self.ids.ProfilesToolbar.title = "Packs disponibles"

    def UpdateProfiles(self,sm,req,res, packs=False):
        if not res:
            sm.PacksScreen.working = False
            # if packs:
            #     sm.MainScreen.ids.NavDrawer.working = False
            return Snackbar(text="No hay ningun pack disponible.").show()
        self.sm = sm
        self.ids.ProfilesScrollView.clear_widgets()
        self.ProfilesScrollGrid = MDGridLayout()
        self.ProfilesScrollGrid.id = "ProfilesScrollGrid"
        self.ProfilesScrollGrid.padding = (10,10,10,10)
        self.ProfilesScrollGrid.spacing = 10
        self.ProfilesScrollGrid.cols = 2
        self.ProfilesScrollGrid.size_hint_y = None

        for profile in res:

            height = Window.height / 3.5
            self.Profiles[profile["ID"]] = ProfilesCard(id= profile["ID"],orientation= "vertical",size_hint= (".6", None),height=height,padding=(0,0,0,0))
            self.Boxes[profile["ID"]] = RoundedCardBox(id="box%s" % profile["ID"], size_hint_y=None, height=height,padding=(0,0,0,0),size=self.Profiles[profile["ID"]].size, orientation="vertical")
            self.Images[profile["ID"]] = AsyncImg(id="img%s" % profile["ID"],source="http://fgpresentaciones.com/images/%s" % profile["ProfileImage"],size=self.Profiles[profile["ID"]].size)
            self.ProfileDescription[profile["ID"]] = profile["Descripcion"]
            self.Boxes[profile["ID"]].add_widget(self.Images[profile["ID"]])
            self.Panels[profile["ID"]] = custom_one_list(id=profile["Nombre"],text=profile["Nombre"])#,bg_color= [120,120,120])
            self.Boxes[profile["ID"]].add_widget(self.Panels[profile["ID"]])
            self.Profiles[profile["ID"]].add_widget(self.Boxes[profile["ID"]])
            self.ProfilesScrollGrid.add_widget(self.Profiles[profile["ID"]])
            self.AnonimousPack[profile["ID"]] = profile["Anonimo"]
            # self.Networks[profile["ID"]] = {
            #     "facebook" : profile["Facebook"],
            #     "instagram" : profile["Instagram"],
            #     "whatsapp" : profile["Telefono"],
            #     "twitter" : profile["Twitter"],
            # }

        import math
        self.ids.ProfilesScrollView.add_widget(self.ProfilesScrollGrid)
        self.ProfilesScrollGrid.height = height * math.ceil(len(res)/2) + 10 * math.ceil(len(res)/2) + 10 

        if packs:
            self.sm.current = "ProfilePacksScreen"
        
        self.sm.PacksScreen.working = False

    def GoBack(self):
        self.parent.current = "PacksScreen"

    def OpenProfile(self,card):
        if self.AnonimousPack[card.id]:
            content = AnonimousForm(packname=self.Panels[card.id].text,usermail=self.parent.MainScreen.ids.NavDrawer.CurrentUser["Email"])
            self.MailForm = MDDialog(
                auto_dismiss=False,
                title="[color=f54242]La venta de este pack se realiza de forma anonima, por lo que enviaremos un mail para que el vendedor se ponga en contacto![/color]",
                type="custom",
                content_cls = content,
                buttons=[
                    SendForm(
                        text="Cerrar", on_release=lambda x: self.MailForm.dismiss()
                    ),
                    SendForm(
                        text="Enviar", on_release=lambda x: self.SendMailForm(x,card.id,content)
                    ),

                ],
            )
            self.MailForm.open()

    def SendMailForm(self,x,person,content):
        import json
        import certifi
        cert = certifi.where()
        headers = {'Content-type': 'application/json', 'Accept': 'text/json'}
        body = json.dumps({"ID":person, "Email":content.ids.useremail.text, "Mensaje":content.ids.message.text})
        self.working = True
        self.SearchProfilesRquest = UrlRequest("https://fgpresentaciones.com/send_email",
                                 on_success=lambda x,y: self.GetEmailFormResult(x,y),
                                req_body=body,req_headers=headers,ca_file=cert)

    def GetEmailFormResult(self,x,y):
        self.working=False
        self.MailForm.dismiss()
        return Snackbar(text="Mensaje enviado correctamente!", duration=2).show()