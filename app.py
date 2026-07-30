import streamlit as st
import pandas as pd
import datetime
import os

# Configuración de la página
st.set_page_config(page_title="Antropometría y Triatlón - Historial", layout="wide")

st.title("⚡ Sistema Antropométrico Avanzado con Historial")
st.markdown("---")

# Archivo local o en nube temporal para guardar el historial
ARCHIVO_HISTORIAL = "historial_antropometria.csv"

# Función para cargar datos anteriores
def cargar_historial():
    if os.path.exists(ARCHIVO_HISTORIAL):
        return pd.read_csv(ARCHIVO_HISTORIAL)
    return pd.DataFrame(columns=[
        "Fecha", "Edad", "Peso", "Altura", "Genero", "Objetivo", 
        "Suma_Pliegues", "Porcentaje_Grasa", "Masa_Muscular", "Masa_Grasa", "Masa_Osea"
    ])

df_historial = cargar_historial()

# Pestañas para organizar la app
pestana_nueva, pestana_historial = st.tabs(["📝 Nueva Medición", "📈 Historial y Evolución"])

with pestana_nueva:
    st.header("1. Datos Generales y Antropométricos")

    col1, col2, col3 = st.columns(3)
    with col1:
        edad = st.number_input("Edad (años)", min_value=15, max_value=100, value=28)
        peso = st.number_input("Peso actual (kg)", min_value=30.0, max_value=200.0, value=70.0)
    with col2:
        altura = st.number_input("Altura (cm)", min_value=100.0, max_value=220.0, value=175.0)
        genero = st.selectbox("Género", ["Masculino", "Femenino"])
    with col3:
        objetivo = st.selectbox("Objetivo principal", ["Pérdida de grasa", "Rendimiento en Triatlón", "Mantenimiento"])
        nivel_actividad = st.selectbox("Nivel de Actividad", ["Alto (Entrenamiento diario / Triatlón)", "Moderado", "Liviano"])

    st.subheader("2. Pliegues Cutáneos (mm) - Protocolo ISAK")
    col_pl1, col_pl2, col_pl3, col_pl4 = st.columns(4)
    with col_pl1:
        pliegue_tricipital = st.number_input("Tricipital (mm)", value=10.0)
        pliegue_subescapular = st.number_input("Subescapular (mm)", value=12.0)
    with col_pl2:
        pliegue_bicipital = st.number_input("Bicipital (mm)", value=5.0)
        pliegue_cresta_iliaca = st.number_input("Cresta Ilíaca (mm)", value=14.0)
    with col_pl3:
        pliegue_supraespinal = st.number_input("Supraespinal (mm)", value=9.0)
        pliegue_abdominal = st.number_input("Abdominal (mm)", value=18.0)
    with col_pl4:
        pliegue_muslo = st.number_input("Muslo anterior (mm)", value=15.0)
        pliegue_pantorrilla = st.number_input("Pantorrilla (mm)", value=10.0)

    st.subheader("3. Perímetros Corporales (cm)")
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        brazo_relajado = st.number_input("Brazo extendido / relajado (cm)", value=30.0)
    with col_p2:
        brazo_contraido = st.number_input("Brazo flexionado / fuerza (cm)", value=34.0)
    with col_p3:
        cintura = st.number_input("Cintura (cm)", value=80.0)
    with col_p4:
        pantorrilla_perimetro = st.number_input("Pantorrilla máx. (cm)", value=35.0)

    if st.button("Calcular y Guardar Medición", type="primary"):
        suma_pliegues = (pliegue_tricipital + pliegue_subescapular + pliegue_cresta_iliaca + 
                         pliegue_supraespinal + pliegue_muslo + pliegue_pantorrilla)
        
        if genero == "Masculino":
            porcentaje_grasa = max(5.0, min(40.0, (0.29288 * suma_pliegues) - (0.0005 * (suma_pliegues**2)) + (0.158 * edad) - 5.76))
        else:
            porcentaje_grasa = max(8.0, min(45.0, (0.29669 * suma_pliegues) - (0.00043 * (suma_pliegues**2)) + (0.02963 * edad) + 1.40))

        masa_grasa_kg = peso * (porcentaje_grasa / 100)
        masa_magra_kg = peso - masa_grasa_kg
        masa_osea_kg = peso * 0.14  
        masa_residual_kg = peso * 0.22 if genero == "Masculino" else peso * 0.24 
        masa_muscular_kg = masa_magra_kg - masa_osea_kg - masa_residual_kg

        # Guardar en DataFrame de historial
        nueva_fila = {
            "Fecha": datetime.date.today().strftime("%Y-%m-%d"),
            "Edad": edad, "Peso": peso, "Altura": altura, "Genero": genero, "Objetivo": objetivo,
            "Suma_Pliegues": round(suma_pliegues, 1),
            "Porcentaje_Grasa": round(porcentaje_grasa, 1),
            "Masa_Muscular": round(masa_muscular_kg, 1),
            "Masa_Grasa": round(masa_grasa_kg, 1),
            "Masa_Osea": round(masa_osea_kg, 1)
        }
        
        df_historial = pd.concat([df_historial, pd.DataFrame([nueva_fila])], ignore_index=True)
        df_historial.to_csv(ARCHIVO_HISTORIAL, index=False)
        st.success("¡Medición calculada y guardada con éxito en el historial!")

        st.markdown("---")
        st.header("📊 Resultados Actuales")
        res_col1, res_col2, res_col3, res_col4 = st.columns(4)
        res_col1.metric("Porcentaje de Grasa", f"{porcentaje_grasa:.1f}%", f"{masa_grasa_kg:.1f} kg")
        res_col2.metric("Masa Muscular", f"{masa_muscular_kg:.1f} kg")
        res_col3.metric("Masa Ósea", f"{masa_osea_kg:.1f} kg")
        res_col4.metric("Suma de Pliegues", f"{suma_pliegues:.1f} mm")

        # Nutrición
        if genero == "Masculino":
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
        else:
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

        factor_actividad = 1.8 if "Triatlón" in objetivo or "Alto" in nivel_actividad else 1.5
        gasto_total = tmb * factor_actividad
        calorias_objetivo = gasto_total - 400 if objetivo == "Pérdida de grasa" else gasto_total

        st.markdown("---")
        st.header("🥗 Nutrición y Macronutrientes")
        nut_col1, nut_col2 = st.columns(2)
        with nut_col1:
            st.info(f"**TMB:** {tmb:.0f} kcal | **Gasto Total:** {gasto_total:.0f} kcal")
            st.success(f"**Calorías Objetivo:** {calorias_objetivo:.0f} kcal")
        with nut_col2:
            prot = masa_magra_kg * 2.2
            gras = (calorias_objetivo * 0.25) / 9
            carb = (calorias_objetivo - (prot * 4) - (gras * 9)) / 4
            st.text(f"- Proteínas: {prot:.0f} g\n- Carbohidratos: {carb:.0f} g\n- Grasas: {gras:.0f} g")

with pestana_historial:
    st.header("📈 Evolución Temporal de tu Composición Corporal")
    if len(df_historial) > 0:
        st.dataframe(df_historial, use_container_width=True)
        
        st.subheader("Evolución del Porcentaje de Grasa y Masa Muscular")
        df_grafico = df_historial.set_index("Fecha")[["Porcentaje_Grasa", "Masa_Muscular", "Peso"]]
        st.line_chart(df_grafico)
    else:
        st.info("Aún no hay mediciones guardadas. Ve a la pestaña 'Nueva Medición' y registra tus datos.")