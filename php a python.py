from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'secret_key'

# Posibles colores para combinaciones
colores = {
    "White": "#ffffff",
    "Black": "#000000",
    "Blue": "#0000ff",
    "Green": "#00ff00",
    "Red": "#ff0000",
    "Yellow": "#ffff00",
    "Cyan": "#00ffff",
    "Light green": "#90ee90",
    "Dark turquoise": "#00ced1",
    "Purple": "#ff00ff"
}

# Sortea una nueva combinación
def nuevo_secreto(colores):
    secreto = []
    for _ in range(4):
        secreto.append(random.choice(list(colores.values())))
    return secreto

# Calcula resultados de un intento
def calcula_resultado(intento, secreto):
    resultado = []
    for i in range(4):
        if intento[i] == secreto[i]:
            resultado.append('<input style="background-color:green" disabled type="color" value="{0}">'.format(intento[i]))
        elif intento[i] in secreto:
            resultado.append('<input style="background-color:yellow" disabled type="color" value="{0}">'.format(intento[i]))
        else:
            resultado.append('<input disabled type="color" value="{0}">'.format(intento[i]))
    return ''.join(resultado)

# Inicializa la sesión
app.secret_key = 'secret_key'

@app.route('/', methods=['GET', 'POST'])
def mastermind():
    if 'secreto' not in session:
        session['secreto'] = nuevo_secreto(colores)
        session['intentos_realizados'] = []

    intento = []
    intentos_realizados = session.get('intentos_realizados', [])

    if request.method == 'POST':
        intento = request.form.getlist('intento[]')
        session['intentos'] = session.get('intentos', 0) + 1
        resultado = calcula_resultado(intento, session['secreto'])
        intentos_realizados.append((session['intentos'], intento, resultado))
        session['intentos_realizados'] = intentos_realizados

    return render_template('index.html', colores=colores, intento=intento, intentos_realizados=intentos_realizados)

@app.route('/reiniciar', methods=['POST'])
def reiniciar():
    session.pop('secreto', None)
    session.pop('intentos', None)
    session.pop('intentos_realizados', None)
    return "Juego reiniciado."

if __name__ == '__main__':
    app.run(debug=True)
