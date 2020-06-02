from Libs import *

def CreateMainKV():
    page_kv = """

<_Triangle>:
    canvas:
        Color:
            rgba: rgba("#f54242")
        Triangle:
            points:
                [ \
                self.right-14, self.y+7, \
                self.right-7, self.y+7, \
                self.right-7, self.y+14 \
                ]

<-SearchFiltersDropDown>:
    # size_hint:  ".6", None
    position: "center"
    orientation: "vertical"
    # adaptive_size: True
    spacing: "5dp"
    padding: "5dp", "5dp", "5dp", 0

    MDBoxLayout:
        adaptive_size: True
        spacing: "10dp"

        Label:
            id: label_item
            size_hint: None, None
            size: self.texture_size
            color: rgba("#f54242")
            font_size: root.font_size

        _Triangle:
            size_hint: None, None
            size: "20dp", "20dp"

    MDSeparator:

<MainScreen>:

    id : MainScreen
    name : "MainScreen"

    MDGridLayout:
        id : MainGrid
        orientation : "vertical"
        cols : 1

        MDToolbar:
            id : MainToolbar
            pos_hint: {"top" : 1}
            left_action_items : [['fire', lambda x : NavDrawer.set_state("open")]]
            title : "Encuentros"

        MDBoxLayout:
            id : MainTitlesBox
            orientation : "vertical"
            # spacing : 10
            spaing : 0
            padding : 0,0,0,0
            # padding: 10,10,10,10

            # MDLabel:
            #     id : MainTitle
            #     padding : 0,0
            #     theme_text_color: "Custom"
            #     text_color: rgba("#f54242")
            #     text : "Encuentros"
            #     halign : "center"
            #     font_style : "H2"

            MDLabel:
                id : MainSubt
                text : "Personas que buscan lo mismo que vos..."
                padding: 0,0
                theme_text_color: "Custom"
                text_color: rgba("#f54242")
                halign : "center"
                font_style : "H4"
                # size_hint : 1, None

        MDGridLayout:
            id : FiltersBox
            orientation : "vertical"
            cols : 2
            spacing : 5
            size_hint_y : .6
            padding :10,5

            SearchFiltersDropDown:
                id : province_dropmenu
                text : "Provincia"
                # on_release : root.province_menu.open()
                on_release : root.NoDisponible()

            SearchFiltersDropDown:
                id : zone_dropmenu
                text : "Zona"
                # on_release : root.zone_menu.open()
                on_release : root.NoDisponible()

            SearchFiltersDropDown:
                id : locality_dropmenu
                text : "Localidad"
                # on_release : root.locality_menu.open()
                on_release : root.NoDisponible()

            SearchFiltersDropDown:
                id : locality_dropmenu
                text : "Genero"
                # on_release : root.gender._menu.open()
                on_release : root.NoDisponible()

            MDLabel:
            MDLabel:
            # MDLabel:

            MDRaisedButton:
                text : "¡Buscar sin filtros!"
                padding: 10,10,10,10
                size_hint : locality_dropmenu.size_hint
                # size : locality_dropmenu.size
                on_release : root.CreateProfiles(True)

            MDRaisedButton:
                text : "¡Buscar!"
                padding: 10,10,10,10
                size_hint : locality_dropmenu.size_hint
                # size : locality_dropmenu.size
                # on_release : root.CreateProfiles()
                on_release : root.NoDisponible()

        MDBoxLayout:
            id : MainProfilesBox
            padding : 10,10,10,10
            spacing : 10

            # id : SearchButton
            # icon : "comment-search"
            # size_hint : .5,.5
            # user_font_size : "64sp"
            # theme_text_color : "Custom"
            # text_color: rgba("#f54242")
            # # on_release : root.CreateProfiles()

        MDBottomNavigation:
            id : MainBottom
            size_hint_y : None
            panel_color : 0.9607843137254902, 0.25882352941176473, 0.25882352941176473, 1
            
            MDBottomNavigationItem:
                id : MainSusc
                name : "Suscribirse"
                text : "Suscribirse"
                icon : ""

    NavDrawer:
        id : NavDrawer
"""
    return page_kv

class SearchFiltersDropDown(MDDropDownItem):
    pass

class custom_one_list(OneLineListItem):
    pass

class AsyncImg(AsyncImage):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

class MainScreen(CustomScreen):
    

    started = BooleanProperty(defaultvalue = False)
    callback = ObjectProperty(lambda : None)
    sm = ObjectProperty()

    def __init__(self,**kwargs):
        super(MainScreen,self).__init__(**kwargs)
        self.SendFiltersRequest()

    def SendFiltersRequest(self):    
        import certifi
        import json
        cert = certifi.where()
        body = json.dumps({"asd":"asd"})
        headers = {'Content-type': 'application/json', 'Accept': 'text/json'}
        # self.GetFilters = UrlRequest("https://fgpresentaciones.com/update_filters", 
        self.GetFilters = UrlRequest("https://fgpresentaciones.com/get_main_profiles", 
        on_success=self.CreateMainProfiles,
        on_failure=self.FailedRequest,
        on_error=self.FailedRequest,
        req_body=body,
        req_headers=headers,
        ca_file=cert)

    def CreateMainProfiles(self,req,res):

        for profile in res:
            height = Window.height / 3.5
            self.sm.ProfilesScreen.Profiles[profile["ID"]] = MDCard(on_release=lambda x : self.OpenProfile(x),id= profile["ID"],orientation= "vertical",size_hint= (".6", None),height=height,padding=(0,0,0,0))
            # self.sm.ProfilesScreen.Profiles[profile["ID"]].on_release = lambda  : print(self.sm.ProfilesScreen.Profiles[profile["ID"]].id)
            self.sm.ProfilesScreen.Boxes[profile["ID"]] = MDBoxLayout(id="box%s" % profile["ID"], size_hint_y=None, height=height,padding=(0,0,0,0),size=self.sm.ProfilesScreen.Profiles[profile["ID"]].size, orientation="vertical")
            self.sm.ProfilesScreen.Images[profile["ID"]] = AsyncImg(id="img%s" % profile["ID"],source="http://fgpresentaciones.com/images/%s" % profile["ProfileImage"],size=self.sm.ProfilesScreen.Profiles[profile["ID"]].size)
            self.sm.ProfilesScreen.ProfileDescription[profile["ID"]] = profile["Descripcion"]
            self.sm.ProfilesScreen.Boxes[profile["ID"]].add_widget(self.sm.ProfilesScreen.Images[profile["ID"]])
            self.sm.ProfilesScreen.Panels[profile["ID"]] = custom_one_list(id=profile["Nombre"],text=profile["Nombre"])#,bg_color= [120,120,120])
            self.sm.ProfilesScreen.Boxes[profile["ID"]].add_widget(self.sm.ProfilesScreen.Panels[profile["ID"]])
            self.sm.ProfilesScreen.Profiles[profile["ID"]].add_widget(self.sm.ProfilesScreen.Boxes[profile["ID"]])
            self.ids.MainProfilesBox.add_widget(self.sm.ProfilesScreen.Profiles[profile["ID"]])
            self.sm.ProfilesScreen.Networks[profile["ID"]] = {
                "facebook" : profile["Facebook"],
                "instagram" : profile["Instagram"],
                "whatsapp" : profile["Telefono"],
                "twitter" : profile["Twitter"],
            }

        self.started = True 
        print("go")       

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
            "desc" : self.sm.ProfilesScreen.ProfileDescription[card.id],
            "card" : self.sm.ProfilesScreen.Profiles[card.id],
            "box" : self.sm.ProfilesScreen.Boxes[card.id],
            "img" : self.sm.ProfilesScreen.Images[card.id],
            "name" : self.sm.ProfilesScreen.Panels[card.id].text,
            "Facebook" : self.sm.ProfilesScreen.Networks[card.id]["facebook"],
            "Instagram" : self.sm.ProfilesScreen.Networks[card.id]["instagram"],
            "WhatsApp" : self.sm.ProfilesScreen.Networks[card.id]["whatsapp"],
            "Twitter     " : self.sm.ProfilesScreen.Networks[card.id]["twitter"],
            "Main" : True
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
        # self.sm.ProfileScreen.GoBack = self.SwitchBack
        self.working = False


    def CrateFiltersMenu(self,req,res):
        # provincias = [{"text": f"{i}"} for i in res["Provincia"]]
        # zonas = [{"text": f"{i}"} for i in res["Zona"]]
        # localidades = [{"text": f"{i}"} for i in res["Localidad"]]
        # generos = [{"text": f"{i}"} for i in ["Mujer", "Hombres", "Trans"]]

        # self.province_menu = MDDropdownMenu(
        #     caller=self.ids.province_dropmenu,
        #     items=provincias,
        #     position="bottom",
        #     callback=lambda x: self.SetFilterItem(x,"province_dropmenu"),
        #     width_mult=4,

        # )
        # self.zone_menu = MDDropdownMenu(
        #     id="zone",
        #     caller=self.ids.zone_dropmenu,
        #     items=zonas,
        #     position="bottom",
        #     callback=lambda x:self.SetFilterItem(x,"zone_dropmenu"),
        #     width_mult=4,
        # )
        # self.locality_menu = MDDropdownMenu(
        #     id="locality",
        #     caller=self.ids.locality_dropmenu,
        #     items=localidades,
        #     position="bottom",
        #     callback=lambda x:self.SetFilterItem(x,"locality_dropmenu"),
        #     width_mult=4,
        # )
        # self.gender_menu = MDDropdownMenu(
        #     id="genre",
        #     caller=self.ids.gender_dropmenu,
        #     items=generos,
        #     position="bottom",
        #     callback=lambda x:self.SetFilterItem(x,"gender_dropmenu"),
        #     width_mult=4,
        # )

        self.started = True 
        print("go")

    def SetFilterItem(self, instance, dropmenu):
        getattr(self.ids, dropmenu).set_item(instance.text)
        getattr(self,dropmenu.split("_")[0]+"_menu").dismiss()


    def CreateProfiles(self,Todo=False):
        if Todo:
            filters = {"Provincia" : "Todo", "Genero" : "Mujer"}
        else:
            filters = self.GetFiltersSearch()
        import json
        import certifi
        cert = certifi.where()
        headers = {'Content-type': 'application/json', 'Accept': 'text/json'}
        body = json.dumps(filters)
        if filters:
            self.working = True
            self.SearchProfilesRquest = UrlRequest("https://fgpresentaciones.com/get_profiles",
                                     on_success=lambda x,y : self.parent.ProfilesScreen.UpdateProfiles(self.parent,x,y),
                                    req_body=body,req_headers=headers,ca_file=cert,on_failure=self.ErrorRequest,on_error=self.ErrorRequest)

    def GetFiltersSearch(self,genderchange=False):
        filters = {}
        for menu in self.ids.FiltersBox.children:
            if hasattr(menu,"current_item"):
                if not menu.current_item:
                    if genderchange:
                        return False
                    return Snackbar(text="Debe especificar todos los filtros",duration=2).show()
                filters[menu.text] = menu.current_item
        filters["Genero"] = "Mujer"
        return filters

    def on_started(self, instance, value):
        self.callback(True)

    def FailedRequest(self,x,y):
        self.callback(False)

    def NoDisponible(self):
        Snackbar(text="La bsqueda por filtros no esta disponible aun!").show()
