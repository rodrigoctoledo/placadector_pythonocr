import threading
import time
from ui import login_window, main_menu
from video_processing import process_video
from api import get_occurrences

def periodic_occurrence_update():
    while True:
        get_occurrences()
        time.sleep(60)

if __name__ == "__main__":
    # Realiza o login via interface
    login_window()

    # Inicia uma thread para atualizar a lista de ocorrências a cada 1 minuto
    occurrence_thread = threading.Thread(target=periodic_occurrence_update, daemon=True)
    occurrence_thread.start()

    # Inicia o processamento do vídeo em uma thread separada
    video_thread = threading.Thread(target=process_video, daemon=True)
    video_thread.start()

    # Abre o menu principal
    main_menu()
