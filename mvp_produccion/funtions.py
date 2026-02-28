import pandas as pd
from math import ceil 
from informacion_principal import RESUMEN_PRODUCCION, MATERIA_PRIMA_TORTAS

import pandas as pd
import numpy as np

def calculo_produccion(data: dict) -> pd.DataFrame:

    mat_prima = pd.read_excel(RESUMEN_PRODUCCION)

    data.pop("csrf_token", None)

    filas = []

    for producto, valor in data.items():

        if not valor or valor == "-":
            continue

        for item in valor.split(","):

            item = item.strip()

            if "x" not in item:
                continue

            cantidad, gramaje = item.split("x")

            filas.append(
                (f"{producto}x{gramaje.strip()}", cantidad.strip())
            )

    resultado_df = pd.DataFrame(filas, columns=["Abreviacion", "Cantidad"])
    print("PRODUCTOS PRODUCCCION")
    print(resultado_df)
    informacion_produccion = mat_prima.merge(resultado_df, on="Abreviacion", how="left")
    print("MERGE CON MAT PRIA")
    print(informacion_produccion)
    informacion_produccion["Cantidad"] = (
        pd.to_numeric(informacion_produccion["Cantidad"], errors="coerce")
        .fillna(0)
    )

    und_lata = informacion_produccion["Und_lata"].replace(0, np.nan)
    latas_batido = informacion_produccion["Latas_Batido"].replace(0, np.nan)

    informacion_produccion["Latas"] = np.ceil(
        informacion_produccion["Cantidad"] / und_lata
    ).fillna(0).astype(int)
    print("CALCULO LATASPOR HACER")
    print(informacion_produccion)
    informacion_produccion["Batidos"] = np.ceil(
        informacion_produccion["Latas"] / latas_batido
    ).fillna(0).astype(int)
    print("CALCULO BATIDOS")
    print(informacion_produccion)
    informacion_produccion["Cantidad"] = informacion_produccion["Cantidad"].astype(int)
    informacion_produccion.drop(columns=["Abreviacion", "Und_lata", "Latas_Batido"], inplace=True)

    return informacion_produccion

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

# dict_test = {'b_arequipe': '100x100gr', 'b_refri': '700x75gr', 'b_mora_arequipe': '-', 'brookie': '50x70gr,100x75gr', 'b_chocolate': '-', 'b_arequipe_pasion': '300x90gr,600x50gr', 'b_chocho_pasion': '34x50gr,30x80gr', 'b_refri_pasion': '-', 'b_white': '70x70gr', 'b_mini': '-', 'b_mini_chocolate': '-', 'b_mini_mani': '-', 'alfabrownie': '-', 'alfajor': '30x80gr,1000x30gr', 'truffes': '-', 'mantecada': '600xgr,400xlgr', 't_fruta': '-', 't_amapola': '-', 't_negra': '500x75gr', 't_tiramisu': '-', 't_arequipe_chocolate': '-', 'galleta_avena': '70xgr', 'bocaditos': '100xgr', 'corazones': '100xgr', 'a_negro': '-', 'a_blanco': '-', 'g_vinilla': '600x55gr', 'g_chocolate': '600x55gr', 'b_cheesecake': '50x75gr', 'b_milky': '50x75gr', 'b_super': '50x75gr', 'b_walnut': '50x75gr', 'csrf_token': 'ImExNTcxOWYyMzRhYmEyNGE0ZTk2MWFhYjhkMTgzNWI0ODJhMDcxNjEi.aaDpww.T-rg_FvYmzUcwwPKmTNCvfWJyfI'}

# resumen_dict = calculo_produccion(dict_test)
