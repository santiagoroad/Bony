from flask import Flask, render_template, make_response, redirect, url_for, session
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import csv, os
from weasyprint import HTML
from informacion_principal import FORMULARIOS_SELECCIONADOS, MATERIA_PRIMA_TORTAS
from funtions import listado_materia_prima
'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# El codigo se saco del día 62 100 days bootcamp
#### CLASES CREACIÓN FLASKFORMS ####
class Reporte(FlaskForm):
    reportes = SelectField('Seleccione el formulario que desea procesar', 
                                choices=[('tortas', 'TORTAS CASERITAS, MANTECADAS Y TORTA NEGRA'),
                                ('hojaldre', 'HOJALDRE'),
                                ('brownies', 'BROWNIES. BROOKIES, CHOCO CHOICE, GALLETAS'),
                                ], validators=[DataRequired()])
    submit = SubmitField('Continuar')

class FormularioTortas(FlaskForm):
    fecha_elaboracion = StringField('Fecha elaboración', validators=[DataRequired()])
    fecha_vencimiento = StringField('Fecha vencimiento', validators=[DataRequired()])
    lote = StringField('Lote', validators=[DataRequired()])
    moldes_cuadraros = StringField('Moldes cuadrados', validators=[DataRequired()])
    moldes_largos = StringField('Moldes largos', validators=[DataRequired()])
    responsable_pesaje = StringField('Responsable pesaje', validators=[DataRequired()])
    unidades_tortas = StringField('Unidades tortas', validators=[DataRequired()])
    unidades_mantecadas = StringField('Unidades mantecadas', validators=[DataRequired()])
    unidades_muffins = StringField('Unidades muffins', validators=[DataRequired()])
    numero_batidora = StringField('Número batidora', validators=[DataRequired()])
    inicio_batido = StringField('Hora inicio batido', validators=[DataRequired()])
    observaciones_mat_prima = StringField('Observaciones materia prima', validators=[DataRequired()])
    observaciones_batido = StringField('Observaciones batidos', validators=[DataRequired()])
    submit = SubmitField('Generar archivo')

#### PAGINA PRINCIPAL
@app.route("/", methods=["GET", "POST"])
def home():
    reporte = Reporte()

    if reporte.validate_on_submit():
        tipo = reporte.reportes.data

        template = FORMULARIOS_SELECCIONADOS[tipo]
        
        return redirect(url_for(template))
    else :
        return render_template("index.html", form=reporte)

#### PARA LAS TORTAS
@app.route('/parametros_tortas', methods=["GET", "POST"])
def param_tortas():
    reporte_tortas = FormularioTortas()

    if reporte_tortas.validate_on_submit():
        informacion_produccion_tortas = {
            field.name: field.data
            for field in reporte_tortas
            if field.name != "submit"
        }
        
        materias_primas = listado_materia_prima("Information/materia_prima_test.xlsx", "torta")
        
        ## Con las lineas de codigo que están comentadas se descarga el pdf
        html_rendered = render_template("formulario_tortas.html", materias_primas = materias_primas)

        # 2. Convertir HTML a PDF
        pdf = HTML(
            string=html_rendered,
            base_url=os.path.abspath("static")
        ).write_pdf()

        # 3. Responder como descarga
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = (
            f"attachment; filename=tortas.pdf"
        )

        return response

        # session["datos_tortas"] = informacion_produccion_tortas
        # return redirect(url_for('tortas'))
    else :
        return render_template("parametros_tortas.html", form = reporte_tortas)

@app.route('/tortas', methods=["GET", "POST"])
def tortas():
    datos = session.get("datos_tortas")
    
    materias_primas = listado_materia_prima("Information/materia_prima_test.xlsx", "torta")
    print(materias_primas)
    return render_template("formulario_tortas.html", form = materias_primas)

#### PARA EL HOJALDRE
@app.route('/parametros_hojaldre', methods=["GET", "POST"])
def hojaldre():
    return render_template("parametros_hojaldre.html")

#### PARA LOS BROWNIES
@app.route('/parametros_brownies', methods=["GET", "POST"])
def brownies():
    return render_template("parametros_brownies.html")

if __name__ == '__main__':
    app.run(debug=True)
