import cv2
import pytesseract
import os
import re

# Mapeamento ambíguo para substituição de caracteres confusos
ambiguous_mapping = {
    'Q': ['O'],
    'O': ['Q', '0', 'D'],
    '0': ['O', 'D'],
    'D': ['O', '0'],
    'I': ['1', 'L'],
    '1': ['I', 'L'],
    'L': ['I', '1'],
    'Z': ['2'],
    '2': ['Z'],
    'S': ['5'],
    '5': ['S'],
    'E': ['3'],
    '3': ['E'],
    'G': ['6', '9', 'C'],
    '6': ['G', '9', 'C'],
    '9': ['G', '6'],
    'C': ['G', '6', '9'],
    'B': ['8'],
    '8': ['B'],
    'T': ['7'],
    '7': ['T'],
    'A': ['4'],
    '4': ['A'],
    'U': ['V'],
    'V': ['U'],
    'M': ['N'],
    'N': ['M'],
    'P': ['R'],
    'R': ['P']
}

def gerar_variantes(texto, mapping):
    """
    Gera todas as variações possíveis do texto usando o mapeamento ambíguo.
    """
    variantes = [""]
    for char in texto:
        novas_variantes = []
        if char in mapping:
            for var in variantes:
                # Adiciona o caractere original
                novas_variantes.append(var + char)
                # Adiciona as variações alternativas
                for alt in mapping[char]:
                    novas_variantes.append(var + alt)
        else:
            for var in variantes:
                novas_variantes.append(var + char)
        variantes = novas_variantes
    return list(set(variantes))

def checar_variantes_placa(texto_basico):
    """
    Gera variações a partir do texto extraído e verifica quais batem com os padrões:
      - Antigo: LLLNNNN (ex: ABC1234)
      - Mercosul: LLLNLNN (ex: ABC1D23)
    Retorna uma lista com todas as placas válidas encontradas.
    """
    variantes = gerar_variantes(texto_basico, ambiguous_mapping)
    validas = []
    # Regex que aceita tanto o padrão antigo quanto o novo (Mercosul)
    padrao = r'^([A-Z]{3}[0-9]{4}|[A-Z]{3}[0-9][A-Z][0-9]{2})$'
    for var in variantes:
        if re.fullmatch(padrao, var):
            validas.append(var)
    return validas

def encontrarRoiPlaca(frame):
    """
    Detecta a região de interesse (ROI) da placa no frame utilizando threshold e contornos.
    Desenha um retângulo na ROI e a salva na pasta output.
    """
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(cinza, 90, 255, cv2.THRESH_BINARY)
    desfoque = cv2.GaussianBlur(bin_img, (5, 5), 0)

    contornos, _ = cv2.findContours(desfoque, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for c in contornos:
        perimetro = cv2.arcLength(c, True)
        if perimetro > 120:
            aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True)
            if len(aprox) == 4:
                x, y, lar, alt = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + lar, y + alt), (0, 255, 0), 2)
                roi = frame[y:y + alt, x:x + lar]
                if not os.path.exists("output"):
                    os.makedirs("output")
                cv2.imwrite("output/roi.png", roi)
                return frame, roi
    return frame, None

def preProcessamentoRoiPlaca():
    """
    Processa a imagem ROI salva em "output/roi.png":
      - Redimensiona para aumentar a resolução.
      - Converte para cinza, aplica threshold e desfoque.
      - Salva o resultado em "output/roi-ocr.png".
    """
    if not os.path.exists("output/roi.png"):
        print("Imagem ROI não encontrada.")
        return None

    img_roi = cv2.imread("output/roi.png")
    resize_img_roi = cv2.resize(img_roi, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("output/roi-resized.png", resize_img_roi)

    img_cinza = cv2.cvtColor(resize_img_roi, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("output/roi-gray.png", img_cinza)

    _, img_binary = cv2.threshold(img_cinza, 70, 255, cv2.THRESH_BINARY)
    cv2.imwrite("output/roi-binary.png", img_binary)

    img_desfoque = cv2.GaussianBlur(img_binary, (5, 5), 0)
    cv2.imwrite("output/roi-ocr.png", img_desfoque)

    return img_desfoque

def ocrImageRoiPlaca():
    """
    Executa o OCR na imagem pré-processada (output/roi-ocr.png), limpa o texto extraído,
    aplica a verificação de variantes e retorna a placa válida, se houver.
    """
    image = cv2.imread("output/roi-ocr.png")
    if image is None:
        print("Imagem para OCR não encontrada.")
        return ""
    config_str = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'
    saida = pytesseract.image_to_string(image, lang='eng', config=config_str)
    texto_basico = ''.join(filter(str.isalnum, saida)).upper().strip()
    placas_validas = checar_variantes_placa(texto_basico)
    if placas_validas:
        return placas_validas[0]
    else:
        print("Nenhuma variação válida encontrada no OCR.")
        return ""
