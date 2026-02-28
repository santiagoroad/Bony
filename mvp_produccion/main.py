import io
import zipfile
from flask import Flask, render_template, make_response, redirect, url_for, session
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Optional
import csv, os
from weasyprint import HTML
from informacion_principal import MATERIA_PRIMA_TORTAS
from funtions import calculo_produccion, listado_materia_prima
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
class FormularioProduccion(FlaskForm):
    b_arequipe = StringField('Ingrese la cantidad de B. arequipe',validators=[Optional()],default="x100gr")
    b_refri = StringField('Ingrese la cantidad de B. Refri', validators=[Optional()], default="-")
    b_mora_arequipe = StringField('Ingrese la cantidad de B. Mora – Arequipe', validators=[Optional()], default="-")
    brookie = StringField('Ingrese la cantidad de Brookie', validators=[Optional()], default="-")
    b_chocolate = StringField('Ingrese la cantidad de B. Chocolate', validators=[Optional()], default="-")
    b_arequipe_pasion = StringField('Ingrese la cantidad de B. Arequipe pasion', validators=[Optional()], default="-")
    b_chocho_pasion = StringField('Ingrese la cantidad de B. Choco pasion', validators=[Optional()], default="-")
    b_refri_pasion = StringField('Ingrese la cantidad de B. Refri pasion', validators=[Optional()], default="-")
    b_white = StringField('Ingrese la cantidad de B. White', validators=[Optional()], default="-")
    b_mini = StringField('Ingrese la cantidad de B. Mini', validators=[Optional()], default="-")
    b_mini_chocolate = StringField('Ingrese la cantidad de B. Mini Chocolate', validators=[Optional()], default="-")
    b_mini_mani  = StringField('Ingrese la cantidad de B. Mini Mani', validators=[Optional()], default="-")
    alfabrownie = StringField('Ingrese la cantidad de Alfabrownie', validators=[Optional()], default="-")
    alfajor = StringField('Ingrese la cantidad de Alfajor', validators=[Optional()], default="-")
    truffes = StringField('Ingrese la cantidad de Trufas', validators=[Optional()], default="-")
    mantecada = StringField('Ingrese la cantidad de Mantecada', validators=[Optional()], default="-")
    t_fruta = StringField('Ingrese la cantidad de T. Fruta', validators=[Optional()], default="-")
    t_amapola = StringField('Ingrese la cantidad de T. Amapola', validators=[Optional()], default="-")
    t_negra = StringField('Ingrese la cantidad de T. Negra', validators=[Optional()], default="-")
    t_tiramisu = StringField('Ingrese la cantidad de T. Tiramisu', validators=[Optional()], default="-")
    t_arequipe_chocolate = StringField('Ingrese la cantidad de T. Arequipe – Chocolate', validators=[Optional()], default="-")
    galleta_avena = StringField('Ingrese la cantidad de Galleta de avena', validators=[Optional()], default="-")
    bocaditos = StringField('Ingrese la cantidad de Bocaditos', validators=[Optional()], default="-")
    corazones = StringField('Ingrese la cantidad de Corazones', validators=[Optional()], default="-")
    a_negro = StringField('Ingrese la cantidad de A. Negro', validators=[Optional()], default="-")
    a_blanco = StringField('Ingrese la cantidad de A. Blanco', validators=[Optional()], default="-")
    g_vinilla = StringField('Ingrese la cantidad de G. Vinilla', validators=[Optional()], default="-")
    g_chocolate = StringField('Ingrese la cantidad de G. Chocolate', validators=[Optional()], default="-")
    b_cheesecake = StringField('Ingrese la cantidad de B. Cheese-cake', validators=[Optional()], default="-")
    b_milky = StringField('Ingrese la cantidad de B. Milky', validators=[Optional()], default="-")
    b_super = StringField('Ingrese la cantidad de B. Super', validators=[Optional()], default="-")
    b_walnut = StringField('Ingrese la cantidad de B. Walnut', validators=[Optional()], default="-")
    submit = SubmitField('Generar producción')

#### PAGINA PRINCIPAL
@app.route("/", methods=["GET", "POST"])
def home():
    reporte_produccion = FormularioProduccion()

    if reporte_produccion.validate_on_submit():
        
        informacion_produccion = {
            field.name: field.data
            for field in reporte_produccion
            if field.name != "submit"
        }
                
        informacion_produccion = {'b_arequipe': '100x100gr', 'b_refri': '700x75gr', 'b_mora_arequipe': '-', 'brookie': '50x70gr,100x75gr', 'b_chocolate': '-', 'b_arequipe_pasion': '300x90gr,600x50gr', 'b_chocho_pasion': '34x50gr,30x80gr', 'b_refri_pasion': '-', 'b_white': '70x70gr', 'b_mini': '-', 'b_mini_chocolate': '-', 'b_mini_mani': '-', 'alfabrownie': '-', 'alfajor': '30x80gr,1000x30gr', 'truffes': '-', 'mantecada': '600xgr,400xlgr', 't_fruta': '-', 't_amapola': '-', 't_negra': '500x75gr', 't_tiramisu': '-', 't_arequipe_chocolate': '-', 'galleta_avena': '70xgr', 'bocaditos': '100xgr', 'corazones': '100xgr', 'a_negro': '-', 'a_blanco': '-', 'g_vinilla': '600x55gr', 'g_chocolate': '600x55gr', 'b_cheesecake': '50x75gr', 'b_milky': '50x75gr', 'b_super': '50x75gr', 'b_walnut': '50x75gr', 'csrf_token': 'ImExNTcxOWYyMzRhYmEyNGE0ZTk2MWFhYjhkMTgzNWI0ODJhMDcxNjEi.aaDpww.T-rg_FvYmzUcwwPKmTNCvfWJyfI'}
        print(informacion_produccion)
        produccion = calculo_produccion(informacion_produccion)
        # PRODUCCION
        html_produccion = render_template(
            "formulario_produccion.html",
            produccion=produccion
        )

        pdf_produccion = HTML(
            string=html_produccion,
            base_url=os.path.abspath("static")
        ).write_pdf()

        # TORTAS
        materias_primas = listado_materia_prima("Information/materia_prima_test.xlsx", "torta")

        html_rendered = render_template("formulario_tortas.html", materias_primas = materias_primas)

        # 2. Convertir HTML a PDF
        pdf_tortas = HTML(
            string=html_rendered,
            base_url=os.path.abspath("static")
        ).write_pdf()

        # ----- CREAR ZIP -----
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("produccion.pdf", pdf_produccion)
            zip_file.writestr("tortas.pdf", pdf_tortas)

        zip_buffer.seek(0)

        response = make_response(zip_buffer.read())
        response.headers["Content-Type"] = "application/zip"
        response.headers["Content-Disposition"] = "attachment; filename=reportes_20280228.zip"

        return response

    else :
        return render_template("index.html", form=reporte_produccion)

if __name__ == '__main__':
    app.run(debug=True)
