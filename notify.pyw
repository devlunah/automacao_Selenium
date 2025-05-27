
from winotify import Notification, audio

toast = Notification(app_id="SUAP",
                     title="Novo chamado detectado!",
                     msg="Verifique o SUAP agora.")  
toast.set_audio(audio.Default, loop=False)
toast.show()
