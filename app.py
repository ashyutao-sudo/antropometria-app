import streamlit as st
import pandas as pd
import datetime
import os
import sqlite3
import hashlib
import urllib.parse
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="TROPAFIT | Sistema Antropométrico", layout="wide", page_icon="⚡")

# --- CONEXIÓN Y CONFIGURACIÓN DE BASE DE DATOS SQLITE ---
DB_FILE = "tropafit_database.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            rol TEXT NOT NULL,
            disciplina TEXT,
            objetivo TEXT,
            meta_peso REAL DEFAULT 70.0
        )
    ''')
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN meta_peso REAL DEFAULT 70.0")
    except sqlite3.OperationalError:
        pass

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mediciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            fecha TEXT,
            edad INTEGER,
            peso REAL,
            altura REAL,
            genero TEXT,
            p_hombros REAL,
            p_pecho REAL,
            p_biceps_rel REAL,
            p_biceps_con REAL,
            p_antebrazo REAL,
            p_munecca REAL,
            p_abdomen REAL,
            p_cintura REAL,
            p_caderas REAL,
            p_muslo REAL,
            p_rodilla REAL,
            p_gemelos REAL,
            p_tobillo REAL,
            porcentaje_grasa REAL,
            masa_muscular REAL,
            masa_grasa REAL,
            FOREIGN KEY (username) REFERENCES usuarios(username)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- ESTÉTICA VISUAL ---
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
        max-width: 160px;
        height: auto;
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
    .report-box {
        background-color: #1e1e1e;
        border: 1px solid #333333;
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

logo_path = "logo.png" if os.path.exists("logo.png") else ("input_file_1.png" if os.path.exists("input_file_1.png") else None)
if logo_path:
    with open(logo_path, "rb") as f:
        encoded_logo = base64.b64encode(f.read()).decode('utf-8')
    st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{encoded_logo}" class="logo-img" />
        </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #d4d4d8; font-size: 1.1rem; margin-top: 5px;'>Informe de Composición Corporal & Evolución</p>", unsafe_allow_html=True)
st.markdown("---")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['rol'] = ''

def login_view():
    st.markdown("### 🔐 Acceso al Sistema TROPAFIT")
    tab_login, tab_registro = st.tabs(["🔑 Iniciar Sesión", "📝 Registrarse (Nuevo Atleta)"])
    
    with tab_login:
        with st.form("form_login"):
            user_input = st.text_input("Usuario")
            pass_input = st.text_input("Contraseña", type="password")
            btn_submit = st.form_submit_button("Entrar")
            
            if btn_submit:
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute("SELECT password, rol FROM usuarios WHERE username = ?", (user_input,))
                result = cursor.fetchone()
                conn.close()
                
                if result and result[0] == hash_password(pass_input):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = user_input
                    st.session_state['rol'] = result[1]
                    st.success("¡Bienvenido a la Tropa!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")
                    
    with tab_registro:
        with st.form("form_registro"):
            new_user = st.text_input("Elige un Nombre de Usuario")
            new_pass = st.text_input("Elige una Contraseña", type="password")
            new_rol = st.selectbox("Tipo de Cuenta", ["Atleta", "Entrenador"])
            new_meta = st.number_input("Peso Objetivo / Meta (kg)", value=68.0)
            new_disc = st.selectbox("Disciplina Principal", ["🏋️‍♂️ Gimnasio (Fuerza / Hipertrofia)", "🏊‍♂️🚴‍♂️🏃‍♂️ Triatlón / Resistencia"])
            new_obj = st.selectbox("Objetivo Principal", ["Pérdida de grasa / Definición", "Hipertrofia / Ganancia Muscular", "Rendimiento deportivo", "Mantenimiento"])
            btn_reg = st.form_submit_button("Crear Cuenta")
            
            if btn_reg:
                if new_user and new_pass:
                    conn = sqlite3.connect(DB_FILE)
                    cursor = conn.cursor()
                    try:
                        cursor.execute("INSERT INTO usuarios (username, password, rol, disciplina, objetivo, meta_peso) VALUES (?, ?, ?, ?, ?, ?)",
                                       (new_user, hash_password(new_pass), new_rol, new_disc, new_obj, new_meta))
                        conn.commit()
                        st.success("¡Cuenta creada con éxito! Ve a la pestaña 'Iniciar Sesión'.")
                    except sqlite3.IntegrityError:
                        st.error("El nombre de usuario ya existe. Elige otro.")
                    conn.close()
                else:
                    st.warning("Completa todos los campos.")

if not st.session_state['logged_in']:
    login_view()
else:
    with st.sidebar:
        st.write(f"👤 Conectado como: **{st.session_state['username']}**")
        st.write(f"🏷️ Rol: **{st.session_state['rol']}**")
        if st.button("Cerrar Sesión"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.session_state['rol'] = ''
            st.rerun()
            
    if st.session_state['rol'] == "Atleta":
        atleta_actual = st.session_state['username']
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT meta_peso FROM usuarios WHERE username = ?", (atleta_actual,))
        meta_res = cursor.fetchone()
        meta_peso = meta_res[0] if meta_res and meta_res[0] is not None else 70.0
        conn.close()
        
        tab_medicion, tab_evolucion = st.tabs(["📝 Nueva Medición & Informe", "📈 Mi Evolución y Meta"])
        
        with tab_medicion:
            st.markdown(f"### 👤 Carga de Perímetros: {atleta_actual}")
            
            col_n1, col_n2 = st.columns(2)
            with col_n1:
                edad = st.number_input("Edad (años)", min_value=15, max_value=100, value=28)
                peso = st.number_input("Peso actual (Balanza - kg)", min_value=30.0, max_value=200.0, value=70.0)
            with col_n2:
                altura = st.number_input("Altura (cm)", min_value=100.0, max_value=220.0, value=175.0)
                genero = st.selectbox("Género", ["Masculino", "Femenino"])

            st.markdown("### 📏 Toma de Perímetros (Protocolo Oficial)")
            st.markdown("<div class='card-info'>💡 Registra los perímetros en centímetros (cm) utilizando una cinta métrica flexible.</div>", unsafe_allow_html=True)

            with st.expander("🗺️ Ver Imagen Oficial de Referencia (A-L)", expanded=False):
                if os.path.exists("referencia.png"):
                    st.image("referencia.png", use_container_width=True)
                elif os.path.exists("input_file_4.png"):
                    st.image("input_file_4.png", use_container_width=True)
                else:
                    st.info("Guía visual de referencia (A a L)")
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

            if st.button("🚀 Guardar Medición y Generar Informe", use_container_width=True):
                if genero == "Masculino":
                    porcentaje_grasa = max(5.0, min(40.0, (1.20 * (peso / ((altura/100)**2))) + (0.23 * edad) - (10.8 * (p_cintura/altura)) - 5.4))
                else:
                    porcentaje_grasa = max(8.0, min(45.0, (1.20 * (peso / ((altura/100)**2))) + (0.23 * edad) + (0.15 * p_caderas) - (9.5 * (p_cintura/altura)) - 7.2))

                masa_grasa_kg = peso * (porcentaje_grasa / 100)
                masa_magra_kg = peso - masa_grasa_kg
                masa_muscular_kg = masa_magra_kg * 0.72
                masa_osea_kg = peso * 0.14
                masa_residual_kg = peso * 0.22 if genero == "Masculino" else peso * 0.24
                
                fecha_hoy = datetime.date.today().strftime("%Y-%m-%d")

                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO mediciones (
                        username, fecha, edad, peso, altura, genero, 
                        p_hombros, p_pecho, p_biceps_rel, p_biceps_con, p_antebrazo, p_munecca, 
                        p_abdomen, p_cintura, p_caderas, p_muslo, p_rodilla, p_gemelos, p_tobillo, 
                        porcentaje_grasa, masa_muscular, masa_grasa
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (atleta_actual, fecha_hoy, edad, peso, altura, genero,
                      p_hombros, p_pecho, p_biceps_rel, p_biceps_con, p_antebrazo, p_munecca,
                      p_abdomen, p_cintura, p_caderas, p_muslo, p_rodilla, p_gemelos, p_tobillo,
                      round(porcentaje_grasa, 1), round(masa_muscular_kg, 1), round(masa_grasa_kg, 1)))
                
                cursor.execute("SELECT peso, porcentaje_grasa FROM mediciones WHERE username = ? ORDER BY fecha ASC LIMIT 1", (atleta_actual,))
                primer_reg = cursor.fetchone()
                conn.commit()
                conn.close()

                dif_peso = round(peso - primer_reg[0], 2) if primer_reg else 0.0
                dif_grasa = round(porcentaje_grasa - primer_reg[1], 2) if primer_reg else 0.0

                st.markdown("---")
                st.markdown(f"<h2 style='text-align: center; color: #a3e635;'>📋 INFORME DE COMPOSICIÓN CORPORAL</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: #a1a1aa;'>Atleta: <b>{atleta_actual}</b> | Fecha: {fecha_hoy} | Edad: {edad} años</p>", unsafe_allow_html=True)

                tabla_datos = {
                    "Fraccionamiento": ["Masa Adiposa", "Masa Muscular", "Masa Ósea", "Masa Residual", "Masa Total"],
                    "Kg": [round(masa_grasa_kg, 2), round(masa_muscular_kg, 2), round(masa_osea_kg, 2), round(masa_residual_kg, 2), round(peso, 2)],
                    "Porcentaje": [f"{round(porcentaje_grasa, 1)}%", f"{round((masa_muscular_kg/peso)*100, 1)}%", f"{round((masa_osea_kg/peso)*100, 1)}%", f"{round((masa_residual_kg/peso)*100, 1)}%", "100.0%"],
                    "Dif. Inicio": [f"{dif_grasa:+.1f}%", f"-", f"-", f"-", f"{dif_peso:+.1f} kg"]
                }
                df_reporte = pd.DataFrame(tabla_datos)
                st.dataframe(df_reporte, use_container_width=True)

                tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + (5 if genero == "Masculino" else -161)
                gasto_est = tmb * 1.55
                imc = peso / ((altura/100)**2)

                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.info(f"**Estimación Gasto Energético:**\n- Metabolismo Basal: {tmb:.0f} Kcal\n- Gasto Estimado (Mod): {gasto_est:.0f} Kcal")
                with col_d2:
                    st.success(f"**Datos Adicionales:**\n- IMC: {imc:.2f} Kg/m²\n- Peso Meta: {meta_peso} Kg\n- Diferencia a Meta: {round(peso - meta_peso, 1)} Kg")

                reporte_texto = f"""*⚡ TROPAFIT - INFORME CLÍNICO ANTROPOMÉTRICO*
*Atleta:* {atleta_actual} | *Fecha:* {fecha_hoy}
- Peso Total: {peso} kg (Dif. Inicio: {dif_peso:+.1f} kg | Meta: {meta_peso} kg)
- Masa Adiposa: {porcentaje_grasa:.1f}% ({masa_grasa_kg:.1f} kg)
- Masa Muscular: {masa_muscular_kg:.1f} kg
- Gasto Energético Est.: {gasto_est:.0f} Kcal
"""
                whatsapp_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(reporte_texto)}"
                st.markdown(f"""
                    <a href="{whatsapp_url}" target="_blank">
                        <button style="width: 100%; background: linear-gradient(135deg, #22c55e 0%, #15803d 100%); color: white; border: none; border-radius: 12px; padding: 0.6rem 1.5rem; font-weight: 600; cursor: pointer; box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);">
                            💬 Compartir Informe Clínico por WhatsApp
                        </button>
                    </a>
                """, unsafe_allow_html=True)

        with tab_evolucion:
            st.markdown(f"### 📈 Tu Línea de Evolución y Comparativa con el Inicio")
            
            conn = sqlite3.connect(DB_FILE)
            df_user = pd.read_sql_query("SELECT fecha, peso, porcentaje_grasa, masa_muscular, p_cintura FROM mediciones WHERE username = ? ORDER BY fecha ASC", conn, params=(atleta_actual,))
            conn.close()
            
            if not df_user.empty:
                inicio = df_user.iloc[0]
                actual = df_user.iloc[-1]
                
                col_m1, col_m2, col_m3 = st.columns(3)
                col_m1.metric("🏁 1er Registro (Inicio)", f"{inicio['peso']} kg", f"Grasa: {inicio['porcentaje_grasa']}%")
                col_m2.metric("📍 Registro Actual", f"{actual['peso']} kg", f"{round(actual['peso'] - inicio['peso'], 1)} kg vs inicio")
                col_m3.metric("🎯 Peso Meta", f"{meta_peso} kg", f"Faltan: {round(actual['peso'] - meta_peso, 1)} kg")
                
                st.markdown("---")
                st.subheader("📋 Tabla Histórica de Evolución")
                st.dataframe(df_user, use_container_width=True)
                
                st.subheader("📉 Gráfica de Progreso")
                st.line_chart(df_user.set_index("fecha")[["peso", "porcentaje_grasa", "masa_muscular"]])
            else:
                st.info("Aún no tienes registros guardados. Carga tu primera medición.")

    elif st.session_state['rol'] == "Entrenador":
        st.markdown("### 🏆 Panel de Control del Entrenador - Tropa")
        st.write("Visualiza el informe clínico y comparativo de tus atletas.")
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT username, meta_peso FROM usuarios WHERE rol = 'Atleta'")
        atletas_info = cursor.fetchall()
        
        if atletas_info:
            nombres_atletas = [a[0] for a in atletas_info]
            atleta_seleccionado = st.selectbox("Selecciona un Atleta de la Tropa:", nombres_atletas)
            
            meta_atleta = [a[1] for a in atletas_info if a[0] == atleta_seleccionado][0]
            if meta_atleta is None:
                meta_atleta = 70.0
            
            df_atleta = pd.read_sql_query("SELECT * FROM mediciones WHERE username = ? ORDER BY fecha ASC", conn, params=(atleta_seleccionado,))
            conn.close()
            
            if not df_atleta.empty:
                inicio = df_atleta.iloc[0]
                actual = df_atleta.iloc[-1]
                
                col_e1, col_e2, col_e3 = st.columns(3)
                col_e1.metric("🏁 Inicio (1er Registro)", f"{inicio['peso']} kg", f"Grasa: {inicio['porcentaje_grasa']}%")
                col_e2.metric("📊 Último Registro", f"{actual['peso']} kg", f"Grasa: {actual['porcentaje_grasa']}%")
                col_e3.metric("🎯 Meta Establecida", f"{meta_atleta} kg")
                
                st.markdown("---")
                st.markdown(f"#### Historial Clínico de: {atleta_seleccionado}")
                st.dataframe(df_atleta, use_container_width=True)
                
                if len(df_atleta) > 1:
                    st.subheader("📈 Línea de Evolución del Atleta")
                    st.line_chart(df_atleta.set_index("fecha")[["peso", "porcentaje_grasa", "masa_muscular"]])
            else:
                st.info(f"El atleta {atleta_seleccionado} aún no ha registrado mediciones.")
        else:
            conn.close()
            st.warning("Todavía no hay atletas registrados.")