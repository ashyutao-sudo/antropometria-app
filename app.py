import streamlit as st
import pandas as pd
import datetime
import os

# Configuración de la página
st.set_page_config(page_title="Antropometría y Nutrición - Pro", layout="wide")

st.title("⚡ Sistema Antropométrico, Nutrición y Rendimiento")
st.markdown("---")

ARCHIVO_HISTORIAL = "historial_antropometria.csv"

def cargar_historial():
    if os.path.exists(ARCHIVO_HISTORIAL):
        return pd.read_csv(ARCHIVO_HISTORIAL)
    return pd.DataFrame(columns=[
        "Fecha", "Alumno", "Edad", "Peso", "Altura", "Genero", "Disciplina", "Objetivo", 
        "Suma_Pliegues", "Porcentaje_Grasa", "Masa_Muscular", "Masa_Grasa", "Masa_Osea"
    ])

df_historial = cargar_historial()

pestana_nueva, pestana_historial = st.tabs(["📝 Nueva Medición & Plan", "📈 Historial y Evolución"])

with pestana_nueva:
    st.header("1. Datos Generales y del Alumno")

    col_n1, col_n2 = st.columns(2)
    with col_n1:
        nombre_alumno = st.text_input("Nombre / Identificación del Alumno", value="Alumno 1")
        disciplina = st.selectbox("Disciplina Principal", [
            "🏋️‍♂️ Gimnasio (Fuerza / Hipertrofia / Estética)", 
            "🏊‍♂️🚴‍♂️🏃‍♂️ Triatlón / Resistencia"
        ])
    with col_n2:
        objetivo = st.selectbox("Objetivo principal", [
            "Pérdida de grasa / Definición", 
            "Hipertrofia / Ganancia Muscular", 
            "Rendimiento deportivo", 
            "Mantenimiento"
        ])

    col1, col2, col3 = st.columns(3)
    with col1:
        edad = st.number_input("Edad (años)", min_value=15, max_value=100, value=28)
        peso = st.number_input("Peso actual (kg)", min_value=30.0, max_value=200.0, value=70.0)
    with col2:
        altura = st.number_input("Altura (cm)", min_value=100.0, max_value=220.0, value=175.0)
        genero = st.selectbox("Género", ["Masculino", "Femenino"])
    with col3:
        nivel_actividad = st.selectbox("Nivel de Actividad Diaria", ["Alto (Entrena todos los días)", "Moderado (3-4 veces por semana)", "Liviano"])
        
        if "Gimnasio" in disciplina:
            tipo_dia = st.selectbox("Tipo de entrenamiento de hoy", [
                "Día de Fuerza / Hipertrofia Pesada", 
                "Día de Descanso / Recuperación"
            ])
        else:
            tipo_dia = st.selectbox("Tipo de entrenamiento de hoy", [
                "Fondo Largo (Alta demanda resistencia)", 
                "Intensidad / Umbrales (Series)", 
                "Recuperación / Suave", 
                "Descanso Total"
            ])

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

    if st.button("Calcular Plan Nutricional y Corporal", type="primary"):
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

        fecha_hoy = datetime.date.today().strftime("%Y-%m-%d")
        nueva_fila = {
            "Fecha": fecha_hoy,
            "Alumno": nombre_alumno,
            "Edad": edad, "Peso": peso, "Altura": altura, "Genero": genero, 
            "Disciplina": disciplina, "Objetivo": objetivo,
            "Suma_Pliegues": round(suma_pliegues, 1),
            "Porcentaje_Grasa": round(porcentaje_grasa, 1),
            "Masa_Muscular": round(masa_muscular_kg, 1),
            "Masa_Grasa": round(masa_grasa_kg, 1),
            "Masa_Osea": round(masa_osea_kg, 1)
        }
        
        df_historial = pd.concat([df_historial, pd.DataFrame([nueva_fila])], ignore_index=True)
        df_historial.to_csv(ARCHIVO_HISTORIAL, index=False)

        # Cálculo TMB
        if genero == "Masculino":
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
        else:
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

        # Factor de actividad según disciplina
        if "Gimnasio" in disciplina:
            factor_dia = 1.5 if "Alto" in nivel_actividad else 1.35
        else:
            factor_dia = 1.9 if "Fondo" in tipo_dia else 1.6

        gasto_total = tmb * factor_dia
        
        # Ajuste de calorías según objetivo
        if "Pérdida de grasa" in objetivo:
            calorias_objetivo = gasto_total - 400
        elif "Hipertrofia" in objetivo:
            calorias_objetivo = gasto_total + 300  # Superávit para ganar músculo
        else:
            calorias_objetivo = gasto_total

        # Macronutrientes ajustados según la disciplina
        if "Gimnasio" in disciplina:
            prot = masa_magra_kg * 2.2  # Mayor proteína para síntesis de tejido muscular en gym
            gras = (calorias_objetivo * 0.25) / 9
            carb = (calorias_objetivo - (prot * 4) - (gras * 9)) / 4
        else:
            prot = masa_magra_kg * 1.8
            gras = (calorias_objetivo * 0.25) / 9
            carb = (calorias_objetivo - (prot * 4) - (gras * 9)) / 4

        st.markdown("---")
        st.header(f"📊 Resultados para: {nombre_alumno}")
        res_col1, res_col2, res_col3, res_col4 = st.columns(4)
        res_col1.metric("Porcentaje de Grasa", f"{porcentaje_grasa:.1f}%", f"{masa_grasa_kg:.1f} kg")
        res_col2.metric("Masa Muscular", f"{masa_muscular_kg:.1f} kg")
        res_col3.metric("Masa Ósea", f"{masa_osea_kg:.1f} kg")
        res_col4.metric("Diferencia Brazo (Fuerza)", f"+{brazo_contraido - brazo_relajado:.1f} cm")

        st.markdown("---")
        st.header("🥗 Nutrición y Macronutrientes")
        nut_col1, nut_col2 = st.columns(2)
        with nut_col1:
            st.info(f"**Gasto Total (TDEE):** {gasto_total:.0f} kcal")
            st.success(f"**Calorías Objetivo ({objetivo}):** {calorias_objetivo:.0f} kcal")
            
            if "Gimnasio" in disciplina:
                st.warning("💪 **Enfoque Gimnasio:** Prioriza el descanso de 48-72h por grupo muscular y mantén un consumo constante de agua (35ml/kg) para optimizar el volumen celular e hipertrofia.")
            else:
                st.warning("🚴‍♂️ **Enfoque Triatlón:** Mantén atención en la carga de glucógeno y la hidratación intra-entreno.")

        with nut_col2:
            st.write("**Distribución de Macronutrientes:**")
            st.text(f"- Proteínas: {prot:.0f} g ({prot*4:.0f} kcal)")
            st.text(f"- Carbohidratos: {carb:.0f} g ({carb*4:.0f} kcal)")
            st.text(f"- Grasas: {gras:.0f} g ({gras*9:.0f} kcal)")

        # Reporte descargable
        st.markdown("---")
        reporte_texto = f"""
==================================================
INFORME ANTROPOMÉTRICO Y NUTRICIONAL
Alumno: {nombre_alumno}
Fecha: {fecha_hoy}
==================================================
- Disciplina: {disciplina}
- Objetivo: {objetivo}
- Peso: {peso} kg | Altura: {altura} cm | Edad: {edad} años

[COMPOSICIÓN CORPORAL]
- Porcentaje de grasa: {porcentaje_grasa:.1f}% ({masa_grasa_kg:.1f} kg)
- Masa muscular: {masa_muscular_kg:.1f} kg
- Masa ósea: {masa_osea_kg:.1f} kg
- Diferencia de brazo (relajado vs contraído): +{brazo_contraido - brazo_relajado:.1f} cm

[PLAN NUTRICIONAL]
- Calorías Objetivo: {calorias_objetivo:.0f} kcal
- Proteínas: {prot:.0f} g
- Carbohidratos: {carb:.0f} g
- Grasas: {gras:.0f} g
==================================================
"""
        st.download_button(
            label="📄 Descargar Informe del Alumno (.txt)",
            data=reporte_texto,
            file_name=f"Informe_{nombre_alumno}_{fecha_hoy}.txt",
            mime="text/plain"
        )

with pestana_historial:
    st.header("📈 Historial General de Alumnos")
    if len(df_historial) > 0:
        st.dataframe(df_historial, use_container_width=True)
    else:
        st.info("No hay registros guardados todavía.")