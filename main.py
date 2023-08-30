import PySimpleGUI as sg
from PIL import Image
import io
import requests
import os

def resize_image(image_path):
    img = Image.open(image_path)
    img = img.resize((800,600), Image.Resampling.LANCZOS)
    return img

layout = [
    [sg.Menu([['Arquivo', ['Abrir', 'Fechar', 'Abrir URL', 'Salvar']], 
                ['Ajuda', ['Sobre']],
                ['Info', ['Dados da Imagem']]])],
    [sg.Image(key='-IMAGE-', size=(800,600))],
]

window = sg.Window('Menu e Get File', layout, resizable=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Fechar':
        break
    elif event ==  'Abrir':
        file_path = sg.popup_get_file('Selecione uma imagem', file_types=(("Imagens", "*.jpg *.png"),))
        if file_path:
            resized_img = resize_image(file_path)
            #Converte a imagem PIL para o formato que o PySimpleGUI entende
            img_bytes = io.BytesIO() #Permite criar objetos como se fossem arquivos na memoria RAM
            resized_img.save(img_bytes, format='PNG') #Salva a imagem na memoria RAM
            window['-IMAGE-'].update(data=img_bytes.getvalue())
    elif event == 'Abrir URL':
        url = sg.popup_get_text('Digite a URL da imagem')
        if url:
            response = requests.get(url)
            resized_img = resize_image(io.BytesIO(response.content))
            img_bytes = io.BytesIO()
            resized_img.save(img_bytes, format='PNG')
            window['-IMAGE-'].update(data=img_bytes.getvalue())
    elif event == 'Dados da Imagem':
        sg.popup('Em breve')
    elif event == 'Salvar':
        sg.popup('Em breve')
    elif event == 'Sobre':
        sg.popup('Desenvolvido pelo BCC - 6 semestre. \n\n Fabiana Sayuri. ')

window.close()