from Libs import *

def CreateAnnounceKV():
    announce_kv = """
<AnnounceScreen>:
    id : AnnounceScreen
    name : "AnnounceScreen"

    MDGridLayout:
        cols : 1

        MDToolbar:
            id : AnnounceToolbar
            pos_hint : {"top" : 1}
            left_action_items : [['account-arrow-left-outline', lambda x : root.GoBack()]]

        MDGridLayout:
            orientation : "vertical"
            cols : 1
            padding : 10,10,10,10
            spacing : 5
            
            MDLabel:
                text: "¡Publicita en Encuentros!"
                theme_text_color: "Custom"
                text_color: rgba("#f54242")
                padding: 0,0
                halign: "center"
                font_style: "H2"

            MDLabel:
                text: "Recorda que debes ser mayor de 18 años y deberas validar tu identidad por cuestiones de seguridad."
                theme_text_color: "Custom"
                text_color: rgba("#f54242")
                halign: "center"
                font_style: "Subtitle2"

            MDTextField:
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                hint_text: "Nombre completo.."
            MDTextField:
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                hint_text: "Nombre completo.."
            MDTextField:
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                hint_text: "Nombre completo.."
            MDTextField:
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                hint_text: "Nombre completo.."
            MDTextField:
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                hint_text: "Nombre completo.."
            MDTextField:
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                hint_text: "Nombre completo.."
            MDTextField:
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                hint_text: "Nombre completo.."

            MDRaisedButton:
                id: SendAnnouncerForm
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                text: "Enviar"
    """
    return announce_kv

class AnnounceScreen(CustomScreen):

    def GoBack(self):
        self.parent.current = "MainScreen"