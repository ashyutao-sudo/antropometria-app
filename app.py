import streamlit as st
import pandas as pd
import datetime
import os

# Configuración de la página
st.set_page_config(page_title="Antropometría y Triatlón - Pro", layout="wide")

st.title("⚡ Sistema Antropométrico y Nutricional para Triatlón")
st.markdown("---")

ARCHIVO_HISTORIAL = "historial_antropometria.csv"

def cargar_historial():
    if os.path.exists(ARCHIVO_HISTORIAL):
        return pd.read_csv(ARCHIVO_HISTORIAL)
    return pd.DataFrame(columns=[
        "Fecha", "Edad", "Peso", "Altura", "Genero", "Objetivo", 
        "Suma_Pliegues", "Porcentaje_Grasa", "Masa_Muscular", "Masa_Grasa", "Masa_Osea"
    ])

df_historial = cargar_historial()

pestana_nueva, pestana_historial = st.tabs(["📝 Nueva Medición & Plan", "📈 Historial y Evolución"])

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
        tipo_dia = st.selectbox("Tipo de entrenamiento de hoy", [
            "Fondo Largo (Alta demanda / Ciclismo o Running extendido)", 
            "Intensidad / Umbrales (Series)", 
            "Recuperación / Suave (Natación corta o técnica)", 
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

    if st.button("Calcular Plan Específico para Triatlón", type="primary"):
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

        # Guardar en historial
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

        # Cálculo TMB (Mifflin-St Jeor)
        if genero == "Masculino":
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
        else:
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

        # Factor de actividad dinámico según el tipo de día seleccionado
        if "Fondo Largo" in tipo_dia:
            factor_dia = 1.9
        elif "Intensidad" in tipo_dia:
            factor_dia = 1.7
        elif "Recuperación" in tipo_dia:
            factor_dia = 1.4
        else:
            factor_dia = 1.25

        gasto_total = tmb * factor_dia
        
        if objetivo == "Pérdida de grasa" and "Fondo Largo" not in tipo_dia:
            calorias_objetivo = gasto_total - 300  # Déficit moderado controlado
        else:
            calorias_objetivo = gasto_total  # Normocalórica para rendir o aguantar fondos

        st.markdown("---")
        st.header("📊 Composición Corporal y Resultados")
        res_col1, res_col2, res_col3, res_col4 = st.columns(4)
        res_col1.metric("Porcentaje de Grasa", f"{porcentaje_grasa:.1f}%", f"{masa_grasa_kg:.1f} kg")
        res_col2.metric("Masa Muscular", f"{masa_muscular_kg:.1f} kg")
        res_col3.metric("Masa Ósea", f"{masa_osea_kg:.1f} kg")
        res_col4.metric("Suma de Pliegues", f"{suma_pliegues:.1f} mm")

        st.markdown("---")
        st.header("🥗 Nutrición Adaptada al Día de Hoy")
        nut_col1, nut_col2 = st.columns(2)
        with nut_col1:
            st.info(f"**Gasto Estimado (Hoy):** {gasto_total:.0f} kcal")
            st.success(f"**Calorías Objetivo:** {calorias_objetivo:.0f} kcal")
            
            # Hidratación y electrolitos sugeridos por tipo de día
            if "Fondo Largo" in tipo_dia:
                st.warning("💧 **Hidratación sugerida:** 600-800 ml de agua por hora de entrenamiento + aporte de 40-60g de carbohidratos/hora en gel o bebida isotónica.")
            elif "Intensidad" in tipo_dia:
                st.warning("💧 **Hidratación sugerida:** 500 ml/hora con sales minerales (electrolitos) para evitar calambres en umbrales.")
            else:
                st.warning("💧 **Hidratación sugerida:** Mantener ingesta base de 35-40 ml por kg de peso corporal durante el día.")

        with nut_col2:
            # Distribución de macros orientada a resistencia
            prot = masa_magra_kg * 2.0
            gras = (calorias_objetivo * 0.25) / 9
            carb = (calorias_objetivo - (prot * 4) - (gras * 9)) / 4
            
            st.write("**Macronutrientes recomendados para hoy:**")
            st.text(f"- Proteínas: {prot:.0f} g ({prot*4:.0f} kcal)")
            st.text(f"- Carbohidratos: {carb:.0f} g ({carb*4:.0f} kcal)")
            st.text(f"- Grasas: {gras:.0f} g ({gras*9:.0f} kcal)")

with pestana_historial:
    st.header("📈 Historial de Evolución Temporal")
    if len(df_historial) > 0:
        st.dataframe(df_historial, use_container_width=True)
        st.subheader("Gráfica de Progreso")
        df_grafico = df_historial.set_index("Fecha")[["Porcentaje_Grasa", "Masa_Muscular", "Peso"]]
        st.line_chart(df_grafico)
    else:
        st.info("No hay registros todavía.")