import streamlit as st
import pandas as pd

st.set_page_config(page_title="Antropometría y Triatlón", layout="wide")

st.title("⚡ Sistema Integral de Antropometría y Nutrición")
st.markdown("---")

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

st.subheader("Perímetros Corporales (cm)")
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    brazo_relajado = st.number_input("Brazo extendido / relajado (cm)", value=30.0)
with col_p2:
    brazo_contraido = st.number_input("Brazo flexionado / haciendo fuerza (cm)", value=34.0)
with col_p3:
    cintura = st.number_input("Cintura (cm)", value=80.0)

if st.button("Calcular Composición y Plan", type="primary"):
    
    if genero == "Masculino":
        porcentaje_grasa = max(8.0, min(35.0, 1.20 * (peso / ((altura/100)**2)) + 0.23 * edad - 16.2))
    else:
        porcentaje_grasa = max(12.0, min(40.0, 1.20 * (peso / ((altura/100)**2)) + 0.23 * edad - 5.4))

    masa_grasa_kg = peso * (porcentaje_grasa / 100)
    masa_magra_kg = peso - masa_grasa_kg
    masa_osea_kg = peso * 0.15 
    masa_muscular_kg = masa_magra_kg - masa_osea_kg

    st.markdown("---")
    st.header("📊 Resultados de la Composición Corporal")
    
    res_col1, res_col2, res_col3, res_col4 = st.columns(4)
    res_col1.metric("Porcentaje de Grasa", f"{porcentaje_grasa:.1f}%", f"{masa_grasa_kg:.1f} kg")
    res_col2.metric("Masa Muscular Est.", f"{masa_muscular_kg:.1f} kg")
    res_col3.metric("Masa Ósea Est.", f"{masa_osea_kg:.1f} kg")
    res_col4.metric("Diferencia Brazo", f"+{brazo_contraido - brazo_relajado:.1f} cm")

    if genero == "Masculino":
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
    else:
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

    factor_actividad = 1.8 if "Triatlón" in objetivo or "Alto" in nivel_actividad else 1.5
    gasto_total = tmb * factor_actividad

    if objetivo == "Pérdida de grasa":
        calorias_objetivo = gasto_total - 400 
    else:
        calorias_objetivo = gasto_total

    st.markdown("---")
    st.header("🥗 Plan Nutricional Sugerido")
    
    nut_col1, nut_col2 = st.columns(2)
    with nut_col1:
        st.info(f"**Gasto Energético Basal (TMB):** {tmb:.0f} kcal")
        st.success(f"**Calorías Objetivo Diarias:** {calorias_objetivo:.0f} kcal")
    
    with nut_col2:
        proteinas_g = masa_magra_kg * 2.0 
        grasas_g = (calorias_objetivo * 0.25) / 9 
        carbohidratos_g = (calorias_objetivo - (proteinas_g * 4) - (grasas_g * 9)) / 4 
        
        st.write("**Distribución de Macronutrientes:**")
        st.text(f"- Proteínas: {proteinas_g:.0f} g")
        st.text(f"- Carbohidratos: {carbohidratos_g:.0f} g")
        st.text(f"- Grasas: {grasas_g:.0f} g")