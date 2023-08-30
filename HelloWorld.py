import PySimpleGUI as sg

layout = [
    [sg.Text("Digite um texto: ")],
    [sg.Input(key='-INPUT-')],
    [sg.Button('Mostrar valor')],
]

window = sg.Window('Botões', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event ==  'Mostrar valor':
        input_text = values['-INPUT-']
        sg.popup(f'Você digitou: {input_text}')

window.close()