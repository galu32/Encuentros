from Libs import *

class custom_description_label(MDLabel):
    pass

class AsyncImg(AsyncImage):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

def CreateProfileKV():

    profile_kv = """

<ProfileScreen>:
    id : ProfileScreen
    name : "ProfileScreen"

    p : Profile.__self__
    desc1 : desc1.__self__
    # desc2 : desc2.__self__
    imagegallery : ImageGalleryGrid.__self__
    galleryscroll : ImageGalleryScroll.__self__
    gallery : ImageGallery.__self__

    MDGridLayout:
        id : ProfileGrid
        orientation : "vertical"
        cols : 1
        spacing : 5

        MDToolbar:
            id : ProfileToolbar
            post_hint : {"top" : 1}
            left_action_items : [['account-arrow-left-outline', lambda x : root.GoBack()]]

        MDGridLayout:
            cols : 1
            id: container
            padding : 0,0,0,0
            spacing : 0

            MDGridLayout:
                id : Profile
                orientation : "vertical"
                spacing : 10
                padding : 15,15,15,15
                cols : 2

            MDGridLayout:
                id : SocialNetwork
                cols:2
                rows:2
                size_hint : None,None
                width : Window.width
                orientation : "horizontal"
                padding : 20,15,30,10
                spacing: 15

                MDChip:
                    id : facebookchip
                    label: 'Facebook'
                    icon: 'facebook'
                    color : rgba("#f54242")
                    pos_hint : {"center_x": .5, "center_y": .5}
                    callback: root.OpenNetwork
                
                MDChip:
                    color : rgba("#f54242")
                    label: 'Instagram'
                    icon: 'instagram'
                    pos_hint : {"center_x": .5, "center_y": .5}
                    callback: root.OpenNetwork
                
                MDChip:
                    color : rgba("#f54242")
                    label: 'Twitter     '
                    icon: 'twitter'
                    pos_hint : {"center_x": .5, "center_y": .5}
                    callback: root.OpenNetwork
                
                MDChip:
                    color : rgba("#f54242")
                    label: 'WhatsApp'
                    icon: 'whatsapp'
                    pos_hint : {"center_x": .5, "center_y": .5}
                    callback: root.OpenNetwork

            MDLabel:
                size_hint: 1, None
                height : self.texture_size[1] + facebookchip.height

            custom_description_label
                id : desc1
                text : ""
                padding:15,15
                text_size: self.width, None
                size_hint: 1, None
                height: self.texture_size[1]
            MDLabel:
                size_hint: 1, None
                height : self.texture_size[1] + facebookchip.height
            # custom_description_label:
            #     id : desc2
            #     text : ""

            MDBoxLayout:
                id : ImageGallery
                orientation : "horizontal"

                ScrollView:
                    id : ImageGalleryScroll
                    orientation : "horizontal"
                    size_hint_x : None
                    width : Window.width

                    MDGridLayout:
                        id : ImageGalleryGrid
                        spacing : 10
                        pading : 10,10,10,10
                        cols : 50
                        do_scroll_x : True
                        size_hint_x : None

"""
    return profile_kv

class ModalCard(MDCard):
    callback = ObjectProperty()
    def __init__(self,**kwargs):
        super(ModalCard,self).__init__(**kwargs)    
        # self.on_release : lambda self : 
    def on_release(self,**k):
        self.callback(self)

class ProfileScreen(Screen):

    profile = DictProperty()

    cardgallery = ListProperty()

    callback = ObjectProperty()

    # ImageModal = ObjectProperty()

    current_profilecard = ObjectProperty()

    def __init__(self,**kwargs):
        super(ProfileScreen,self).__init__(**kwargs)

    def on_profile(self,x,y):
        if self.profile:

            self.Networks = {}
            for Network in self.profile:
                if Network in ["Facebook","Instagram","WhatsApp","Twitter     "]:
                    self.Networks[Network] = self.profile[Network]

            self.ids.ProfileToolbar.title = self.profile["name"]
            self.CreateProfileImage()
            self.CreateProfileDesc()
            self.CreteImageGallery()
            self.callback()

    def CreateProfileImage(self):
        self.p.clear_widgets()
        card = self.profile["card"]
        c = MDCard()
        c.on_release = lambda : self.OpenModal(c)
        c.id = card.id
        c.orientation = card.orientation
        c.size_hint = (".6", ".6")
        c.height = card.height
        c.padding = card.padding

        box = BoxLayout(
            id = card.children[0].id,
            height = card.children[0].height,
            padding = card.children[0].padding,
            size = card.children[0].size,
            orientation = card.children[0].orientation,
            )

        img = AsyncImg(
            source=card.children[0].children[1].source,
            size = card.children[0].children[1].size,
            nocache = True
            )
        box.add_widget(img)
        c.add_widget(box)
        self.p.add_widget(c)
        self.p.add_widget(Image(source="images/premium.png",size=c.size,
                        allow_stretch = True,
            keep_ratio = False))

        self.current_profilecard = c.__self__

    def CreateProfileDesc(self):
        self.desc1.text = self.profile["desc"]
        # self.desc2.text = self.profile["desc"]

    def CreteImageGallery(self):
        self.imagegallery.clear_widgets()

        for a in self.cardgallery:

            height = Window.height / 5
            width = Window.width / 3.5
            card = ModalCard(id=a,orientation= "vertical",size_hint=(None,None),width=width,height= height,padding=(0,0,0,0))
            card.callback = lambda card : self.OpenModal(card)
            box = BoxLayout(size_hint_y=None, height=height,padding=(0,0,0,0),size=card.size, orientation="vertical")
            img = AsyncImg(id=a,source="http://fgpresentaciones.com/images/%s" % a,size=card.size)
            box.add_widget(img)
            card.add_widget(box)

            self.imagegallery.add_widget(card)

        self.imagegallery.width = card.width * len(self.cardgallery)

    def GoBack(self):
        if self.profile["Main"]:
            self.parent.current = "MainScreen"
        else:
            self.parent.current = "ProfilesScreen"
        if hasattr(self,"CardModal"):
            self.ids.ProfileGrid.remove_widget(self.CardModal)
            self.ids.ProfileToolbar.right_action_items.pop()                
            del self.CardModal

    def OpenModal(self,c):
        source = c.children[0].children[0].source
        self.ImageModal = AsyncImage(source=source)
        self.ImageModal.id = "ImageModal"
        self.ImageModal.size_hint = (None,None)
        self.ImageModal.keep_ratio = False
        self.ImageModal.allow_stretch = True
        self.ImageModal.size = self.ids.ProfileGrid.size
        self.CardModal = MDCard(size_hint=(None,None), size=self.ids.ProfileGrid.size)
        self.CardModal.add_widget(self.ImageModal)
        self.ids.ProfileGrid.add_widget(self.CardModal)
        self.ids.ProfileToolbar.right_action_items.append(["close", lambda x: self.CloseModal(x)])

    def CloseModal(self,x):
        self.ids.ProfileToolbar.right_action_items.pop()
        self.ids.ProfileGrid.remove_widget(self.CardModal)
        del self.CardModal

    def OpenNetwork(self,instance,label):
        if not self.Networks[label]:
            webbrowser.open("https://google.com/")
        else:
            webbrowser.open(self.Networks[label])