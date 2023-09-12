import PySimpleGUI as sg
from PIL import Image, ExifTags
import io
import os
import webbrowser
import requests

image_atual = None
image_path = None

def resize_image(img):
    img = img.resize((800, 600), Image.Resampling.LANCZOS) 
    return img

def url_download(url):
    global image_atual
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            image_atual = Image.open(io.BytesIO(r.content))
            show_image()
        else:
            sg.popup("Falha ao baixar a imagem. Verifique a URL e tente novamente.")
    except Exception as e:
        sg.popup(f"Erro ao baixar a imagem: {str(e)}")

def show_image():
    global image_atual
    try:
        resized_img = resize_image(image_atual)
        #Converte a image PIL para o formato que o PySimpleGUI
        img_bytes = io.BytesIO() #Permite criar objetos semelhantes a arquivos na memÃ³ria RAM
        resized_img.save(img_bytes, format='PNG')
        window['-IMAGE-'].update(data=img_bytes.getvalue())
    except Exception as e:
        sg.popup(f"Erro ao exibir a imagem: {str(e)}")

def open_image(filename):
    global image_atual
    global image_path
    image_path = filename
    image_atual = Image.open(filename)    
    
    resized_img = resize_image(image_atual)
    #Converte a image PIL para o formato que o PySimpleGUI
    img_bytes = io.BytesIO() #Permite criar objetos semelhantes a arquivos na memÃ³ria RAM
    resized_img.save(img_bytes, format='PNG')
    window['-IMAGE-'].update(data=img_bytes.getvalue())

def save_image(filename):
    global image_atual
    if image_atual:
        with open(filename, 'wb') as file:
            image_atual.save(file)

def exif_data():
    global image_atual
    try:
        if image_atual:
            exif = image_atual._getexif() 
            if exif:
                exif_data = ""
                for tag, value in exif.items():
                    if tag in ExifTags.TAGS:
                        if tag == 37500 or tag == 34853: #Remove os dados customizados (37500) e de GPS (34853)
                            continue
                        tag_name = ExifTags.TAGS[tag]
                        exif_data += f"{tag_name}: {value}\n"
                sg.popup("Dados EXIF:", exif_data)
            else:
                sg.popup("A imagem não possui dados EXIF.")
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao ler dados EXIF: {str(e)}")

def gps_data():
    global image_atual
    try:
        if image_atual:
            exif = image_atual._getexif()
            if exif:
                gps_info = exif.get(34853)  #Tag para informações de GPS
                print (gps_info[1], gps_info[3])
                if gps_info:
                    latitude = int(gps_info[2][0]) + int(gps_info[2][1]) / 60 + int(gps_info[2][2]) / 3600
                    if gps_info[1] == 'S':  #Verifica se a direção é 'S' (sul)
                        latitude = -latitude
                    longitude = int(gps_info[4][0]) + int(gps_info[4][1]) / 60 + int(gps_info[4][2]) / 3600
                    if gps_info[3] == 'W':  #Verifica se a direção é 'W' (oeste)
                        longitude = -longitude
                    sg.popup(f"Latitude: {latitude:.6f}\nLongitude: {longitude:.6f}")
                    open_in_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
                    if sg.popup_yes_no("Deseja abrir no Google Maps?") == "Yes":
                        webbrowser.open(open_in_maps_url)
                else:
                    sg.popup("A imagem não possui informações de GPS.")
            else:
                sg.popup("A imagem não possui dados EXIF.")
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao ler dados de GPS: {str(e)}")


def info_image():
    global image_atual
    global image_path
    try:
        if image_atual:
            largura, altura = image_atual.size
            formato = image_atual.format
            tamanho_bytes = os.path.getsize(image_path)
            tamanho_mb = tamanho_bytes / (1024 * 1024)
            sg.popup(f"Tamanho: {largura} x {altura}\nFormato: {formato}\nTamanho em MB: {tamanho_mb:.2f}")
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao exibir informações da imagem: {str(e)}")

layout = [
    [sg.Menu([['Arquivo', ['Abrir', 'Abrir URL', 'Salvar', 'Fechar']], 
                ['Ajuda', ['Sobre']],
                ['Info', ['Dados da Imagem', 'Mostrar dados da imagem', 'Mostrar dados de GPS']]])],
    [sg.Image(key='-IMAGE-', size=(800,600))],
]

window = sg.Window('Menu e Get File', layout, resizable=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Fechar':
        break

    elif event == 'Abrir':
        arquivo = sg.popup_get_file('Selecionar image', file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
        if arquivo:
            open_image(arquivo)

    elif event == 'Abrir URL':
        url = sg.popup_get_text("Digite a url")
        if url:
            url_download(url)

    elif event == 'Dados da Imagem':
        info_image()

    elif event == 'Mostrar dados da imagem':
        exif_data()

    elif event == 'Mostrar dados de GPS':
        gps_data()

    elif event == 'Salvar':
        if image_atual:
            arquivo = sg.popup_get_file('Salvar image como', save_as=True, file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
            if arquivo:
                save_image(arquivo)
                
    elif event == 'Sobre':
        sg.popup('Desenvolvido pelo BCC - 6 semestre. \n\n Fabiana Sayuri. ')

window.close()