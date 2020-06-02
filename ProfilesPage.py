from Libs import * 

def CreateProfilesKV():
    profiles_kv = """

<ProfilesCard@MDCard>:
    on_release : self.parent.parent.parent.parent.parent.OpenProfile(self)

<custom_one_list@OneLineListItem>:
    bg_color: rgba("#f54242")
    text_color: rgba("#ffffff")
    theme_text_color: "Custom"

<ProfilesScreen>:
    id : ProfilesScreen
    name : "ProfilesScreen"

    MDGridLayout:
        id : ProfilesScreenGrid
        orientation : "vertical"
        cols : 1

        MDToolbar:
            id : ProfilesToolbar
            title : "Encuentros"
            pos_hint : {"top" : 1}
            left_action_items : [['account-arrow-left-outline', lambda x : root.GoBack()]]

        MDBoxLayout:
            id : ProfilesBox
            orientation : "vertical"

            ScrollView:
                id : ProfilesScrollView


        MDBottomNavigation:
            id : ProfilesBottomNavigation
            size_hint : None, None
            panel_color: 0.9607843137254902, 0.25882352941176473, 0.25882352941176473, 1
            width : Window.width

            BottomItem:
                id : female
                name : "Mujer"
                text : "Mujeres"
                icon : "gender-female"

            BottomItem:
                id : male
                name : "Hombres"
                text : "Hombres"
                icon : "gender-male"

            BottomItem:
                id : "trans"
                name : "Trans"
                text : "Trans"
                icon : "gender-transgender"

"""
    return profiles_kv

class BottomItem(MDBottomNavigationItem):
    header = ObjectProperty()
    
    def __init__(self,**k):
        super().__init__(**k)

    def on_leave(self, *args):
        pass

    def on_tab_press(self):
        par = self.parent_widget
        # par.ids.tab_manager.current = self.name
        if par.previous_tab is not self:
            Animation(_label_font_size=sp(12), d=0.1).start(
                par.previous_tab.header
            )
            Animation(
                _current_color=par.previous_tab.header.theme_cls.disabled_hint_text_color,
                d=0.1,
            ).start(par.previous_tab.header)
        # par.previous_tab.header.active = False
        # self.header.active = True
        par.previous_tab = self
        par.parent.parent.ChangeGender(self.name)

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

class ProfilesScreen(CustomScreen):

    ProfileDescription = DictProperty()
    Profiles = DictProperty()
    Boxes = DictProperty()
    Images = DictProperty()
    Panels = DictProperty()
    Networks = DictProperty()

    def __init__(self,**kwargs):
        super(ProfilesScreen,self).__init__(**kwargs)

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
            if profile["Escort"]:
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

    def GoBack(self):
        self.parent.current = "MainScreen"

    def OpenProfile(self,card):
        if "publicidad" in card.id:
            return
        
        self.working = True

        import json
        import certifi
        cert = certifi.where()
        headers = {'Content-type': 'application/json', 'Accept': 'text/json'}
        body = json.dumps({"ID" : card.id})

        self.sm.ProfileScreen.profile = {}

        self.sm.ProfileScreen.callback = self.ProfileCreated

        d = {
            "desc" : self.ProfileDescription[card.id],
            "card" : self.Profiles[card.id],
            "box" : self.Boxes[card.id],
            "img" : self.Images[card.id],
            "name" : self.Panels[card.id].text,
            "Facebook" : self.Networks[card.id]["facebook"],
            "Instagram" : self.Networks[card.id]["instagram"],
            "WhatsApp" : self.Networks[card.id]["whatsapp"],
            "Twitter     " : self.Networks[card.id]["twitter"],
            "Main" : False
        }

        self.ImageGalleryRequest = UrlRequest("https://fgpresentaciones.com/get_image_gallery",
                                     on_success=lambda x,y : self.GetProfileGallery(x,y,d),
                                    req_body=body,req_headers=headers,ca_file=cert,on_failure=self.ErrorRequest,on_error=self.ErrorRequest)
        

        # self.sm.ProfileScreen.profile = d

    def GetProfileGallery(self,x,res,d):
        l = []
        for a in res: l.append(a.get("Image"))

        self.sm.ProfileScreen.cardgallery = l
        self.sm.ProfileScreen.profile = d      

    def ProfileCreated(self):
        self.sm.current = "ProfileScreen"
        self.working = False

    def ChangeGender(self,gender):
        filters = self.sm.MainScreen.GetFiltersSearch(True)
        if filters :
            filters["Genero"] = gender
        else:
            filters = {"Provincia" : "Todo", "Genero" : gender}
        import json
        import certifi
        cert = certifi.where()
        headers = {'Content-type': 'application/json', 'Accept': 'text/json'}
        body = json.dumps(filters)
        if filters:
            self.working = True
            self.SearchProfilesRquest = UrlRequest("https://fgpresentaciones.com/get_profiles",
                                     on_success=lambda x,y : self.UpdateProfiles(self.sm,x,y),
                                    req_body=body,req_headers=headers,ca_file=cert,on_failure=self.ErrorRequest,on_error=self.ErrorRequest)