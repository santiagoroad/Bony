# ---------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------- LIBRERIAS --------------------------------------------------- #
import pandas as pd
import os
from datetime import timedelta

# ---------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------- PARAMETROS -------------------------------------------------- #
ARCHIVO_HORAS = "Insumos/bony_horas_5_14_ene.txt"   # SE CAMBIA EL NOMBRE DEL PARAMETRO POR EL NOMBRE DEL ARCHIVO
ARCHIVO_USERS = "Insumos/user_bony.xlsx"    # NO SE DEBE ACTUALIZAR EL NOMBRE DEL ARCHIVO, SIEMPRE VA A SER EL MISMO
FECHA_INICIO = "2026-01-05"                 # SE AGREGA LA FECHA INICIAL PARA EL CALCULO
FECHA_FIN    = "2026-01-14"                 # SE AGREGA LA FECHA FINAL PARA EL CALCULO
resultado = []

# ---------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------ CARGA DE DATOS ------------------------------------------------ #
# ---------------------------------------------------- HORAS ----------------------------------------------------- #
colnames = ["user", "timestamp", "value1", "value2", "value3", "value4"]
time_worked = pd.read_table(ARCHIVO_HORAS, sep='\t', names=colnames, index_col=False)
time_worked["timestamp"] = pd.to_datetime(time_worked["timestamp"])
time_worked["date"] = time_worked["timestamp"].dt.date

time_worked = time_worked.drop(columns=["value1", "value2", "value3", "value4"])

fecha_inicio = pd.to_datetime(FECHA_INICIO).date()
fecha_fin = pd.to_datetime(FECHA_FIN).date()

time_worked = time_worked[
    (time_worked["date"] >= fecha_inicio) &
    (time_worked["date"] <= fecha_fin)
]

# --------------------------------------------------- USUARIOS --------------------------------------------------- #
users = pd.read_excel(ARCHIVO_USERS)
# users["descuento"] = pd.to_datetime(users["descuento"])
# print(users.head())

# ---------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------ LOGICA PROCESO ------------------------------------------------ #
info = time_worked.merge(users, how='left', on='user')
# print(info.head())

# Agrupamiento por usuario y fecha para evaluar cada jornada laborada
for (user, fecha), grupo in info.groupby(["user", "date"]):

    # Ordenar cronológicamente las marcaciones
    grupo = grupo.sort_values("timestamp").reset_index(drop=True)
    
    # Caso sin datos suficientes → no se puede calcular jornada
    if len(grupo) < 2:
        trabajo_real = timedelta(0)

    else:
        inicio = grupo.iloc[0]["timestamp"]
        salida = grupo.iloc[-1]["timestamp"]
        
        bruto = salida - inicio

        # Aplicación de deducciones estándar por pausas obligatorias
        deduccion = grupo.iloc[0]["descuento"]

        val_deducion = timedelta(
            hours=deduccion.hour,
            minutes=deduccion.minute,
            seconds=deduccion.second
        )

        # Tiempo neto laborado
        trabajo_real = bruto - val_deducion
        
        # Corrección si el descuento deja el resultado negativo
        # if trabajo_real < timedelta(0):
        #     trabajo_real = timedelta(0)

    # Conversión a horas decimales
    horas = trabajo_real.total_seconds() / 3600

    resultado.append([fecha, grupo.iloc[0]["user"], grupo.iloc[0]["cc"], grupo.iloc[0]["nombre"], inicio, salida, deduccion, round(horas, 2)])

res = pd.DataFrame(resultado, columns=["date", "user", "cc", "nombre", "hora_entrada", "hora_salida", "valor_deduccion", "horas_extra"])


res["hora_entrada"] = res["hora_entrada"].dt.strftime("%H:%M:%S")
res["hora_salida"]  = res["hora_salida"].dt.strftime("%H:%M:%S")

total_horas = res.groupby("nombre")
total_horas = total_horas["horas_extra"].sum()

# ---------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------ AGRUPADO & RESULTADO FINAL ------------------------------------------ #
total_horas = (
    res.groupby(["user","nombre"], as_index=False)["horas_extra"]
       .sum()
       .rename(columns={"horas_extra": "total_horas_extra"})
)

os.chdir("Resultado/")

with pd.ExcelWriter("reporte_horas_ene_5_14.xlsx", engine="xlsxwriter") as writer:
    res.to_excel(
        writer,
        sheet_name="informacion_general",
        index=False
    )
    
    total_horas.to_excel(
        writer,
        sheet_name="total_horas_extra",
        index=False
    )
