import streamlit as st
import pandas as pd
import datetime
import os
import urllib.parse

# --- CONFIGURACIÓN Y ESTÉTICA VISUAL ---
st.set_page_config(page_title="TROPAFIT | Antropometría por Perímetros", layout="wide", page_icon="⚡")

# Color de fondo idéntico al de la imagen del logo (#222222) y CSS para nitidez de imagen
st.markdown("""
    <style>
    .main {
        background-color: #222222;
        color: #f8fafc;
    }
    .stApp {
        background-color: #222222;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    .logo-img {
        max-width: 180px;
        height: auto;
        image-rendering: -webkit-optimize-contrast; /* Máxima nitidez en navegadores */
        image-rendering: crisp-edges;
    }
    .stButton>button {
        background: linear-gradient(135deg, #a3e635 0%, #65a30d 100%);
        color: #111827;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(163, 230, 53, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(163, 230, 53, 0.5);
    }
    .stMetric {
        background-color: #2d2d2d;
        padding: 15px;
        border-radius: 14px;
        border: 1px solid #3f3f46;
    }
    h1, h2, h3 {
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    .card-info {
        background-color: #2d2d2d;
        padding: 12px;
        border-radius: 10px;
        border-left: 4px solid #a3e635;
        font-size: 0.85rem;
        color: #a1a1aa;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Logo centrado arriba de manera absoluta mediante HTML/CSS Flexbox para máxima nitidez
import base64
logo_path = None
if os.path.exists("logo.png"):
    logo_path = "logo.png"
elif os.path.exists("input_file_1.png"):
    logo_path = "input_file_1.png"

if logo_path:
    with open(logo_path, "rb") as f:
        encoded_logo = base64.b64encode(f.read()).decode('utf-8')
    st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{encoded_logo}" class="logo-img" />
        </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #d4d4d8; font-size: 1.1rem; margin-top: 5px;'>Evaluación Antropométrica por Perímetros, Balanza y Cinta Métrica</p>", unsafe_allow_html=True)
st.markdown("---")

ARCHIVO_HISTORIAL = "historial_perimetros_tropa.csv"

def cargar_historial():
    if os.path.exists(ARCHIVO_HISTORIAL):
        return pd.read_csv(ARCHIVO_HISTORIAL)
    return pd.DataFrame(columns=[
        "Fecha", "Alumno", "Edad", "Peso", "Altura", "Genero", "Disciplina", "Objetivo", 
        "Porcentaje_Grasa", "Masa_Muscular", "Masa_Grasa"
    ])

df_historial = cargar_historial()

pestana_nueva, pestana_historial = st.tabs(["📝 Registro de Perímetros", "📈 Historial y Evolución"])

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
        peso = st.number_input("Peso actual (Balanza - kg)", min_value=30.0, max_value=200.0, value=70.0)
    with col2:
        altura = st.number_input("Altura (cm)", min_value=100.0, max_value=220.0, value=175.0)
        genero = st.selectbox("Género", ["Masculino", "Femenino"])
    with col3:
        nivel_actividad = st.selectbox("Nivel de Actividad Diaria", ["Alto (Entrena todos los días)", "Moderado (3-4 veces por semana)", "Liviano"])
        
        if "Gimnasio" in disciplina:
            tipo_dia = st.selectbox("Enfoque de la sesión", ["Día de Fuerza / Hipertrofia Pesada", "Día de Descanso / Recuperación"])
        else:
            tipo_dia = st.selectbox("Enfoque de la sesión", ["Fondo Largo (Resistencia)", "Intensidad / Series", "Recuperación", "Descanso Total"])

    st.markdown("### 📏 2. Toma de Perímetros (Protocolo Oficial)")
    st.markdown("<div class='card-info'>💡 Registra los perímetros en centímetros (cm) utilizando una cinta métrica flexible e inextensible. Despliega la guía visual abajo para ver exactamente la referencia de cada letra (A hasta L).</div>", unsafe_allow_html=True)

    # --- GUÍA VISUAL CON IMAGEN INCORPORADA ---
    with st.expander("🗺️ Ver Imagen Oficial de Referencia (A-L)", expanded=False):
        if os.path.exists("referencia.png"):
            st.image("referencia.png", use_container_width=True)
        elif os.path.exists("input_file_4.png"):
            st.image("input_file_4.png", use_container_width=True)
        else:
            st.info("Guía visual de referencia (A a L) - Sube tu imagen de referencia como 'referencia.png' a GitHub.")
        
        st.markdown("""
        * **A:** P. Hombros | **B:** P. Pecho | **C1:** P. Bíceps relajado | **C2:** P. Bíceps contraído
        * **D:** P. Antebrazo | **E:** P. Muñeca | **F:** P. Abdomen | **G:** P. Cintura
        * **H:** P. Caderas | **I:** P. Muslo | **J:** P. Rodilla | **K:** P. Gemelos | **L:** P. Tobillo
        """)

    st.markdown("#### **Tren Superior (Tronco y Brazos)**")
    c_ts1, c_ts2, c_ts3, c_ts4 = st.columns(4)
    with c_ts1:
        p_hombros = st.number_input("A - P. Hombros (cm)", value=110.0)
        p_biceps_rel = st.number_input("C1 - P. Bíceps relajado (cm)", value=30.0)
    with c_ts2:
        p_pecho = st.number_input("B - P. Pecho (cm)", value=98.0)
        p_biceps_con = st.number_input("C2 - P. Bíceps contraído (cm)", value=34.0)
    with c_ts3:
        p_antebrazo = st.number_input("D - P. Antebrazo (cm)", value=26.0)
    with c_ts4:
        p_munecca = st.number_input("E - P. Muñeca (cm)", value=16.5)

    st.markdown("#### **Tronco y Cintura**")
    c_tr1, c_tr2, c_tr3 = st.columns(3)
    with c_tr1:
        p_abdomen = st.number_input("F - P. Abdomen (cm)", value=82.0)
    with c_tr2:
        p_cintura = st.number_input("G - P. Cintura (cm)", value=79.0)
    with c_tr3:
        p_caderas = st.number_input("H - P. Caderas (cm)", value=96.0)

    st.markdown("#### **Tren Inferior (Piernas)**")
    c_ti1, c_ti2, c_ti3, c_ti4 = st.columns(4)
    with c_ti1:
        p_muslo = st.number_input("I - P. Muslo (cm)", value=54.0)
    with c_ti2:
        p_rodilla = st.number_input("J - P. Rodilla (cm)", value=37.0)
    with c_ti3:
        p_gemelos = st.number_input("K - P. Gemelos (cm)", value=36.0)
    with c_ti4:
        p_tobillo = st.number_input("L - P. Tobillo (cm)", value=22.0)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Calcular Métricas y Plan de la Tropa", use_container_width=True):
        
        if genero == "Masculino":
            porcentaje_grasa = max(5.0, min(40.0, (1.20 * (peso / ((altura/100)**2))) + (0.23 * edad) - (10.8 * (p_cintura/altura)) - 5.4))
        else:
            porcentaje_grasa = max(8.0, min(45.0, (1.20 * (peso / ((altura/100)**2))) + (0.23 * edad) + (0.15 * p_caderas) - (9.5 * (p_cintura/altura)) - 7.2))

        masa_grasa_kg = peso * (porcentaje_grasa / 100)
        masa_magra_kg = peso - masa_grasa_kg
        
        indice_tono_brazo = p_biceps_con - p_biceps_rel
        masa_muscular_kg = masa_magra_kg * 0.72

        fecha_hoy = datetime.date.today().strftime("%Y-%m-%d")
        nueva_fila = {
            "Fecha": fecha_hoy,
            "Alumno": nombre_alumno,
            "Edad": edad, "Peso": peso, "Altura": altura, "Genero": genero, 
            "Disciplina": disciplina, "Objetivo": objetivo,
            "Porcentaje_Grasa": round(porcentaje_grasa, 1),
            "Masa_Muscular": round(masa_muscular_kg, 1),
            "Masa_Grasa": round(masa_grasa_kg, 1)
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
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Porcentaje de Grasa", f"{porcentaje_grasa:.1f}%", f"{masa_grasa_kg:.1f} kg")
        res_col2.metric("Masa Muscular Est.", f"{masa_muscular_kg:.1f} kg")
        res_col3.metric("Masa Adiposa", f"{masa_grasa_kg:.1f} kg")

        st.markdown("---")
        st.markdown("### 🥗 Plan Nutricional y Objetivos de Energía")
        nut_col1, nut_col2 = st.columns(2)
        with nut_col1:
            st.info(f"**Gasto Energético Total:** {gasto_total:.0f} kcal\n\n**Calorías Objetivo ({objetivo}):** {calorias_objetivo:.0f} kcal")
            st.markdown(f"💪 **Tono / Contracción de Bíceps:** +{indice_tono_brazo:.1f} cm (Indicador de desarrollo muscular local)")
        with nut_col2:
            st.markdown("**Distribución Ideal de Macronutrientes:**")
            st.text(f"• Proteínas: {prot:.0f} g ({prot*4:.0f} kcal)")
            st.text(f"• Carbohidratos: {carb:.0f} g ({carb*4:.0f} kcal)")
            st.text(f"• Grasas: {gras:.0f} g ({gras*9:.0f} kcal)")

        st.markdown("---")
        reporte_texto = f"""*⚡ TROPAFIT - INFORME ANTROPOMÉTRICO*
*Atleta:* {nombre_alumno}
*Fecha:* {fecha_hoy}

*Disciplina:* {disciplina}
*Objetivo:* {objetivo}
*Peso (Balanza):* {peso} kg | *Altura:* {altura} cm | *Edad:* {edad} años

*[COMPOSICIÓN CORPORAL ESTIMADA]*
- Porcentaje de grasa: {porcentaje_grasa:.1f}% ({masa_grasa_kg:.1f} kg)
- Masa muscular estimada: {masa_muscular_kg:.1f} kg

[PERÍMETROS REGISTRADOS (Protocolo Oficial)]
- A. Hombros: {p_hombros} cm
- B. Pecho: {p_pecho} cm
- C1. Bíceps relajado: {p_biceps_rel} cm
- C2. Bíceps contraído: {p_biceps_con} cm (Diferencia: +{indice_tono_brazo:.1f} cm)
- D. Antebrazo: {p_antebrazo} cm
- E. Muñeca: {p_munecca} cm
- F. Abdomen: {p_abdomen} cm
- G. Cintura: {p_cintura} cm
- H. Caderas: {p_caderas} cm
- I. Muslo: {p_muslo} cm
- J. Rodilla: {p_rodilla} cm
- K. Gemelos: {p_gemelos} cm
- L. Tobillo: {p_tobillo} cm

*[PLAN NUTRICIONAL]*
- Calorías Objetivo: {calorias_objetivo:.0f} kcal
- Proteínas: {prot:.0f} g
- Carbohidratos: {carb:.0f} g
- Grasas: {gras:.0f} g
"""

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.download_button(
                label="📄 Descargar Informe (.txt)",
                data=reporte_texto,
                file_name=f"Tropafit_Perimetros_{nombre_alumno}_{fecha_hoy}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col_btn2:
            whatsapp_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(reporte_texto)}"
            st.markdown(f"""
                <a href="{whatsapp_url}" target="_blank">
                    <button style="width: 100%; background: linear-gradient(135deg, #22c55e 0%, #15803d 100%); color: white; border: none; border-radius: 12px; padding: 0.6rem 1.5rem; font-weight: 600; cursor: pointer; box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);">
                        💬 Compartir por WhatsApp
                    </button>
                </a>
            """, unsafe_allow_html=True)

with pestana_historial:
    st.markdown("### 📈 Base de Datos y Progreso de la Tropa")
    if len(df_historial) > 0:
        st.dataframe(df_historial, use_container_width=True)
    else:
        st.info("Aún no se han registrado mediciones en el sistema de la Tropa.")