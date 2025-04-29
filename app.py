from flask import Flask, render_template, request   # importando modulo, clase y objetos.

app = Flask(__name__)   # Diciendo a flask que arranque de acá.

def analizar_seo(titulo, descripcion):
    score = 100
    consejos = []


    # 1. Longitud del titulo
    if len(titulo) < 30:
        score -= 10
        consejos.append("El titulo es demasiado corto (menos de 30 caracteres).")
    elif len(titulo) > 70:
        score -= 10
        consejos.append("El titulo es muy largo (más de 70 caracteres).")
        # Acá hay un hueco de posibilidad a error, por que 40, 50, 60 quedan libres. Más los decimales evidentemente.
    
    # 2. Longitud de la descripción
    if len(descripcion) < 100:
        score -= 10
        consejos.append("La descripción es demasiado corta (menos de 100 caracteres).")
        # Lo mismo que el anterior, muchos posibles bugs, por falta de lógica condicinal multiples.

    # 3. Repetición de palabras clave (simplificado)
    palabras_titulo = set(titulo.lower().split())
    palabras_desc = descripcion.lower().split()
    coincidencias = [palabra for palabra in palabras_titulo if palabra in palabras_desc]    # Para cada palabra dentro del vector SI esta dentro de palabras_desc, añadelo, sino no. Se debe cumplir que la palabra este en A y en B.

    if len(coincidencias) < 2:
        score -= 10
        consejos.append("Pocas coincidencias entre el titulo y descripción. Añade palabras clave relevantes.")

    return score, consejos

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/analyze", methods = ["POST"])
def analyze():
    titulo = request.form["titulo"]
    descripcion= request.form["descripcion"]
    score, consejos = analizar_seo(titulo, descripcion)

    return f"""
    <h2>Resultados del análisis SEO</h2>
    <p><strong>Score:</strong> {score}/100</p>
    <h3>Consejos:</h3>
    <ul>
        {''.join(f"<li>{c}</li>" for c in consejos) if consejos else '<li>¡Buen trabajo! Tu SEO se ve sólido.</li>'}
    </ul>
    <br><a href="/">Volver</a>
    """

if __name__ == "__main__":
    app.run(debug = True)

