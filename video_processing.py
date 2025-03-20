import cv2
import time
from ocr import encontrarRoiPlaca, preProcessamentoRoiPlaca, ocrImageRoiPlaca
from api import check_and_register_occurrence, get_occurrences
from config import occurrences_list

def process_video():
    # Captura o vídeo da webcam (índice 0)
    cap = cv2.VideoCapture(0)
    last_check_time = time.time()
    detected_plate = ""

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar frame da webcam.")
            break

        frame, roi = encontrarRoiPlaca(frame)
        cv2.imshow("Detecção de Placa", frame)

        if roi is not None:
            # Salva a ROI para ser processada
            cv2.imwrite("output/roi.png", roi)
            preProcessamentoRoiPlaca()
            ocr_result = ocrImageRoiPlaca()
            if ocr_result:
                print("Placa detectada:", ocr_result)
                detected_plate = ocr_result
                # Verifica se a placa detectada corresponde a uma ocorrência existente
                if any(o.get("placa", "").upper() == detected_plate.upper() for o in occurrences_list):
                    print(f"Placa {detected_plate} corresponde a uma ocorrência existente. Registrando...")
                    check_and_register_occurrence(detected_plate)

        # Atualiza a lista de ocorrências a cada 60 segundos
        if time.time() - last_check_time >= 60:
            last_check_time = time.time()
            get_occurrences()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
