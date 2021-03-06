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
            title : "¡Publicita en Encuentros!"

        MDGridLayout:
            id: formgrid
            orientation : "vertical"
            cols : 1
            padding : 10,10,10,10
            spacing : 5
            
            # MDLabel:
            #     text: "¡Publicita en Encuentros!"
            #     theme_text_color: "Custom"
            #     text_color: rgba("#f54242")
            #     padding: 0,0
            #     halign: "center"
            #     font_style: "H2"

            MDLabel:
                text: "Recorda que debes ser mayor de 18 años y deberas validar tu identidad por cuestiones de seguridad."
                theme_text_color: "Custom"
                text_color: rgba("#f54242")
                halign: "center"
                font_style: "Subtitle2"


            MDTextField:
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                hint_text: "Nombre.."
                id: Nombre
            
            MDTextField:
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                hint_text: "Apellido.."
                id: Apellido

            MDTextField:
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                hint_text: "Localidad.."
                id: Localidad

            MDTextField:
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                hint_text: "Provincia.."
                id: Provincia

            MDTextField:
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                hint_text: "Genero.."
                id: Genero
            MDTextField:
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                hint_text: "Telefono.."
                id: Telefono
            
            MDTextField:
                id: Codigo
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                hint_text: "Codigo referido (opcional).."

            MDRaisedButton:
                id: SendAnnouncerForm
                on_release: root.SendForm({Nombre,Apellido,Localidad,Provincia,Genero,Telefono,Codigo})
                post_hint: {"top": 1 ,"center_x": .5, "center_y": .5}
                text: "Enviar"
    """
    return announce_kv

class AnnounceScreen(CustomScreen):

    def GoBack(self):
        self.parent.current = "MainScreen"

    def SendForm(self,fields):
        form = {}
        for f in fields:
            if not f.text and not "Codigo" in f.hint_text:
                return Snackbar(text="Se debe completar todos los campos.").show()
            if "Codigo" in f.hint_text:
                form["Codigo"] = f.text
            else:
                form[f.hint_text[:-2]] = f.text
        self.working = True
        import json
        import certifi
        cert = certifi.where()
        headers = {'Content-type': 'application/json', 'Accept': 'text/json'}
        form["Email"] = self.parent.MainScreen.ids.NavDrawer.CurrentUser["Email"]
        body = json.dumps(form)
        self.SendFormRequest = UrlRequest("https://fgpresentaciones.com/new_suscription",
                                 on_success=lambda x,y : self.GetSuscriptionResponse(x,y),
                                req_body=body,req_headers=headers,ca_file=cert,
                                on_failure=self.ErrorRequest,on_error=self.ErrorRequest)

    def GetSuscriptionResponse(self,req,res):
        self.working = False
        if res["affectedRows"]:
            return Snackbar(text="Recibiras un mail para completar tu registro",duration=2).show()
        else:
            return self.ErrorRequest()

