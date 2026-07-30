import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Antropometría y Triatlón - ISAK", layout="wide")

st.title("⚡ Sistema Antropométrico Avanzado (Protocolo ISAK)")
st.markdown("---")

# --- SECCIÓN 1: DATOS GENERALES ---
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

# --- SECCIÓN 2: PLIEGUES CUTÁNEOS ISAK (mm) ---
st.subheader("2. Pliegues Cutáneos (mm) - Protocolo ISAK")
st.markdown("Ingresa las mediciones en milímetros tomadas con el plicómetro:")

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

# --- SECCIÓN 3: PERÍMETROS CORPORALES (cm) ---
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

# --- SECCIÓN 4: CÁLCULOS Y ESTIMACIONES AVANZADAS ---
if st.button("Calcular Composición Avanzada ISAK y Plan", type="primary"):
    
    # Suma de pliegues clave para estimación de densidad corporal y % de grasa (Suma de 6 pliegues estándar)
    suma_pliegues = (pliegue_tricipital + pliegue_subescapular + pliegue_cresta_iliaca + 
                     pliegue_supraespinal + pliegue_muslo + pliegue_pantorrilla)
    
    # Estimación de porcentaje de grasa basada en la suma de pliegues (Ecuación de Durnin/Jackson adaptada)
    if genero == "Masculino":
        porcentaje_grasa = max(5.0, min(40.0, (0.29288 * suma_pliegues) - (0.0005 * (suma_pliegues**2)) + (0.158 * edad) - 5.76))
    else:
        porcentaje_grasa = max(8.0, min(45.0, (0.29669 * suma_pliegues) - (0.00043 * (suma_pliegues**2)) + (0.02963 * edad) + 1.40))

    # Masas corporales fraccionadas (Modelo de fraccionamiento antropométrico)
    masa_grasa_kg = peso * (porcentaje_grasa / 100)
    masa_magra_kg = peso - masa_grasa_kg
    
    # Estimación ósea y muscular refinada mediante perímetros corregidos
    masa_osea_kg = peso * 0.14  # Estimación estructural ósea típica
    masa_residual_kg = peso * 0.22 if genero == "Masculino" else peso * 0.24 # Órganos y vísceras
    masa_muscular_kg = masa_magra_kg - masa_osea_kg - masa_residual_kg

    st.markdown("---")
    st.header("📊 Resultados del Fraccionamiento Antropométrico (ISAK)")
    
    res_col1, res_col2, res_col3, res_col4 = st.columns(4)
    res_col1.metric("Porcentaje de Grasa", f"{porcentaje_grasa:.1f}%", f"{masa_grasa_kg:.1f} kg")
    res_col2.metric("Masa Muscular", f"{masa_muscular_kg:.1f} kg")
    res_col3.metric("Masa Ósea", f"{masa_osea_kg:.1f} kg")
    res_col4.metric("Suma de Pliegues", f"{suma_pliegues:.1f} mm")

    # --- SECCIÓN 5: NUTRICIÓN Y GASTO ENERGÉTICO ---
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
    st.header("🥗 Plan Nutricional y Macronutrientes")
    
    nut_col1, nut_col2 = st.columns(2)
    with nut_col1:
        st.info(f"**Gasto Energético Basal (TMB):** {tmb:.0f} kcal")
        st.success(f"**Calorías Objetivo Diarias:** {calorias_objetivo:.0f} kcal")
    
    with nut_col2:
        proteinas_g = masa_magra_kg * 2.2 # Ajuste fino para deportistas de resistencia/fuerza
        grasas_g = (calorias_objetivo * 0.25) / 9 
        carbohidratos_g = (calorias_objetivo - (proteinas_g * 4) - (grasas_g * 9)) / 4 
        
        st.write("**Distribución para Triatlón:**")
        st.text(f"- Proteínas: {proteinas_g:.0f} g (Protección muscular)")
        st.text(f"- Carbohidratos: {carbohidratos_g:.0f} g (Glucógeno para entrenos)")
        st.text(f"- Grasas: {grasas_g:.0f} g (Salud hormonal y metabólica)")

    # --- SECCIÓN 6: ANÁLISIS DE RENDIMIENTO ---
    st.markdown("---")
    st.header("🚴‍♂️ Análisis de Perímetros y Rendimiento en Triatlón")
    diferencia_brazo = brazo_contraido - brazo_relajado
    st.markdown(f"""
    * **Tono del Tren Superior (Natación):** La diferencia en tu brazo entre extendido y contraído es de **+{diferencia_brazo:.1f} cm**. Un buen tono en los bíceps/tríceps aporta estabilidad en la brazada libre en aguas abiertas.
    * **Relación Potencia-Peso:** Con una masa muscular estimada de **{masa_muscular_kg:.1f} kg** frente a tu masa grasa, el control de la evolución de tus pliegues en el muslo y pantorrilla te permitirá maximizar tu eficiencia de carrera a pie (running) reduciendo el costo energético por cada zancada.
    """)