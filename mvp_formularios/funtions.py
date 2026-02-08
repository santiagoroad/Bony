import pandas as pd
from informacion_principal import MATERIA_PRIMA_TORTAS



def listado_materia_prima(archivo_materia_prima, formulario_eval):
    mat_prima = pd.read_excel(archivo_materia_prima)
    #print(mat_prima.head())
    #print(type(mat_prima))
    resultado = []
    for test in MATERIA_PRIMA_TORTAS:
        # print(item)
        
        informacion = mat_prima.loc[
            mat_prima["MATERIA_PRIMA"] == test,
            ["MATERIA_PRIMA", "PROVEEDOR", "LOTE", "FECHA_VENCIMIENTO"]
        ]

        if not informacion.empty:
            resultado.append(informacion)

    return resultado
