import streamlit as st
import pandas as pd
import datetime
import os

# --- CONFIGURACIÓN Y ESTÉTICA VISUAL ---
st.set_page_config(page_title="Tropa | Antropometría y Rendimiento", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    }
    .stMetric {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 14px;
        border: 1px solid #334155;
    }
    h1, h2, h3 {
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    .mapa-box {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #334155;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>⚡ TROPA PERFORMANCE LAB</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.1rem;'>Sistema inteligente de antropometría, composición corporal y nutrición deportiva.</p>", unsafe_allow_html=True)
st.markdown("---")

ARCHIVO_HISTORIAL = "historial_antropometria_tropa.csv"

def cargar_historial():
    if os.path.exists(ARCHIVO_HISTORIAL):
        return pd.read_csv(ARCHIVO_HISTORIAL)
    return pd.DataFrame(columns=[
        "Fecha", "Alumno", "Edad", "Peso", "Altura", "Genero", "Disciplina", "Objetivo", 
        "Suma_Pliegues", "Porcentaje_Grasa", "Masa_Muscular", "Masa_Grasa", "Masa_Osea"
    ])

df_historial = cargar_historial()

pestana_nueva, pestana_historial = st.tabs(["📝 Nueva Medición & Guía Anatómica", "📈 Historial de la Tropa"])

with pestana_nueva:
    st.markdown("### 👤 1. Perfil del Atleta")

    col_n1, col_n2 = st.columns(2)
    with col_n1:
        nombre_alumno = st.text_input("Nombre del Atleta", value="Atleta Tropa")
        disciplina = st.selectbox("Disciplina Principal", [
            "🏋️‍♂️ Gimnasio (Fuerza / Hipertrofia)", 
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
            tipo_dia = st.selectbox("Enfoque de la sesión", [
                "Día de Fuerza / Hipertrofia Pesada", 
                "Día de Descanso / Recuperación"
            ])
        else:
            tipo_dia = st.selectbox("Enfoque de la sesión", [
                "Fondo Largo (Resistencia extendida)", 
                "Intensidad / Umbrales (Series)", 
                "Recuperación / Suave", 
                "Descanso Total"
            ])

    # --- MAPA ANATÓMICO VISUAL DEL CUERPO HUMANO ---
    st.markdown("### 🗺️ Guía Visual del Cuerpo Humano (Puntos Antropométricos)")
    st.markdown("Utiliza este esquema visual interactivo para ubicar exactamente cada zona de medición en el cuerpo de tu atleta:")

    # Dibujo esquemático del cuerpo humano mediante SVG integrado de alta calidad visual
    st.markdown("""
    <div class="mapa-box">
        <svg viewBox="0 0 600 320" width="100%" height="100%" style="max-height: 280px;">
            <!-- Silueta humana estilizada central -->
            <g fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity="0.4">
                <!-- Cabeza y cuello -->
                <circle cx="300" cy="35" r="18"/>
                <path d="M300 53 v20"/>
                <!-- Tronco -->
                <path d="M275 73 h50 l15 90 h-80 z"/>
                <!-- Brazos -->
                <path d="M275 73 l-35 50 l-25 45"/>
                <path d="M325 73 l35 50 l25 45"/>
                <!-- Piernas -->
                <path d="M280 163 l-15 80 l-10 70"/>
                <path d="M320 163 l15 80 l10 70"/>
            </g>

            <!-- Puntos interactivos señalados con líneas y etiquetas -->
            <!-- Bicipital y Tricipital -->
            <line x1="240" y1="110" x2="160" y2="80" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="3,3"/>
            <circle cx="240" cy="110" r="4" fill="#f43f5e"/>
            <text x="70" y="85" fill="#f8fafc" font-size="12" font-family="sans-serif">💪 Bicipital / Tricipital</text>

            <!-- Subescapular -->
            <line x1="310" y1="95" x2="420" y2="60" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3,3"/>
            <circle cx="310" cy="95" r="4" fill="#38bdf8"/>
            <text x="430" y="65" fill="#f8fafc" font-size="12" font-family="sans-serif">🦴 Subescapular (Espalda)</text>

            <!-- Cresta Ilíaca y Supraespinal -->
            <line x1="325" y1="145" x2="430" y2="120" stroke="#10b981" stroke-width="1.5" stroke-dasharray="3,3"/>
            <circle cx="325" cy="145" r="4" fill="#10b981"/>
            <text x="435" y="125" fill="#f8fafc" font-size="12" font-family="sans-serif">📍 Cresta Ilíaca / Supraespinal</text>

            <!-- Abdominal y Cintura -->
            <line x1="300" y1="130" x2="150" y2="140" stroke="#eab308" stroke-width="1.5" stroke-dasharray="3,3"/>
            <circle cx="300" cy="130" r="4" fill="#eab308"/>
            <text x="60" y="145" fill="#f8fafc" font-size="12" font-family="sans-serif">🎯 Abdominal / Cintura</text>

            <!-- Muslo -->
            <line x1="270" y1="210" x2="140" y2="200" stroke="#a855f7" stroke-width="1.5" stroke-dasharray="3,3"/>
            <circle cx="270" cy="210" r="4" fill="#a855f7"/>
            <text x="75" y="205" fill="#f8fafc" font-size="12" font-family="sans-serif">🦵 Muslo Anterior</text>

            <!-- Pantorrilla -->
            <line x1="255" y1="280" x2="410" y2="260" stroke="#06b6d4" stroke-width="1.5" stroke-dasharray="3,3"/>
            <circle cx="255" cy="280" r="4" fill="#06b6d4"/>
            <text x="420" y="265" fill="#f8fafc" font-size="12" font-family="sans-serif">⚡ Pantorrilla Máxima</text>
        </svg>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📐 2. Pliegues Cutáneos (Protocolo ISAK - mm)")
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

    st.markdown("### 📏 3. Perímetros Corporales (cm)")
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        brazo_relajado = st.number_input("Brazo extendido (cm)", value=30.0)
    with col_p2:
        brazo_contraido = st.number_input("Brazo contraído (cm)", value=34.0)
    with col_p3:
        cintura = st.number_input("Cintura (cm)", value=80.0)
    with col_p4:
        pantorrilla_perimetro = st.number_input("Pantorrilla máx. (cm)", value=35.0)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Calcular Métricas y Plan de la Tropa", use_container_width=True):
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

        if genero == "Masculino":
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
        else:
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

        factor_dia = 1.5 if "Gimnasio" in disciplina else 1.8
        gasto_total = tmb * factor_dia
        
        if "Pérdida de grasa" in objetivo:
            calorias_objetivo = gasto_total - 400
        elif "Hipertrofia" in objetivo:
            calorias_objetivo = gasto_total + 300  
        else:
            calorias_objetivo = gasto_total

        if "Gimnasio" in disciplina:
            prot = masa_magra_kg * 2.2  
            gras = (calorias_objetivo * 0.25) / 9
            carb = (calorias_objetivo - (prot * 4) - (gras * 9)) / 4
        else:
            prot = masa_magra_kg * 1.8
            gras = (calorias_objetivo * 0.25) / 9
            carb = (calorias_objetivo - (prot * 4) - (gras * 9)) / 4

        st.markdown("---")
        st.markdown(f"### 📊 Resultados de Composición: {nombre_alumno}")
        res_col1, res_col2, res_col3, res_col4 = st.columns(4)
        res_col1.metric("Porcentaje de Grasa", f"{porcentaje_grasa:.1f}%", f"{masa_grasa_kg:.1f} kg")
        res_col2.metric("Masa Muscular", f"{masa_muscular_kg:.1f} kg")
        res_col3.metric("Masa Ósea", f"{masa_osea_kg:.1f} kg")
        res_col4.metric("Diferencia Brazo", f"+{brazo_contraido - brazo_relajado:.1f} cm")

        st.markdown("---")
        st.markdown("### 🥗 Plan Nutricional y Objetivos de Energía")
        nut_col1, nut_col2 = st.columns(2)
        with nut_col1:
            st.info(f"**Gasto Energético Total:** {gasto_total:.0f} kcal\n\n**Calorías Objetivo ({objetivo}):** {calorias_objetivo:.0f} kcal")
        with nut_col2:
            st.markdown("**Distribución Ideal de Macronutrientes:**")
            st.text(f"• Proteínas: {prot:.0f} g ({prot*4:.0f} kcal)")
            st.text(f"• Carbohidratos: {carb:.0f} g ({carb*4:.0f} kcal)")
            st.text(f"• Grasas: {gras:.0f} g ({gras*9:.0f} kcal)")

        st.markdown("---")
        reporte_texto = f"""
==================================================
TROPA PERFORMANCE LAB - INFORME NUTRICIONAL
Atleta: {nombre_alumno}
Fecha: {fecha_hoy}
==================================================
- Disciplina: {disciplina}
- Objetivo: {objetivo}
- Peso: {peso} kg | Altura: {altura} cm | Edad: {edad} años

[COMPOSICIÓN CORPORAL]
- Porcentaje de grasa: {porcentaje_grasa:.1f}% ({masa_grasa_kg:.1f} kg)
- Masa muscular: {masa_muscular_kg:.1f} kg
- Masa ósea: {masa_osea_kg:.1f} kg
- Tono / Diferencia de brazo: +{brazo_contraido - brazo_relajado:.1f} cm

[PLAN NUTRICIONAL]
- Calorías Objetivo: {calorias_objetivo:.0f} kcal
- Proteínas: {prot:.0f} g
- Carbohidratos: {carb:.0f} g
- Grasas: {gras:.0f} g
==================================================
"""
        st.download_button(
            label="📄 Descargar Informe Estilizado (.txt)",
            data=reporte_texto,
            file_name=f"Tropa_{nombre_alumno}_{fecha_hoy}.txt",
            mime="text/plain",
            use_container_width=True
        )

with pestana_historial:
    st.markdown("### 📈 Base de Datos y Progreso de la Tropa")
    if len(df_historial) > 0:
        st.dataframe(df_historial, use_container_width=True)
    else:
        st.info("Aún no se han registrado mediciones en el sistema de la Tropa.")