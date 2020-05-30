from Libs import *


class CreateManager(ScreenManager):

    def __init__(self,**kwargs):
        super(CreateManager,self).__init__(**kwargs)
        self.transition=NoTransition()
        self.id = "ScreenManager"
        Window.bind(on_keyboard=self.PhoneBack)

    def PhoneBack(self,window,key,*k):
        if key == 27:
            if self.current == "MainScreen":
                return True
            if self.current == "ProfilesScreen":
                self.current = "MainScreen"
            if self.current == "ProfileScreen":
                if hasattr(self.ProfileScreen, "CardModal"):
                    self.ProfileScreen.CloseModal(self)
                    return True
                self.ProfileScreen.GoBack()
            if self.current == "PacksScreen":
                self.current = "MainScreen"
            if self.current == "ProfilePacksScreen":
                self.current = "PacksScreen"
            return True
