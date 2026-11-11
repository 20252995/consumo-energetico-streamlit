import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Calculadora de Consumo Energético de Laboratorio",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Calculadora de Consumo Energético de Laboratorio")
st.write(
    "Registra los equipos eléctricos del laboratorio y calcula su consumo "
    "y costo mensual utilizando una tarifa eléctrica común."
)

# Estado temporal de la aplicación
if "equipos" not in st.session_state:
    st.session_state.equipos = []

if "contador_equipo" not in st.session_state:
    st.session_state.contador_equipo = 0

if "tarifa" not in st.session_state:
    st.session_state.tarifa = 0.0


def calcular_resultados(equipos, tarifa):
    """Devuelve una tabla con el consumo y costo mensual por equipo."""
    filas = []
    for equipo in equipos:
        consumo = (
            equipo["Potencia (W)"]
            * equipo["Cantidad"]
            * equipo["Horas diarias"]
            * equipo["Días mensuales"]
            / 1000
        )
        costo = consumo * tarifa
        filas.append(
            {
                "Equipo": equipo["Equipo"],
                "Potencia (W)": equipo["Potencia (W)"],
                "Cantidad": equipo["Cantidad"],
                "Horas diarias": equipo["Horas diarias"],
                "Días mensuales": equipo["Días mensuales"],
                "Consumo mensual (kWh)": consumo,
                "Costo mensual (S/)": costo,
            }
        )
    return pd.DataFrame(filas)


with st.sidebar:
    st.header("Configuración")
    tarifa = st.number_input(
        "Tarifa eléctrica (S/ por kWh)",
        min_value=0.0,
        value=float(st.session_state.tarifa),
        step=0.01,
        format="%.4f",
        help="Se aplica la misma tarifa a todos los equipos.",
    )
    st.session_state.tarifa = tarifa

    st.divider()
    st.subheader("Agregar equipo")

    with st.form("formulario_equipo", clear_on_submit=True):
        nombre = st.text_input("Nombre del equipo", placeholder="Ej. Computadora")
        potencia = st.number_input(
            "Potencia (W)", min_value=0.0, value=0.0, step=10.0
        )
        cantidad = st.number_input(
            "Cantidad de equipos", min_value=1, value=1, step=1
        )
        horas = st.number_input(
            "Horas de funcionamiento al día",
            min_value=0.0,
            max_value=24.0,
            value=1.0,
            step=0.5,
        )
        dias = st.number_input(
            "Días de funcionamiento al mes",
            min_value=0,
            max_value=31,
            value=30,
            step=1,
        )
        enviado = st.form_submit_button("Agregar equipo", use_container_width=True)

        if enviado:
            if not nombre.strip():
                st.error("Ingresa un nombre para el equipo.")
            elif potencia <= 0:
                st.error("La potencia debe ser mayor que cero.")
            elif cantidad < 1:
                st.error("La cantidad debe ser al menos 1.")
            elif horas <= 0 or horas > 24:
                st.error("Las horas diarias deben ser mayores que 0 y no superar 24.")
            elif dias <= 0 or dias > 31:
                st.error("Los días mensuales deben estar entre 1 y 31.")
            else:
                st.session_state.contador_equipo += 1
                st.session_state.equipos.append(
                    {
                        "id": st.session_state.contador_equipo,
                        "Equipo": nombre.strip(),
                        "Potencia (W)": float(potencia),
                        "Cantidad": int(cantidad),
                        "Horas diarias": float(horas),
                        "Días mensuales": int(dias),
                    }
                )
                st.success(f"Se agregó «{nombre.strip()}».")

st.subheader("Equipos registrados")

if not st.session_state.equipos:
    st.info("Todavía no hay equipos registrados. Utiliza el formulario del panel lateral.")
else:
    # Mostrar y eliminar registros individualmente
    for equipo in st.session_state.equipos:
        col_nombre, col_detalle, col_boton = st.columns([2, 5, 1])
        with col_nombre:
            st.write(f"**{equipo['Equipo']}**")
        with col_detalle:
            st.caption(
                f"{equipo['Potencia (W)']:,.2f} W · "
                f"{equipo['Cantidad']} unidad(es) · "
                f"{equipo['Horas diarias']:g} h/día · "
                f"{equipo['Días mensuales']} días/mes"
            )
        with col_boton:
            if st.button("Eliminar", key=f"eliminar_{equipo['id']}"):
                st.session_state.equipos = [
                    item for item in st.session_state.equipos
                    if item["id"] != equipo["id"]
                ]
                st.rerun()

    resultados = calcular_resultados(st.session_state.equipos, tarifa)

    st.subheader("Resultados mensuales")
    tabla = resultados.drop(columns=["Cantidad"]) if False else resultados
    st.dataframe(
        tabla.style.format(
            {
                "Potencia (W)": "{:,.2f}",
                "Horas diarias": "{:,.2f}",
                "Consumo mensual (kWh)": "{:,.3f}",
                "Costo mensual (S/)": "S/ {:,.2f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    consumo_total = resultados["Consumo mensual (kWh)"].sum()
    costo_total = resultados["Costo mensual (S/)"].sum()
    col1, col2, col3 = st.columns(3)
    col1.metric("Consumo total mensual", f"{consumo_total:,.3f} kWh")
    col2.metric("Costo total mensual", f"S/ {costo_total:,.2f}")
    col3.metric("Tarifa aplicada", f"S/ {tarifa:,.4f} por kWh")

    mayor = resultados.loc[resultados["Consumo mensual (kWh)"].idxmax()]
    st.success(
        f"Equipo con mayor consumo: **{mayor['Equipo']}** "
        f"({mayor['Consumo mensual (kWh)']:,.3f} kWh/mes)."
    )

    st.subheader("Comparación de consumo por equipo")
    grafico = resultados.set_index("Equipo")[["Consumo mensual (kWh)"]]
    st.bar_chart(grafico, y="Consumo mensual (kWh)", use_container_width=True)

    csv = resultados.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="Descargar resultados en CSV",
        data=csv,
        file_name="resultados_consumo_laboratorio.csv",
        mime="text/csv",
        use_container_width=True,
    )

    if st.button("Eliminar todos los equipos", type="secondary"):
        st.session_state.equipos = []
        st.rerun()

st.caption(
    "Fórmula: Consumo mensual (kWh) = Potencia (W) × Cantidad × "
    "Horas diarias × Días mensuales ÷ 1000. "
    "Costo mensual (S/) = Consumo mensual × Tarifa."
)
