
import os
import re
import sqlite3
from io import BytesIO
from datetime import date, datetime

import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(
    page_title="Clientes Cristian Rodriguez",
    page_icon="📊",
    layout="wide"
)

DB_PATH = "clientes_pro.db"


# ============================================================
# DISEÑO PRO - MODO EMPRESA
# ============================================================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top left, rgba(37,99,235,.18), transparent 32%),
        radial-gradient(circle at bottom right, rgba(250,204,21,.28), transparent 34%),
        linear-gradient(135deg, #f8fafc 0%, #eff6ff 55%, #fff7cc 100%);
}
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071426 0%, #12337a 52%, #2563eb 100%);
    border-right: 1px solid rgba(255,255,255,.15);
}
[data-testid="stSidebar"] * {
    color: white !important;
}
.sidebar-title {
    font-size: 17px;
    font-weight: 950;
    color: white;
    margin-top: 12px;
    margin-bottom: 20px;
    letter-spacing: .4px;
}
.sidebar-section {
    font-size: 11px;
    font-weight: 900;
    color: #facc15 !important;
    text-transform: uppercase;
    margin-top: 18px;
    margin-bottom: 8px;
    letter-spacing: .5px;
}
.main-title {
    font-size: 54px;
    font-weight: 950;
    color: #12337a;
    margin-bottom: 1rem;
    letter-spacing: -1.2px;
    text-shadow: 0 4px 14px rgba(37,99,235,.16);
}
.badge {
    display:inline-block;
    padding:9px 18px;
    border-radius:999px;
    font-size:13px;
    font-weight:950;
    background:linear-gradient(135deg,#1d4ed8,#2563eb,#facc15);
    color:white;
    margin-bottom:12px;
    box-shadow: 0 8px 18px rgba(37,99,235,.22);
}
.card {
    background:rgba(255,255,255,.96);
    border:1px solid #93c5fd;
    border-radius:22px;
    padding:20px;
    box-shadow:0 12px 32px rgba(30,64,175,.14);
    margin-bottom:16px;
}
.card-yellow {
    background:linear-gradient(135deg,#eff6ff 0%, #ffffff 48%, #fef3c7 100%);
    border:1px solid #facc15;
    border-radius:24px;
    padding:22px;
    box-shadow:0 14px 34px rgba(37,99,235,.16);
    margin-bottom:16px;
}
.metric-card {
    background:linear-gradient(135deg,#ffffff 0%,#dbeafe 100%);
    border:1px solid #60a5fa;
    border-radius:20px;
    padding:17px;
    box-shadow:0 10px 24px rgba(37,99,235,.14);
    text-align:center;
    min-height: 92px;
}
.metric-label {
    font-size:13px;
    color:#475569;
    font-weight:900;
}
.metric-value {
    font-size:24px;
    color:#1e3a8a;
    font-weight:950;
}
.client-card {
    background: linear-gradient(135deg,#ffffff 0%,#eff6ff 55%,#fef3c7 100%);
    border: 1px solid #60a5fa;
    border-radius: 24px;
    padding: 22px;
    box-shadow: 0 14px 34px rgba(37,99,235,.16);
    margin-bottom: 18px;
}
.client-name {
    font-size: 26px;
    font-weight: 950;
    color: #12337a;
    margin-bottom: 12px;
}
.estado-activo {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    background: #dcfce7;
    color: #166534;
    border: 1px solid #22c55e;
    font-weight: 950;
}
.estado-pre {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    background: #fef3c7;
    color: #92400e;
    border: 1px solid #facc15;
    font-weight: 950;
}
.estado-perdido {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    background: #fee2e2;
    color: #991b1b;
    border: 1px solid #ef4444;
    font-weight: 950;
}
.alert-box {
    background:linear-gradient(135deg,#fff7ed,#ffedd5);
    border:1px solid #fb923c;
    border-radius:16px;
    padding:12px 14px;
    margin-bottom:10px;
    color:#9a3412;
    font-weight:850;
}
.ok-box {
    background:linear-gradient(135deg,#ecfdf5,#dcfce7);
    border:1px solid #22c55e;
    border-radius:16px;
    padding:12px 14px;
    margin-bottom:10px;
    color:#166534;
    font-weight:850;
}
.danger-box {
    background:linear-gradient(135deg,#fef2f2,#fee2e2);
    border:1px solid #ef4444;
    border-radius:16px;
    padding:12px 14px;
    margin-bottom:10px;
    color:#991b1b;
    font-weight:850;
}
.blue-line {
    height: 3px;
    background: linear-gradient(90deg, #1d4ed8, #2563eb, #facc15, transparent);
    margin: 20px 0 24px 0;
    border-radius: 12px;
}
input, textarea {
    background-color:white !important;
    color:#0f172a !important;
}
div[data-baseweb="select"] > div {
    background-color:white !important;
    color:#0f172a !important;
    border-color:#93c5fd !important;
}
div[data-testid="stExpander"] {
    background:white !important;
    border-radius:16px;
    border:1px solid #93c5fd;
    box-shadow: 0 8px 18px rgba(37,99,235,.08);
}
.stButton > button, [data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg,#1d4ed8,#2563eb,#facc15) !important;
    color: white !important;
    border-radius: 14px !important;
    font-weight: 950 !important;
    border: none !important;
}
[data-testid="stSidebar"] [role="radiogroup"] {
    width: 100%;
}
[data-testid="stSidebar"] [role="radiogroup"] label {
    width: 100% !important;
    min-width: 155px !important;
    height: 42px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: rgba(255,255,255,.12) !important;
    border: 1px solid rgba(255,255,255,.22) !important;
    border-radius: 12px !important;
    padding: 0 !important;
    margin-bottom: 9px !important;
    font-weight: 900 !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: linear-gradient(135deg,#2563eb,#facc15) !important;
    border: 1px solid #facc15 !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
    display: none !important;
}
[data-testid="stSidebar"] [role="radiogroup"] p {
    width: 100% !important;
    text-align: center !important;
    font-weight: 900 !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg,#facc15,#eab308) !important;
    border: 1px solid #fde047 !important;
    box-shadow: 0 8px 18px rgba(250,204,21,.35) !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
    color: #0f172a !important;
    font-weight: 950 !important;
}

/* ============================================================
   AJUSTES FINALES PRO: KPI, BOTONES Y TABLAS
   ============================================================ */
.metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #dbeafe 100%) !important;
    border: 2px solid #60a5fa !important;
    border-radius: 20px !important;
    padding: 18px 14px !important;
    box-shadow: 0 12px 28px rgba(37,99,235,.18) !important;
    text-align: center !important;
    min-height: 92px !important;
    margin: 10px 4px 18px 4px !important;
}

.metric-label {
    font-size: 12px !important;
    color: #1e3a8a !important;
    font-weight: 950 !important;
    margin-bottom: 7px !important;
}

.metric-value {
    font-size: 24px !important;
    color: #0f2f79 !important;
    font-weight: 950 !important;
}

div[data-testid="stHorizontalBlock"] {
    gap: 1rem !important;
}

.stButton > button {
    margin-top: 16px !important;
    min-height: 42px !important;
}

div[data-testid="stDataFrame"] {
    background: rgba(255,255,255,.96) !important;
    border: 1px solid #93c5fd !important;
    border-radius: 18px !important;
    padding: 10px !important;
    box-shadow: 0 10px 24px rgba(37,99,235,.10) !important;
}

.pro-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    background: rgba(255,255,255,.97);
    border: 1px solid #93c5fd;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 10px 24px rgba(37,99,235,.10);
    margin-bottom: 22px;
}

.pro-table th {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: white;
    font-weight: 900;
    padding: 12px 10px;
    font-size: 13px;
    text-align: left;
}

.pro-table td {
    padding: 10px;
    font-size: 13px;
    color: #0f172a;
    border-bottom: 1px solid #e5e7eb;
}

.pro-table tr:nth-child(even) td {
    background: #eff6ff;
}

.pro-table tr:hover td {
    background: #dbeafe;
}

.estado-debe {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: #fee2e2;
    color: #991b1b;
    border: 1px solid #ef4444;
    font-weight: 950;
}

.estado-ok {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: #dcfce7;
    color: #166534;
    border: 1px solid #22c55e;
    font-weight: 950;
}


/* Encabezado de tablas con color tipo botón PRO */
.pro-table th {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 65%, #facc15 100%) !important;
    color: white !important;
    font-weight: 950 !important;
    padding: 12px 10px !important;
    font-size: 13px !important;
    text-align: left !important;
    border-bottom: 1px solid #93c5fd !important;
}

.pro-table {
    margin-top: 10px !important;
}


/* Estilo PRO también para dataframes nativos grandes */
div[data-testid="stDataFrame"] {
    background: rgba(255,255,255,.97) !important;
    border: 1px solid #93c5fd !important;
    border-radius: 18px !important;
    padding: 10px !important;
    box-shadow: 0 10px 24px rgba(37,99,235,.10) !important;
}


.pro-table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# UTILIDADES
# ============================================================
def conectar():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def fmt_ars(valor):
    try:
        valor = float(valor)
    except Exception:
        valor = 0
    txt = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"$ {txt}"


def fmt_num(valor, dec=3):
    try:
        valor = float(valor)
    except Exception:
        valor = 0
    return f"{valor:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(valor):
    try:
        valor = float(valor)
    except Exception:
        valor = 0
    return f"{valor:.1f}%"


def metric_card(label, value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)



def colorear_estado_html(valor):
    valor_txt = str(valor).strip()
    if valor_txt.lower() == "debe":
        return '<span class="estado-debe">Debe</span>'
    if valor_txt.lower() in ["al día", "al dia"]:
        return '<span class="estado-ok">Al día</span>'
    return valor_txt


def colorear_estado_html(valor):
    valor_txt = str(valor).strip()
    if valor_txt.lower() == "debe":
        return '<span class="estado-debe">Debe</span>'
    if valor_txt.lower() in ["al día", "al dia"]:
        return '<span class="estado-ok">Al día</span>'
    return valor_txt


def mostrar_tabla_pro(df, columnas=None, alto=None):
    if df is None or df.empty:
        st.info("No hay datos para mostrar.")
        return

    tabla = df.copy()

    if columnas:
        columnas_ok = [c for c in columnas if c in tabla.columns]
        tabla = tabla[columnas_ok]

    if "Estado Cuenta" in tabla.columns:
        tabla["Estado Cuenta"] = tabla["Estado Cuenta"].apply(colorear_estado_html)

    for col in tabla.columns:
        if col in ["Total Vendido", "Total Cobrado", "Saldo Pendiente", "Facturación", "Importe", "Precio Lista", "Precio Venta", "Pagos Manuales", "Cobrado por Pedido", "Comisión Total", "Comisión Venta", "Comisión Cobranza", "Comisión Cobranza Externa"]:
            tabla[col] = pd.to_numeric(tabla[col], errors="coerce").fillna(0).apply(fmt_ars)
        elif col in ["Toneladas"]:
            tabla[col] = pd.to_numeric(tabla[col], errors="coerce").fillna(0).apply(lambda x: fmt_num(x, 3))
        elif "Porcentaje" in col:
            tabla[col] = pd.to_numeric(tabla[col], errors="coerce").fillna(0).apply(lambda x: f"{x:.3f}%")

    if len(tabla) <= 500:
        st.markdown(tabla.to_html(escape=False, index=False, classes="pro-table"), unsafe_allow_html=True)
    else:
        if alto is None:
            st.dataframe(tabla, use_container_width=True)
        else:
            st.dataframe(tabla, use_container_width=True, height=alto)



def limpiar_txt(x):
    return str(x).strip() if pd.notna(x) else ""


def buscar_columna(df, opciones):
    cols_norm = {str(c).strip().lower(): c for c in df.columns}
    for op in opciones:
        if op.lower() in cols_norm:
            return cols_norm[op.lower()]
    for c in df.columns:
        for op in opciones:
            if op.lower() in str(c).strip().lower():
                return c
    return None


def extraer_kilos(presentacion):
    txt = limpiar_txt(presentacion).lower().replace(" ", "")
    m = re.search(r"(\d+(?:[.,]\d+)?)x(\d+(?:[.,]\d+)?)", txt)
    if m:
        return float(m.group(1).replace(",", ".")) * float(m.group(2).replace(",", "."))
    m = re.search(r"(\d+(?:[.,]\d+)?)", txt)
    if m:
        return float(m.group(1).replace(",", "."))
    return 0.0


def ciclo_comercial(fecha=None):
    fecha = pd.Timestamp.today().normalize() if fecha is None else pd.Timestamp(fecha).normalize()
    if fecha.day >= 26:
        inicio = pd.Timestamp(fecha.year, fecha.month, 26)
        fin = inicio + pd.DateOffset(months=1) - pd.DateOffset(days=1)
    else:
        fin = pd.Timestamp(fecha.year, fecha.month, 25)
        inicio = fin - pd.DateOffset(months=1) + pd.DateOffset(days=1)
    return inicio.normalize(), fin.normalize()


def regla_cobranza(dias):
    if dias <= 14:
        return 0.015, "1,5% hasta 14 días"
    if dias <= 21:
        return 0.01, "1% hasta 21 días"
    if dias <= 25:
        return 0.0, "0% entre 22 y 25 días"
    return 0.005, "0,5% después del día 25"


def estado_cliente(dias):
    if pd.isna(dias):
        return "Perdido"
    if dias <= 30:
        return "Activo"
    if dias < 90:
        return "Pre-perdido"
    return "Perdido"


def clase_estado(estado):
    if estado == "Activo":
        return "estado-activo"
    if estado == "Pre-perdido":
        return "estado-pre"
    return "estado-perdido"


def prioridad_visita(estado):
    if estado == "Perdido":
        return 1
    if estado == "Pre-perdido":
        return 2
    return 3


def progreso(actual, meta):
    if meta <= 0:
        return 0
    return min(float(actual) / float(meta), 1)


def texto_objetivo(actual, meta):
    if meta <= 0:
        return "Sin meta"
    return f"{(float(actual) / float(meta)) * 100:.1f}%"


def descargar_excel(hojas):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for nombre, df in hojas.items():
            if df is None:
                df = pd.DataFrame()
            df.to_excel(writer, index=False, sheet_name=nombre[:31])
    return output.getvalue()


# ============================================================
# BASE DE DATOS
# ============================================================
def crear_tablas():
    con = conectar()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT UNIQUE,
        vendedor TEXT,
        cuenta TEXT,
        cuit TEXT,
        direccion TEXT,
        telefono TEXT,
        mail TEXT,
        localidad TEXT,
        provincia TEXT,
        estado TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id TEXT,
        cliente TEXT,
        fecha TEXT,
        hora_pedido TEXT,
        fechahora_pedido TEXT,
        producto TEXT,
        presentacion TEXT,
        cantidad_bultos REAL,
        kilos_por_bulto REAL,
        precio_lista REAL,
        precio_venta REAL,
        importe REAL,
        toneladas REAL,
        cobrado TEXT,
        fecha_cobro TEXT,
        dias_al_cobro REAL,
        porcentaje_cobranza REAL,
        regla_cobranza TEXT,
        comision_venta REAL,
        comision_cobranza REAL,
        comision_total REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pagos (
        id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        hora TEXT,
        cliente TEXT,
        monto_abonado REAL,
        medio_pago TEXT,
        observacion TEXT,
        aplicado_a_pedido TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS notas_credito (
        id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        hora TEXT,
        cliente TEXT,
        pedido_id TEXT,
        monto_nota REAL,
        motivo TEXT,
        observacion TEXT,
        comision_venta_descontada REAL DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS visitas (
        id_visita INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        hora TEXT,
        cliente TEXT,
        estado_cliente TEXT,
        dias_sin_comprar REAL,
        resultado TEXT,
        observacion TEXT,
        proxima_accion TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS objetivos (
        periodo TEXT PRIMARY KEY,
        meta_facturacion REAL,
        meta_toneladas REAL,
        meta_pedidos REAL,
        fecha_actualizacion TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cierres (
        periodo TEXT PRIMARY KEY,
        fecha_cierre TEXT,
        pedidos REAL,
        facturacion REAL,
        toneladas REAL,
        comision_total REAL
    )
    """)

    con.commit()
    con.close()



def asegurar_columna(tabla, columna, tipo_sql):
    con = conectar()
    cur = con.cursor()
    cur.execute(f"PRAGMA table_info({tabla})")
    columnas = [fila[1] for fila in cur.fetchall()]
    if columna not in columnas:
        cur.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {tipo_sql}")
        con.commit()
    con.close()


def preparar_base_modo_empresa():
    # Columnas para fecha de entrega real.
    asegurar_columna("pedidos", "fecha_entrega", "TEXT")
    asegurar_columna("notas_credito", "fecha_entrega", "TEXT")

    # Columnas extra para pagos externos/no cargados en pedidos.
    asegurar_columna("pagos", "tipo_pago", "TEXT DEFAULT 'Pago manual'")
    asegurar_columna("pagos", "pedido_externo", "TEXT")
    asegurar_columna("pagos", "fecha_pedido_externo", "TEXT")
    asegurar_columna("pagos", "fecha_entrega_externa", "TEXT")
    asegurar_columna("pagos", "importe_pedido_externo", "REAL DEFAULT 0")
    asegurar_columna("pagos", "dias_al_cobro_externo", "REAL DEFAULT 0")
    asegurar_columna("pagos", "regla_cobranza_externa", "TEXT")
    asegurar_columna("pagos", "comision_cobranza_externa", "REAL DEFAULT 0")

    # Columnas extra para comisión de venta por producto.
    asegurar_columna("pedidos", "categoria_comision_venta", "TEXT")
    asegurar_columna("pedidos", "porcentaje_comision_venta", "REAL DEFAULT 0")

    con = conectar()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS comisiones_venta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT UNIQUE,
        palabras_clave TEXT,
        hasta_250 REAL,
        desde_250_500 REAL,
        mas_500 REAL,
        porcentaje_fijo REAL DEFAULT 0,
        prioridad REAL DEFAULT 100
    )
    """)

    # Reglas base actualizadas.
    # 0000 y 000 comunes se consideran "Blancas" = 1,5%.
    # "Acondicionadas 0000/000" solo aplica si el producto dice literalmente "acondicionada".
    # Semolín/Semolin se incorpora a Blancas para que no quede sin comisión.
    defaults = [
        ("Aceite y Mayonesa", "aceite,mayonesa", 0.50, 0.50, 0.50, 0.50, 1),
        ("Terminadas premium", "terminada premium,terminadas premium,premium terminada,premium terminadas", 2.00, 1.00, 0.500, 0, 2),
        ("Premium/Int/Reb/Adit", "premium,integral,int,reb,adit,aditivada", 5.00, 2.50, 1.250, 0, 3),
        ("Premezclas", "premezcla,premezclas,chipa", 2.00, 1.00, 0.500, 0, 4),
        ("Acondicionadas 0000", "acondicionada 0000,acondicionadas 0000", 2.00, 1.00, 0.500, 0, 5),
        ("Acondicionadas 000", "acondicionada 000,acondicionadas 000", 1.00, 0.50, 0.250, 0, 6),
        ("Blancas", "blanca,blancas,harina 0000,0000,semolin,semolín,semola,sémola", 1.50, 0.75, 0.375, 0, 7),
        ("Subp Espe", "subp,subproducto,especial,espe", 3.00, 1.50, 0.750, 0, 8),
        ("Terminadas", "terminada,terminadas", 1.00, 0.50, 0.250, 0, 9),
        ("Commodities", "commodity,commodities,000,harina 000", 0.50, 0.25, 0.125, 0, 10),
    ]
    cur.executemany("""
        INSERT OR REPLACE INTO comisiones_venta
        (categoria, palabras_clave, hasta_250, desde_250_500, mas_500, porcentaje_fijo, prioridad)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, defaults)
    con.commit()
    con.close()


def cargar_comisiones_venta():
    con = conectar()
    df = pd.read_sql_query("SELECT * FROM comisiones_venta ORDER BY prioridad ASC, id ASC", con)
    con.close()
    return df


def normalizar_busqueda(txt):
    txt = limpiar_txt(txt).lower()
    reemplazos = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "ä": "a", "ë": "e", "ï": "i", "ö": "o", "ü": "u",
    }
    for a, b in reemplazos.items():
        txt = txt.replace(a, b)
    return txt


def calcular_porcentaje_comision_venta(producto, total_facturado_cliente, df_comisiones):
    producto_txt = normalizar_busqueda(producto)

    # Reglas críticas directas para evitar errores de clasificación.
    # Semolín/Semolin/Sémola = Blancas.
    if "semolin" in producto_txt or "semola" in producto_txt:
        if total_facturado_cliente <= 250_000_000:
            return 1.50, "Blancas"
        elif total_facturado_cliente <= 500_000_000:
            return 0.75, "Blancas"
        else:
            return 0.375, "Blancas"

    # Chipa = Premezclas.
    if "chipa" in producto_txt:
        if total_facturado_cliente <= 250_000_000:
            return 2.00, "Premezclas"
        elif total_facturado_cliente <= 500_000_000:
            return 1.00, "Premezclas"
        else:
            return 0.500, "Premezclas"

    # 0000 común = Blancas. 000 común = Commodities.
    # Si dice acondicionada/acondicionadas, se deja seguir a la tabla.
    if "acondicionad" not in producto_txt:
        if "0000" in producto_txt:
            if total_facturado_cliente <= 250_000_000:
                return 1.50, "Blancas"
            elif total_facturado_cliente <= 500_000_000:
                return 0.75, "Blancas"
            else:
                return 0.375, "Blancas"

        if "000" in producto_txt and "0000" not in producto_txt:
            if total_facturado_cliente <= 250_000_000:
                return 0.50, "Commodities"
            elif total_facturado_cliente <= 500_000_000:
                return 0.25, "Commodities"
            else:
                return 0.125, "Commodities"

    if df_comisiones is None or df_comisiones.empty:
        return 0.0, "Sin regla"

    for _, regla in df_comisiones.iterrows():
        claves = normalizar_busqueda(regla.get("palabras_clave", ""))
        lista_claves = [normalizar_busqueda(c) for c in claves.split(",") if normalizar_busqueda(c)]

        if any(clave in producto_txt for clave in lista_claves):
            fijo = float(pd.to_numeric(regla.get("porcentaje_fijo", 0), errors="coerce") or 0)
            if fijo > 0:
                return fijo, limpiar_txt(regla.get("categoria", ""))

            if total_facturado_cliente <= 250_000_000:
                pct = float(pd.to_numeric(regla.get("hasta_250", 0), errors="coerce") or 0)
            elif total_facturado_cliente <= 500_000_000:
                pct = float(pd.to_numeric(regla.get("desde_250_500", 0), errors="coerce") or 0)
            else:
                pct = float(pd.to_numeric(regla.get("mas_500", 0), errors="coerce") or 0)

            return pct, limpiar_txt(regla.get("categoria", ""))

    return 0.0, "Sin regla"

    for _, regla in df_comisiones.iterrows():
        claves = normalizar_busqueda(regla.get("palabras_clave", ""))
        lista_claves = [normalizar_busqueda(c) for c in claves.split(",") if normalizar_busqueda(c)]

        if any(clave in producto_txt for clave in lista_claves):
            fijo = float(pd.to_numeric(regla.get("porcentaje_fijo", 0), errors="coerce") or 0)
            if fijo > 0:
                return fijo, limpiar_txt(regla.get("categoria", ""))

            if total_facturado_cliente <= 250_000_000:
                pct = float(pd.to_numeric(regla.get("hasta_250", 0), errors="coerce") or 0)
            elif total_facturado_cliente <= 500_000_000:
                pct = float(pd.to_numeric(regla.get("desde_250_500", 0), errors="coerce") or 0)
            else:
                pct = float(pd.to_numeric(regla.get("mas_500", 0), errors="coerce") or 0)

            return pct, limpiar_txt(regla.get("categoria", ""))

    return 0.0, "Sin regla"


def recalcular_comisiones_venta_en_memoria_y_db(df_pedidos_actual, df_comisiones):
    if df_pedidos_actual is None or df_pedidos_actual.empty:
        return df_pedidos_actual

    df = df_pedidos_actual.copy()
    total_cliente_map = df.groupby("Cliente")["Importe"].sum().to_dict()

    con = conectar()
    for idx, r in df.iterrows():
        total_cliente = float(total_cliente_map.get(r.get("Cliente"), 0) or 0)
        pct, categoria = calcular_porcentaje_comision_venta(r.get("Producto", ""), total_cliente, df_comisiones)

        importe = float(pd.to_numeric(r.get("Importe", 0), errors="coerce") or 0)
        comision_cobranza = float(pd.to_numeric(r.get("Comisión Cobranza", 0), errors="coerce") or 0)

        comision_venta = importe * (pct / 100)
        comision_total = comision_venta + comision_cobranza

        df.at[idx, "Porcentaje Comisión Venta"] = pct
        df.at[idx, "Categoría Comisión Venta"] = categoria
        df.at[idx, "Comisión Venta"] = comision_venta
        df.at[idx, "Comisión Total"] = comision_total

        if "id" in df.columns and pd.notna(r.get("id")):
            con.execute("""
                UPDATE pedidos
                SET porcentaje_comision_venta=?,
                    categoria_comision_venta=?,
                    comision_venta=?,
                    comision_total=?
                WHERE id=?
            """, (pct, categoria, comision_venta, comision_total, int(r.get("id"))))

    con.commit()
    con.close()
    return df

def tabla_vacia(nombre):
    con = conectar()
    total = pd.read_sql_query(f"SELECT COUNT(*) AS total FROM {nombre}", con)["total"].iloc[0]
    con.close()
    return total == 0


def leer_sql(tabla):
    con = conectar()
    df = pd.read_sql_query(f"SELECT * FROM {tabla}", con)
    con.close()
    return df


def migrar_excel_a_sqlite():
    con = conectar()

    if tabla_vacia("clientes") and os.path.exists("clientes.xlsx"):
        try:
            df = pd.read_excel("clientes.xlsx", header=1)
            df.columns = [str(c).strip() for c in df.columns]
            col_cliente = buscar_columna(df, ["Cliente", "Razón social", "Razon social", "Nombre"])
            if col_cliente:
                df = df.rename(columns={col_cliente: "Cliente"})
                for _, r in df.iterrows():
                    cliente = limpiar_txt(r.get("Cliente", ""))
                    if cliente:
                        con.execute(
                            """
                            INSERT OR IGNORE INTO clientes
                            (cliente, vendedor, cuenta, cuit, direccion, telefono, mail, localidad, provincia, estado)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                cliente,
                                limpiar_txt(r.get("Vendedor", "")),
                                limpiar_txt(r.get("Cuenta", "")),
                                limpiar_txt(r.get("CUIT", "")),
                                limpiar_txt(r.get("Dirección", r.get("Direccion", ""))),
                                limpiar_txt(r.get("Teléfono", r.get("Telefono", ""))),
                                limpiar_txt(r.get("Mail", "")),
                                limpiar_txt(r.get("Localidad", "")),
                                limpiar_txt(r.get("Provincia", "")),
                                limpiar_txt(r.get("Estado", "")),
                            ),
                        )
                con.commit()
        except Exception as e:
            st.warning(f"No pude migrar clientes.xlsx: {e}")

    if tabla_vacia("pedidos") and os.path.exists("pedidos_diarios.xlsx"):
        try:
            df = pd.read_excel("pedidos_diarios.xlsx")
            df.columns = [str(c).strip() for c in df.columns]
            df = df.rename(
                columns={
                    "Hora": "Hora Pedido",
                    "Bultos": "Cantidad Bultos",
                    "Kilos": "Kilos por Bulto",
                    "Precio": "Precio Venta",
                    "Comision Venta": "Comisión Venta",
                    "Comision Cobranza": "Comisión Cobranza",
                    "Comision Total": "Comisión Total",
                }
            )

            for _, r in df.iterrows():
                fecha = pd.to_datetime(r.get("Fecha", None), errors="coerce")
                fecha_cobro = pd.to_datetime(r.get("Fecha Cobro", None), errors="coerce")
                fechahora = pd.to_datetime(r.get("FechaHora Pedido", None), errors="coerce")

                con.execute(
                    """
                    INSERT INTO pedidos (
                        pedido_id, cliente, fecha, hora_pedido, fechahora_pedido, producto, presentacion,
                        cantidad_bultos, kilos_por_bulto, precio_lista, precio_venta, importe, toneladas,
                        cobrado, fecha_cobro, dias_al_cobro, porcentaje_cobranza, regla_cobranza,
                        comision_venta, comision_cobranza, comision_total
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        limpiar_txt(r.get("Pedido ID", "")),
                        limpiar_txt(r.get("Cliente", "")),
                        str(fecha.date()) if pd.notna(fecha) else "",
                        limpiar_txt(r.get("Hora Pedido", "")),
                        str(fechahora) if pd.notna(fechahora) else "",
                        limpiar_txt(r.get("Producto", "")),
                        limpiar_txt(r.get("Presentacion", "")),
                        float(pd.to_numeric(r.get("Cantidad Bultos", 0), errors="coerce") or 0),
                        float(pd.to_numeric(r.get("Kilos por Bulto", 0), errors="coerce") or 0),
                        float(pd.to_numeric(r.get("Precio Lista", 0), errors="coerce") or 0),
                        float(pd.to_numeric(r.get("Precio Venta", 0), errors="coerce") or 0),
                        float(pd.to_numeric(r.get("Importe", 0), errors="coerce") or 0),
                        float(pd.to_numeric(r.get("Toneladas", 0), errors="coerce") or 0),
                        limpiar_txt(r.get("Cobrado", "No")) or "No",
                        str(fecha_cobro.date()) if pd.notna(fecha_cobro) else "",
                        float(pd.to_numeric(r.get("Dias al Cobro", 0), errors="coerce") or 0),
                        float(pd.to_numeric(r.get("Porcentaje Cobranza", 0), errors="coerce") or 0),
                        limpiar_txt(r.get("Regla Cobranza", "")),
                        float(pd.to_numeric(r.get("Comisión Venta", 0), errors="coerce") or 0),
                        float(pd.to_numeric(r.get("Comisión Cobranza", 0), errors="coerce") or 0),
                        float(pd.to_numeric(r.get("Comisión Total", 0), errors="coerce") or 0),
                    ),
                )
            con.commit()
        except Exception as e:
            st.warning(f"No pude migrar pedidos_diarios.xlsx: {e}")

    if tabla_vacia("pagos") and os.path.exists("pagos_clientes.xlsx"):
        try:
            df = pd.read_excel("pagos_clientes.xlsx")
            df.columns = [str(c).strip() for c in df.columns]
            for _, r in df.iterrows():
                fecha = pd.to_datetime(r.get("Fecha", None), errors="coerce")
                con.execute(
                    """
                    INSERT INTO pagos (fecha, hora, cliente, monto_abonado, medio_pago, observacion, aplicado_a_pedido)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(fecha.date()) if pd.notna(fecha) else "",
                        limpiar_txt(r.get("Hora", "")),
                        limpiar_txt(r.get("Cliente", "")),
                        float(pd.to_numeric(r.get("Monto Abonado", 0), errors="coerce") or 0),
                        limpiar_txt(r.get("Medio de Pago", "")),
                        limpiar_txt(r.get("Observación", "")),
                        limpiar_txt(r.get("Aplicado a Pedido", "")),
                    ),
                )
            con.commit()
        except Exception as e:
            st.warning(f"No pude migrar pagos_clientes.xlsx: {e}")

    if tabla_vacia("visitas") and os.path.exists("visitas.xlsx"):
        try:
            df = pd.read_excel("visitas.xlsx")
            df.columns = [str(c).strip() for c in df.columns]
            for _, r in df.iterrows():
                fecha = pd.to_datetime(r.get("Fecha", None), errors="coerce")
                con.execute(
                    """
                    INSERT INTO visitas (fecha, hora, cliente, estado_cliente, dias_sin_comprar, resultado, observacion, proxima_accion)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(fecha.date()) if pd.notna(fecha) else "",
                        limpiar_txt(r.get("Hora", "")),
                        limpiar_txt(r.get("Cliente", "")),
                        limpiar_txt(r.get("Estado Cliente", "")),
                        float(pd.to_numeric(r.get("Dias sin comprar", 0), errors="coerce") or 0),
                        limpiar_txt(r.get("Resultado", "")),
                        limpiar_txt(r.get("Observación", "")),
                        limpiar_txt(r.get("Próxima acción", "")),
                    ),
                )
            con.commit()
        except Exception as e:
            st.warning(f"No pude migrar visitas.xlsx: {e}")

    con.close()


def cargar_precios():
    if not os.path.exists("precios.xlsx"):
        st.error("No encontré precios.xlsx")
        st.stop()

    try:
        df = pd.read_excel("precios.xlsx", sheet_name="Contact Center", header=2)
        df.columns = [str(c).strip() for c in df.columns]
    except Exception:
        df = pd.read_excel("precios.xlsx")
        df.columns = [str(c).strip() for c in df.columns]

    col_producto = buscar_columna(df, ["Producto", "PRODUCTO", "Articulo", "Artículo", "Descripcion", "Descripción"])
    col_presentacion = buscar_columna(df, ["Presentacion", "Presentación", "Envase", "ENVASE", "Unidad"])
    col_precio = buscar_columna(df, ["Precio (*)", "Precio", "PRECIO", "Lista", "Precio Lista"])

    if col_producto is None or col_precio is None:
        st.error("No pude detectar Producto o Precio en precios.xlsx")
        st.write(df.columns.tolist())
        st.stop()

    if col_presentacion is None:
        df["Presentacion"] = ""
        col_presentacion = "Presentacion"

    df = df.rename(columns={col_producto: "Producto", col_presentacion: "Presentacion", col_precio: "Precio Lista"})
    df["Producto"] = df["Producto"].astype(str).str.strip()
    df["Presentacion"] = df["Presentacion"].astype(str).str.strip()
    df["Precio Lista"] = pd.to_numeric(df["Precio Lista"], errors="coerce")
    df = df.dropna(subset=["Producto", "Precio Lista"])
    df = df[df["Producto"] != ""]
    df = df[df["Precio Lista"] > 0]
    df["Kilos por Bulto"] = df["Presentacion"].apply(extraer_kilos)
    return df.drop_duplicates(subset=["Producto"])


# ============================================================
# INICIAR DATOS
# ============================================================
crear_tablas()
preparar_base_modo_empresa()
migrar_excel_a_sqlite()

df_clientes = leer_sql("clientes")
df_pedidos = leer_sql("pedidos")
df_pagos = leer_sql("pagos")
df_notas_credito = leer_sql("notas_credito")
df_visitas = leer_sql("visitas")
df_objetivos = leer_sql("objetivos")
df_precios = cargar_precios()
df_comisiones_venta = cargar_comisiones_venta()

df_clientes = df_clientes.rename(
    columns={
        "cliente": "Cliente",
        "vendedor": "Vendedor",
        "cuenta": "Cuenta",
        "cuit": "CUIT",
        "direccion": "Dirección",
        "telefono": "Teléfono",
        "mail": "Mail",
        "localidad": "Localidad",
        "provincia": "Provincia",
        "estado": "Estado",
    }
)

df_pedidos = df_pedidos.rename(
    columns={
        "pedido_id": "Pedido ID",
        "cliente": "Cliente",
        "fecha": "Fecha",
        "hora_pedido": "Hora Pedido",
        "fechahora_pedido": "FechaHora Pedido",
        "producto": "Producto",
        "presentacion": "Presentacion",
        "cantidad_bultos": "Cantidad Bultos",
        "kilos_por_bulto": "Kilos por Bulto",
        "precio_lista": "Precio Lista",
        "precio_venta": "Precio Venta",
        "importe": "Importe",
        "toneladas": "Toneladas",
        "cobrado": "Cobrado",
        "fecha_cobro": "Fecha Cobro",
        "fecha_entrega": "Fecha Entrega",
        "dias_al_cobro": "Dias al Cobro",
        "porcentaje_cobranza": "Porcentaje Cobranza",
        "regla_cobranza": "Regla Cobranza",
        "comision_venta": "Comisión Venta",
        "comision_cobranza": "Comisión Cobranza",
        "comision_total": "Comisión Total",
        "categoria_comision_venta": "Categoría Comisión Venta",
        "porcentaje_comision_venta": "Porcentaje Comisión Venta",
    }
)

df_pagos = df_pagos.rename(
    columns={
        "id_pago": "ID Pago",
        "fecha": "Fecha",
        "hora": "Hora",
        "cliente": "Cliente",
        "monto_abonado": "Monto Abonado",
        "medio_pago": "Medio de Pago",
        "observacion": "Observación",
        "aplicado_a_pedido": "Aplicado a Pedido",
        "tipo_pago": "Tipo Pago",
        "pedido_externo": "Pedido Externo",
        "fecha_pedido_externo": "Fecha Pedido Externo",
        "fecha_entrega_externa": "Fecha Entrega Externa",
        "importe_pedido_externo": "Importe Pedido Externo",
        "dias_al_cobro_externo": "Dias al Cobro Externo",
        "regla_cobranza_externa": "Regla Cobranza Externa",
        "comision_cobranza_externa": "Comisión Cobranza Externa",
    }
)

df_notas_credito = df_notas_credito.rename(
    columns={
        "id_nota": "ID Nota",
        "fecha": "Fecha",
        "hora": "Hora",
        "cliente": "Cliente",
        "pedido_id": "Pedido ID",
        "fecha_entrega": "Fecha Entrega",
        "monto_nota": "Monto Nota",
        "motivo": "Motivo",
        "observacion": "Observación",
        "comision_venta_descontada": "Comisión Venta Descontada",
    }
)

df_visitas = df_visitas.rename(
    columns={
        "id_visita": "ID Visita",
        "fecha": "Fecha",
        "hora": "Hora",
        "cliente": "Cliente",
        "estado_cliente": "Estado Cliente",
        "dias_sin_comprar": "Dias sin comprar",
        "resultado": "Resultado",
        "observacion": "Observación",
        "proxima_accion": "Próxima acción",
    }
)

df_objetivos = df_objetivos.rename(
    columns={
        "periodo": "Periodo",
        "meta_facturacion": "Meta Facturación",
        "meta_toneladas": "Meta Toneladas",
        "meta_pedidos": "Meta Pedidos",
        "fecha_actualizacion": "Fecha Actualización",
    }
)

for df, cols_fecha in [
    (df_pedidos, ["Fecha", "Fecha Cobro", "Fecha Entrega", "FechaHora Pedido"]),
    (df_pagos, ["Fecha", "Fecha Pedido Externo", "Fecha Entrega Externa"]),
    (df_visitas, ["Fecha"]),
    (df_notas_credito, ["Fecha", "Fecha Entrega"]),
]:
    for c in cols_fecha:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")

for c in [
    "Importe",
    "Toneladas",
    "Comisión Venta",
    "Comisión Cobranza",
    "Comisión Total",
    "Cantidad Bultos",
    "Kilos por Bulto",
    "Precio Lista",
    "Precio Venta",
]:
    if c in df_pedidos.columns:
        df_pedidos[c] = pd.to_numeric(df_pedidos[c], errors="coerce").fillna(0)

if "Monto Abonado" in df_pagos.columns:
    df_pagos["Monto Abonado"] = pd.to_numeric(df_pagos["Monto Abonado"], errors="coerce").fillna(0)

for c in ["Importe Pedido Externo", "Dias al Cobro Externo", "Comisión Cobranza Externa"]:
    if c in df_pagos.columns:
        df_pagos[c] = pd.to_numeric(df_pagos[c], errors="coerce").fillna(0)

for c in ["Monto Nota", "Comisión Venta Descontada"]:
    if c in df_notas_credito.columns:
        df_notas_credito[c] = pd.to_numeric(df_notas_credito[c], errors="coerce").fillna(0)

# Recalcula comisión de venta por producto y rango de facturación.
df_pedidos = recalcular_comisiones_venta_en_memoria_y_db(df_pedidos, df_comisiones_venta)


# ============================================================
# RESÚMENES Y CÁLCULOS
# ============================================================
inicio_ciclo, fin_ciclo = ciclo_comercial()
periodo_actual = f"{inicio_ciclo.strftime('%d/%m/%Y')} al {fin_ciclo.strftime('%d/%m/%Y')}"

df_ciclo = (
    df_pedidos[
        (df_pedidos["Fecha"].dt.normalize() >= inicio_ciclo)
        & (df_pedidos["Fecha"].dt.normalize() <= fin_ciclo)
    ].copy()
    if not df_pedidos.empty
    else df_pedidos.copy()
)

df_pagos_ciclo = (
    df_pagos[
        (df_pagos["Fecha"].dt.normalize() >= inicio_ciclo)
        & (df_pagos["Fecha"].dt.normalize() <= fin_ciclo)
    ].copy()
    if not df_pagos.empty
    else df_pagos.copy()
)

ultima_compra = (
    df_pedidos.groupby("Cliente", as_index=False)["Fecha"].max().rename(columns={"Fecha": "Ultima Compra"})
    if not df_pedidos.empty
    else pd.DataFrame(columns=["Cliente", "Ultima Compra"])
)

visitas_vendi = (
    df_visitas[df_visitas["Resultado"].astype(str).str.lower().isin(["vendí", "vendi"])].copy()
    if not df_visitas.empty
    else df_visitas.copy()
)

ultima_visita_venta = (
    visitas_vendi.groupby("Cliente", as_index=False)["Fecha"].max().rename(columns={"Fecha": "Ultima Visita Venta"})
    if not visitas_vendi.empty
    else pd.DataFrame(columns=["Cliente", "Ultima Visita Venta"])
)

df_final = df_clientes.merge(ultima_compra, on="Cliente", how="left")
df_final = df_final.merge(ultima_visita_venta, on="Cliente", how="left")

df_final["Referencia Comercial"] = df_final["Ultima Compra"]
mask_ref = df_final["Referencia Comercial"].isna() | (
    pd.to_datetime(df_final["Ultima Visita Venta"], errors="coerce")
    > pd.to_datetime(df_final["Referencia Comercial"], errors="coerce")
)
df_final.loc[mask_ref, "Referencia Comercial"] = df_final.loc[mask_ref, "Ultima Visita Venta"]

df_final["Dias sin comprar"] = (
    pd.Timestamp.today().normalize() - pd.to_datetime(df_final["Referencia Comercial"], errors="coerce")
).dt.days
df_final["Estado Comercial"] = df_final["Dias sin comprar"].apply(estado_cliente)

obj_actual = df_objetivos[df_objetivos["Periodo"] == periodo_actual] if not df_objetivos.empty else pd.DataFrame()

if obj_actual.empty:
    meta_facturacion = 0.0
    meta_toneladas = 0.0
    meta_pedidos = 0.0
else:
    meta_facturacion = float(obj_actual.iloc[0]["Meta Facturación"])
    meta_toneladas = float(obj_actual.iloc[0]["Meta Toneladas"])
    meta_pedidos = float(obj_actual.iloc[0]["Meta Pedidos"])

ventas_cliente = (
    df_pedidos.groupby("Cliente", as_index=False)
    .agg({"Importe": "sum", "Pedido ID": "nunique"})
    .rename(columns={"Importe": "Total Vendido", "Pedido ID": "Pedidos"})
    if not df_pedidos.empty
    else pd.DataFrame(columns=["Cliente", "Total Vendido", "Pedidos"])
)

pedidos_cobrados_cliente = (
    df_pedidos[df_pedidos["Cobrado"] == "Sí"]
    .groupby("Cliente", as_index=False)["Importe"]
    .sum()
    .rename(columns={"Importe": "Cobrado por Pedido"})
    if not df_pedidos.empty
    else pd.DataFrame(columns=["Cliente", "Cobrado por Pedido"])
)

pagos_cliente = (
    df_pagos.groupby("Cliente", as_index=False)["Monto Abonado"]
    .sum()
    .rename(columns={"Monto Abonado": "Pagos Manuales"})
    if not df_pagos.empty
    else pd.DataFrame(columns=["Cliente", "Pagos Manuales"])
)

notas_cliente = (
    df_notas_credito.groupby("Cliente", as_index=False)["Monto Nota"]
    .sum()
    .rename(columns={"Monto Nota": "Notas de Crédito"})
    if not df_notas_credito.empty
    else pd.DataFrame(columns=["Cliente", "Notas de Crédito"])
)

cuenta_corriente = df_clientes[["Cliente"]].drop_duplicates().copy()
cuenta_corriente = cuenta_corriente.merge(ventas_cliente, on="Cliente", how="left")
cuenta_corriente = cuenta_corriente.merge(pedidos_cobrados_cliente, on="Cliente", how="left")
cuenta_corriente = cuenta_corriente.merge(pagos_cliente, on="Cliente", how="left")
cuenta_corriente = cuenta_corriente.merge(notas_cliente, on="Cliente", how="left")

for c in ["Total Vendido", "Pedidos", "Cobrado por Pedido", "Pagos Manuales", "Notas de Crédito"]:
    cuenta_corriente[c] = pd.to_numeric(cuenta_corriente[c], errors="coerce").fillna(0)

cuenta_corriente["Total Cobrado"] = cuenta_corriente["Cobrado por Pedido"] + cuenta_corriente["Pagos Manuales"]
cuenta_corriente["Venta Neta"] = cuenta_corriente["Total Vendido"] - cuenta_corriente["Notas de Crédito"]
cuenta_corriente["Saldo Pendiente"] = cuenta_corriente["Venta Neta"] - cuenta_corriente["Total Cobrado"]
cuenta_corriente["Estado Cuenta"] = cuenta_corriente["Saldo Pendiente"].apply(lambda x: "Debe" if x > 0 else "Al día")
cuenta_corriente = cuenta_corriente.sort_values("Saldo Pendiente", ascending=False)


# ============================================================
# SIDEBAR
# ============================================================
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=170)

st.sidebar.markdown('<div class="sidebar-title">CRISTIAN RODRIGUEZ</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-section">Panel principal</div>', unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Menú",
    [
        "Inicio",
        "Pedidos",
        "Cobranza",
        "Pagos",
        "Notas de Crédito",
        "Cuenta Corriente",
        "Visitas",
        "Objetivos",
        "Inteligencia",
        "Clientes",
        "Productos",
        "Ciclo comercial",
        "Informes",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.write(f"**Ciclo:** {periodo_actual}")
st.sidebar.write(f"**Pedidos ciclo:** {len(df_ciclo)}")
st.sidebar.write("**Base:** SQLite")

st.markdown(f'<div class="main-title">{menu.upper()}</div>', unsafe_allow_html=True)


# ============================================================
# FILTROS GENERALES
# ============================================================
with st.expander("Filtros generales", expanded=(menu == "Inicio")):
    f1, f2, f3, f4 = st.columns(4)

    buscar = f1.text_input("Buscar cliente", placeholder="Escribí para buscar...")
    estado_sel = f2.selectbox("Estado Comercial", ["Todos", "Activo", "Pre-perdido", "Perdido"])

    if "Vendedor" in df_final.columns:
        vendedor_sel = f3.selectbox(
            "Vendedor",
            ["Todos"] + sorted(df_final["Vendedor"].dropna().astype(str).unique().tolist()),
        )
    else:
        vendedor_sel = "Todos"

    clientes_opciones = ["Todos"] + sorted(df_final["Cliente"].dropna().astype(str).unique().tolist())
    cliente_select = f4.selectbox("Cliente exacto", clientes_opciones)

df_vista = df_final.copy()

if buscar:
    df_vista = df_vista[df_vista["Cliente"].str.contains(buscar, case=False, na=False)]

if cliente_select != "Todos":
    df_vista = df_vista[df_vista["Cliente"] == cliente_select]

if estado_sel != "Todos":
    df_vista = df_vista[df_vista["Estado Comercial"] == estado_sel]

if vendedor_sel != "Todos" and "Vendedor" in df_vista.columns:
    df_vista = df_vista[df_vista["Vendedor"].astype(str) == vendedor_sel]

clientes_filtrados = df_vista["Cliente"].dropna().astype(str).unique().tolist()

df_ciclo_f = df_ciclo[df_ciclo["Cliente"].isin(clientes_filtrados)].copy()
df_pedidos_f = df_pedidos[df_pedidos["Cliente"].isin(clientes_filtrados)].copy()
df_pagos_f = df_pagos[df_pagos["Cliente"].isin(clientes_filtrados)].copy()
df_notas_credito_f = df_notas_credito[df_notas_credito["Cliente"].isin(clientes_filtrados)].copy()
df_pagos_ciclo_f = df_pagos_ciclo[df_pagos_ciclo["Cliente"].isin(clientes_filtrados)].copy()
df_notas_credito_ciclo_f = df_notas_credito_f[(df_notas_credito_f["Fecha"].dt.normalize() >= inicio_ciclo) & (df_notas_credito_f["Fecha"].dt.normalize() <= fin_ciclo)].copy() if not df_notas_credito_f.empty else df_notas_credito_f.copy()
df_visitas_f = df_visitas[df_visitas["Cliente"].isin(clientes_filtrados)].copy()
cuenta_corriente_f = cuenta_corriente[cuenta_corriente["Cliente"].isin(clientes_filtrados)].copy()

# Ciclo actual filtrado
facturacion_ciclo = float(df_ciclo_f["Importe"].sum()) if not df_ciclo_f.empty else 0.0
toneladas_ciclo = float(df_ciclo_f["Toneladas"].sum()) if not df_ciclo_f.empty else 0.0
pedidos_ciclo = int(df_ciclo_f["Pedido ID"].nunique()) if not df_ciclo_f.empty else 0
comision_ciclo = float(df_ciclo_f["Comisión Total"].sum()) if not df_ciclo_f.empty else 0.0
comision_venta_ciclo = float(df_ciclo_f["Comisión Venta"].sum()) if not df_ciclo_f.empty else 0.0
comision_cobranza_ciclo = float(df_ciclo_f["Comisión Cobranza"].sum()) if not df_ciclo_f.empty else 0.0

# Acumulado filtrado histórico
facturacion_acumulada = float(df_pedidos_f["Importe"].sum()) if not df_pedidos_f.empty else 0.0
toneladas_acumuladas = float(df_pedidos_f["Toneladas"].sum()) if not df_pedidos_f.empty else 0.0
pedidos_acumulados = int(df_pedidos_f["Pedido ID"].nunique()) if not df_pedidos_f.empty else 0
comision_acumulada = float(df_pedidos_f["Comisión Total"].sum()) if not df_pedidos_f.empty else 0.0
comision_venta_acumulada = float(df_pedidos_f["Comisión Venta"].sum()) if not df_pedidos_f.empty else 0.0
comision_cobranza_acumulada = float(df_pedidos_f["Comisión Cobranza"].sum()) if not df_pedidos_f.empty else 0.0

notas_credito_acumuladas = float(df_notas_credito_f["Monto Nota"].sum()) if not df_notas_credito_f.empty else 0.0
notas_credito_ciclo = float(df_notas_credito_ciclo_f["Monto Nota"].sum()) if not df_notas_credito_ciclo_f.empty else 0.0
comision_venta_descontada_acumulada = float(df_notas_credito_f["Comisión Venta Descontada"].sum()) if not df_notas_credito_f.empty else 0.0
comision_venta_descontada_ciclo = float(df_notas_credito_ciclo_f["Comisión Venta Descontada"].sum()) if not df_notas_credito_ciclo_f.empty else 0.0

facturacion_neta_acumulada = facturacion_acumulada - notas_credito_acumuladas
facturacion_neta_ciclo = facturacion_ciclo - notas_credito_ciclo

comision_venta_acumulada = max(comision_venta_acumulada - comision_venta_descontada_acumulada, 0)
comision_acumulada = max(comision_acumulada - comision_venta_descontada_acumulada, 0)
comision_venta_ciclo = max(comision_venta_ciclo - comision_venta_descontada_ciclo, 0)
comision_ciclo = max(comision_ciclo - comision_venta_descontada_ciclo, 0)

comision_cobranza_externa_acumulada = (
    float(df_pagos_f["Comisión Cobranza Externa"].sum())
    if not df_pagos_f.empty and "Comisión Cobranza Externa" in df_pagos_f.columns
    else 0.0
)
comision_cobranza_externa_ciclo = (
    float(df_pagos_ciclo_f["Comisión Cobranza Externa"].sum())
    if not df_pagos_ciclo_f.empty and "Comisión Cobranza Externa" in df_pagos_ciclo_f.columns
    else 0.0
)

comision_cobranza_acumulada += comision_cobranza_externa_acumulada
comision_acumulada += comision_cobranza_externa_acumulada
comision_cobranza_ciclo += comision_cobranza_externa_ciclo
comision_ciclo += comision_cobranza_externa_ciclo

saldo_pendiente_f = float(cuenta_corriente_f["Saldo Pendiente"].sum()) if not cuenta_corriente_f.empty else 0.0

# General histórico
facturacion_general = float(df_pedidos["Importe"].sum()) if not df_pedidos.empty else 0.0
toneladas_general = float(df_pedidos["Toneladas"].sum()) if not df_pedidos.empty else 0.0
pedidos_general = int(df_pedidos["Pedido ID"].nunique()) if not df_pedidos.empty else 0
comision_general = float(df_pedidos["Comisión Total"].sum()) if not df_pedidos.empty else 0.0
if not df_pagos.empty and "Comisión Cobranza Externa" in df_pagos.columns:
    comision_general += float(df_pagos["Comisión Cobranza Externa"].sum())

# KPIs empresa
ticket_promedio = facturacion_acumulada / pedidos_acumulados if pedidos_acumulados > 0 else 0.0
precio_tonelada = facturacion_acumulada / toneladas_acumuladas if toneladas_acumuladas > 0 else 0.0
total_vendido_f = float(cuenta_corriente_f["Total Vendido"].sum()) if not cuenta_corriente_f.empty else 0.0
total_cobrado_f = float(cuenta_corriente_f["Total Cobrado"].sum()) if not cuenta_corriente_f.empty else 0.0
porcentaje_cobranza = (total_cobrado_f / total_vendido_f * 100) if total_vendido_f > 0 else 0.0
clientes_activos = len(df_vista[df_vista["Estado Comercial"] == "Activo"]) if "Estado Comercial" in df_vista.columns else 0
clientes_pre = len(df_vista[df_vista["Estado Comercial"] == "Pre-perdido"]) if "Estado Comercial" in df_vista.columns else 0
clientes_perdidos = len(df_vista[df_vista["Estado Comercial"] == "Perdido"]) if "Estado Comercial" in df_vista.columns else 0
clientes_con_deuda = len(cuenta_corriente_f[cuenta_corriente_f["Saldo Pendiente"] > 0]) if not cuenta_corriente_f.empty else 0

st.sidebar.write(f"**Facturación acumulada:** {fmt_ars(facturacion_acumulada)}")
st.sidebar.write(f"**Saldo pendiente:** {fmt_ars(saldo_pendiente_f)}")


# ============================================================
# FICHA CLIENTE FILTRADO
# ============================================================
if len(clientes_filtrados) == 1:
    cliente_unico = clientes_filtrados[0]
    ficha = df_final[df_final["Cliente"] == cliente_unico].iloc[0]
    cc_ficha = cuenta_corriente[cuenta_corriente["Cliente"] == cliente_unico]

    vendido = float(cc_ficha["Total Vendido"].sum()) if not cc_ficha.empty else 0
    notas_cliente_ficha = float(cc_ficha["Notas de Crédito"].sum()) if not cc_ficha.empty and "Notas de Crédito" in cc_ficha.columns else 0
    venta_neta_cliente = float(cc_ficha["Venta Neta"].sum()) if not cc_ficha.empty and "Venta Neta" in cc_ficha.columns else vendido - notas_cliente_ficha
    cobrado = float(cc_ficha["Total Cobrado"].sum()) if not cc_ficha.empty else 0
    saldo = float(cc_ficha["Saldo Pendiente"].sum()) if not cc_ficha.empty else 0
    comisiones = float(df_pedidos[df_pedidos["Cliente"] == cliente_unico]["Comisión Total"].sum()) if not df_pedidos.empty else 0
    estado = str(ficha["Estado Comercial"])
    clase = clase_estado(estado)

    with st.expander("Ficha rápida e historial del cliente filtrado", expanded=True):
        st.markdown('<div class="client-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="client-name">{cliente_unico}</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="{clase}">{estado}</span>', unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Días sin comprar", int(ficha["Dias sin comprar"]) if pd.notna(ficha["Dias sin comprar"]) else 0)
        with c2:
            metric_card("Total vendido", fmt_ars(vendido))
        with c3:
            metric_card("Total cobrado", fmt_ars(cobrado))
        with c4:
            metric_card("Saldo pendiente", fmt_ars(saldo))

        c5, c6, c7, c8 = st.columns(4)
        with c5:
            metric_card("Comisiones", fmt_ars(comisiones))
        with c6:
            metric_card("Pedidos", df_pedidos[df_pedidos["Cliente"] == cliente_unico]["Pedido ID"].nunique() if not df_pedidos.empty else 0)
        with c7:
            metric_card("Toneladas", fmt_num(df_pedidos[df_pedidos["Cliente"] == cliente_unico]["Toneladas"].sum() if not df_pedidos.empty else 0))
        with c8:
            metric_card("Estado cuenta", cc_ficha["Estado Cuenta"].iloc[0] if not cc_ficha.empty else "Sin datos")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("### Historial del cliente")

        st.markdown("#### Pedidos")
        historial_pedidos_cliente = df_pedidos[df_pedidos["Cliente"] == cliente_unico].sort_values("Fecha", ascending=False)
        mostrar_tabla_pro(historial_pedidos_cliente)

        st.markdown("#### Pagos")
        historial_pagos_cliente = df_pagos[df_pagos["Cliente"] == cliente_unico].sort_values("Fecha", ascending=False)
        mostrar_tabla_pro(historial_pagos_cliente)

        st.markdown("#### Notas de crédito")
        historial_notas_cliente = df_notas_credito[df_notas_credito["Cliente"] == cliente_unico].sort_values("Fecha", ascending=False)
        mostrar_tabla_pro(historial_notas_cliente)

        st.markdown("#### Visitas")
        historial_visitas_cliente = df_visitas[df_visitas["Cliente"] == cliente_unico].sort_values("Fecha", ascending=False)
        mostrar_tabla_pro(historial_visitas_cliente)

st.markdown('<div class="blue-line"></div>', unsafe_allow_html=True)


# ============================================================
# PANTALLAS
# ============================================================
if menu == "Inicio":
    st.markdown('<span class="badge">Modo empresa: KPIs + rankings</span>', unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1], gap="large")

    with col_left:
        st.markdown('<div class="card-yellow">', unsafe_allow_html=True)
        st.markdown("### Resumen acumulado")
        st.markdown(f"**Ciclo actual:** {periodo_actual}")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Facturación neta", fmt_ars(facturacion_neta_acumulada))
        with c2:
            metric_card("Toneladas acumuladas", fmt_num(toneladas_acumuladas))
        with c3:
            metric_card("Pedidos acumulados", pedidos_acumulados)
        with c4:
            metric_card("Saldo pendiente", fmt_ars(saldo_pendiente_f))

        st.markdown("#### KPIs de negocio")
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            metric_card("Ticket promedio", fmt_ars(ticket_promedio))
        with k2:
            metric_card("Precio por tonelada", fmt_ars(precio_tonelada))
        with k3:
            metric_card("% Cobranza", fmt_pct(porcentaje_cobranza))
        with k4:
            metric_card("Clientes con deuda", clientes_con_deuda)

        k5, k6, k7 = st.columns(3)
        with k5:
            metric_card("Clientes activos", clientes_activos)
        with k6:
            metric_card("Pre-perdidos", clientes_pre)
        with k7:
            metric_card("Perdidos", clientes_perdidos)

        st.markdown("#### Ciclo actual filtrado")
        g1, g2, g3, g4 = st.columns(4)
        with g1:
            metric_card("Facturación neta ciclo", fmt_ars(facturacion_neta_ciclo))
        with g2:
            metric_card("Toneladas ciclo", fmt_num(toneladas_ciclo))
        with g3:
            metric_card("Pedidos ciclo", pedidos_ciclo)
        with g4:
            metric_card("Comisión ciclo", fmt_ars(comision_ciclo))

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Ventas por día")
        if df_pedidos_f.empty:
            st.info("No hay ventas con los filtros actuales.")
        else:
            ventas_dia = df_pedidos_f.groupby(df_pedidos_f["Fecha"].dt.date)["Importe"].sum()
            st.line_chart(ventas_dia)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Alertas inteligentes")

        if saldo_pendiente_f > 0:
            st.markdown(f'<div class="danger-box">Saldo pendiente: {fmt_ars(saldo_pendiente_f)}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="ok-box">Cuenta corriente al día</div>', unsafe_allow_html=True)

        if clientes_pre > 0:
            st.markdown(f'<div class="alert-box">Clientes pre-perdidos: {clientes_pre}</div>', unsafe_allow_html=True)
        if clientes_perdidos > 0:
            st.markdown(f'<div class="danger-box">Clientes perdidos: {clientes_perdidos}</div>', unsafe_allow_html=True)

        pendientes = (
            len(df_pedidos_f[df_pedidos_f["Cobrado"].astype(str).str.lower().isin(["no", "pendiente"])])
            if not df_pedidos_f.empty and "Cobrado" in df_pedidos_f.columns
            else 0
        )
        if pendientes > 0:
            st.markdown(f'<div class="alert-box">Pedidos pendientes de cobro: {pendientes}</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card-yellow">', unsafe_allow_html=True)
        st.markdown("### Comisiones del ciclo (26 → 25)")
        metric_card("Venta ciclo", fmt_ars(comision_venta_ciclo))
        metric_card("Cobranza ciclo", fmt_ars(comision_cobranza_ciclo))
        metric_card("Total ciclo", fmt_ars(comision_ciclo))
        st.caption(f"Histórico total guardado en pedidos: {fmt_ars(comision_general)}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## Rankings profesionales")

    r1, r2 = st.columns(2)

    with r1:
        st.markdown("### Top 10 clientes por facturación")
        if not df_pedidos_f.empty:
            top_clientes = (
                df_pedidos_f.groupby("Cliente", as_index=False)["Importe"]
                .sum()
                .sort_values("Importe", ascending=False)
                .head(10)
                .rename(columns={"Importe": "Facturación"})
            )
            st.dataframe(top_clientes, use_container_width=True)
            if not top_clientes.empty:
                st.bar_chart(top_clientes.set_index("Cliente")["Facturación"])
        else:
            st.info("No hay datos para ranking.")

    with r2:
        st.markdown("### Top 10 clientes por toneladas")
        if not df_pedidos_f.empty:
            top_ton = (
                df_pedidos_f.groupby("Cliente", as_index=False)["Toneladas"]
                .sum()
                .sort_values("Toneladas", ascending=False)
                .head(10)
            )
            st.dataframe(top_ton, use_container_width=True)
            if not top_ton.empty:
                st.bar_chart(top_ton.set_index("Cliente")["Toneladas"])
        else:
            st.info("No hay datos para ranking.")

    r3, r4 = st.columns(2)

    with r3:
        st.markdown("### Top 10 deudores")
        top_deuda = cuenta_corriente_f[cuenta_corriente_f["Saldo Pendiente"] > 0].sort_values("Saldo Pendiente", ascending=False).head(10)
        if top_deuda.empty:
            st.success("No hay saldos pendientes.")
        else:
            mostrar_tabla_pro(
                top_deuda,
                columnas=["Cliente", "Total Vendido", "Total Cobrado", "Saldo Pendiente", "Estado Cuenta"]
            )
            st.bar_chart(top_deuda.set_index("Cliente")["Saldo Pendiente"])

    with r4:
        st.markdown("### Top 10 productos")
        if not df_pedidos_f.empty:
            top_productos = (
                df_pedidos_f.groupby("Producto", as_index=False)
                .agg({"Importe": "sum", "Toneladas": "sum"})
                .sort_values("Importe", ascending=False)
                .head(10)
                .rename(columns={"Importe": "Facturación"})
            )
            st.dataframe(top_productos, use_container_width=True)
            if not top_productos.empty:
                st.bar_chart(top_productos.set_index("Producto")["Facturación"])
        else:
            st.info("No hay datos para ranking.")

    st.markdown("### Pedidos cargados hoy")
    df_hoy = df_pedidos_f[df_pedidos_f["Fecha"].dt.date == date.today()].copy() if not df_pedidos_f.empty else df_pedidos_f
    mostrar_tabla_pro(df_hoy)


elif menu == "Pedidos":
    st.markdown('<span class="badge">Gestión de pedidos</span>', unsafe_allow_html=True)

    if df_clientes.empty or df_precios.empty:
        st.warning("Faltan clientes o precios para cargar pedidos.")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        p1, p2, p3 = st.columns(3)

        cliente = p1.selectbox("Cliente", sorted(df_clientes["Cliente"].dropna().unique()))
        fecha_pedido = p2.date_input("Fecha", date.today())
        producto = p3.selectbox("Producto", sorted(df_precios["Producto"].dropna().unique()))

        prod = df_precios[df_precios["Producto"] == producto].iloc[0]
        presentacion = prod["Presentacion"]
        kilos = float(prod["Kilos por Bulto"])
        precio_lista = float(prod["Precio Lista"])

        q1, q2, q3, q4 = st.columns(4)
        q1.text_input("Presentación", presentacion, disabled=True)
        q2.text_input("Kilos por bulto", fmt_num(kilos, 2), disabled=True)
        cantidad = q3.number_input("Cantidad bolsas / packs", min_value=0.0, step=1.0)
        precio_venta = q4.number_input("Precio venta", min_value=0.0, value=precio_lista, step=1.0)

        toneladas = cantidad * kilos / 1000
        importe = cantidad * precio_venta
        total_cliente_actual = (
            float(df_pedidos[df_pedidos["Cliente"] == cliente]["Importe"].sum())
            if not df_pedidos.empty and "Cliente" in df_pedidos.columns
            else 0.0
        )
        porcentaje_comision_venta, categoria_comision_venta = calcular_porcentaje_comision_venta(
            producto,
            total_cliente_actual + importe,
            df_comisiones_venta
        )
        comision_venta = importe * (porcentaje_comision_venta / 100)

        m1, m2, m3 = st.columns(3)
        with m1:
            metric_card("Toneladas", fmt_num(toneladas))
        with m2:
            metric_card("Importe", fmt_ars(importe))
        with m3:
            metric_card("Comisión venta", fmt_ars(comision_venta))

        ca, cb = st.columns(2)
        with ca:
            metric_card("Categoría comisión venta", categoria_comision_venta)
        with cb:
            metric_card("% comisión venta", f"{porcentaje_comision_venta:.3f}%")

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        if st.button("Guardar pedido", use_container_width=True):
            if cantidad <= 0:
                st.error("La cantidad debe ser mayor a 0.")
            else:
                con = conectar()
                max_id = pd.read_sql_query("SELECT MAX(id) AS max_id FROM pedidos", con)["max_id"].iloc[0]
                nuevo_num = 1 if pd.isna(max_id) else int(max_id) + 1
                pedido_id = f"PED-{nuevo_num:05d}"
                ahora = datetime.now()

                con.execute(
                    """
                    INSERT INTO pedidos (
                        pedido_id, cliente, fecha, hora_pedido, fechahora_pedido, producto, presentacion,
                        cantidad_bultos, kilos_por_bulto, precio_lista, precio_venta, importe, toneladas,
                        cobrado, fecha_cobro, dias_al_cobro, porcentaje_cobranza, regla_cobranza,
                        comision_venta, comision_cobranza, comision_total,
                        categoria_comision_venta, porcentaje_comision_venta
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        pedido_id,
                        cliente,
                        str(fecha_pedido),
                        ahora.strftime("%H:%M:%S"),
                        str(ahora),
                        producto,
                        presentacion,
                        cantidad,
                        kilos,
                        precio_lista,
                        precio_venta,
                        importe,
                        toneladas,
                        "No",
                        "",
                        0,
                        0,
                        "Pendiente",
                        comision_venta,
                        0,
                        comision_venta,
                        categoria_comision_venta,
                        porcentaje_comision_venta,
                    ),
                )
                con.commit()
                con.close()
                st.success(f"Pedido guardado correctamente: {pedido_id}")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## Pedidos del día")
    df_hoy = df_pedidos_f[df_pedidos_f["Fecha"].dt.date == date.today()].copy() if not df_pedidos_f.empty else df_pedidos_f
    mostrar_tabla_pro(df_hoy)


elif menu == "Cobranza":
    st.markdown('<span class="badge">Gestión de cobranza</span>', unsafe_allow_html=True)

    if df_pedidos_f.empty:
        st.info("No hay pedidos con los filtros actuales.")
    else:
        resumen = df_pedidos_f.groupby("Pedido ID", as_index=False).agg(
            {"Cliente": "first", "Fecha": "first", "Importe": "sum", "Comisión Venta": "sum", "Cobrado": "first"}
        )

        resumen["Pedido para cobrar"] = (
            resumen["Cliente"].astype(str)
            + " | "
            + resumen["Pedido ID"].astype(str)
            + " | "
            + resumen["Importe"].apply(fmt_ars)
        )

        pedido_label = st.selectbox("Cliente / pedido a cobrar", resumen["Pedido para cobrar"].tolist())
        pedido = resumen.loc[resumen["Pedido para cobrar"] == pedido_label, "Pedido ID"].iloc[0]
        fila = resumen[resumen["Pedido ID"] == pedido].iloc[0]

        f_ent, f_cob = st.columns(2)
        with f_ent:
            fecha_entrega = st.date_input("Fecha de entrega", date.today())
        with f_cob:
            fecha_cobro = st.date_input("Fecha de cobro", date.today())

        dias = (pd.Timestamp(fecha_cobro).normalize() - pd.Timestamp(fecha_entrega).normalize()).days
        dias = max(0, int(dias))

        st.info(
            "La comisión por cobranza se calcula desde la fecha de entrega hasta la fecha de cobro."
        )

        d1, d2 = st.columns(2)
        with d1:
            metric_card("Días entrega → cobro", dias)
        with d2:
            metric_card("Fecha de entrega", fecha_entrega.strftime("%d/%m/%Y"))

        porc, regla = regla_cobranza(dias)
        com_cob = fila["Importe"] * porc
        com_total = fila["Comisión Venta"] + com_cob

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Cliente", fila["Cliente"])
        with c2:
            metric_card("Importe", fmt_ars(fila["Importe"]))
        with c3:
            metric_card("Comisión cobranza", fmt_ars(com_cob))
        with c4:
            metric_card("Comisión total", fmt_ars(com_total))

        r1, r2 = st.columns(2)
        with r1:
            metric_card("Regla aplicada", regla)
        with r2:
            metric_card("% cobranza", f"{porc * 100:.2f}%")

        b1, b2 = st.columns(2)

        if b1.button("Marcar como cobrado", use_container_width=True):
            con = conectar()
            con.execute(
                """
                UPDATE pedidos
                SET cobrado=?, fecha_entrega=?, fecha_cobro=?, dias_al_cobro=?, porcentaje_cobranza=?, regla_cobranza=?,
                    comision_cobranza=?, comision_total=comision_venta + ?
                WHERE pedido_id=?
                """,
                ("Sí", str(fecha_entrega), str(fecha_cobro), dias, porc, regla, com_cob, com_cob, pedido),
            )
            con.commit()
            con.close()
            st.success("Pedido marcado como cobrado")
            st.rerun()

        if b2.button("Marcar como pendiente", use_container_width=True):
            con = conectar()
            con.execute(
                """
                UPDATE pedidos
                SET cobrado=?, fecha_entrega=?, fecha_cobro=?, dias_al_cobro=?, porcentaje_cobranza=?, regla_cobranza=?,
                    comision_cobranza=?, comision_total=comision_venta
                WHERE pedido_id=?
                """,
                ("No", "", "", 0, 0, "Pendiente", 0, pedido),
            )
            con.commit()
            con.close()
            st.success("Pedido volvió a pendiente")
            st.rerun()


elif menu == "Pagos":
    st.markdown('<span class="badge">Pagos manuales y cobranzas externas</span>', unsafe_allow_html=True)

    if df_clientes.empty:
        st.warning("No hay clientes cargados.")
    else:
        st.markdown('<div class="card-yellow">', unsafe_allow_html=True)

        p1, p2, p3 = st.columns(3)
        cliente_pago = p1.selectbox("Cliente", sorted(df_clientes["Cliente"].dropna().unique()))
        fecha_pago = p2.date_input("Fecha de pago", date.today())
        monto_pago = p3.number_input("Monto abonado", min_value=0.0, step=1000.0)

        p4, p5 = st.columns(2)
        medio_pago = p4.selectbox("Medio de pago", ["Efectivo", "Transferencia", "Cheque", "Mercado Pago", "Otro"])
        aplicado_pedido = p5.text_input("Aplicado a pedido", value="No aplica")

        pago_externo = st.checkbox("Este pago corresponde a un pedido externo/no cargado en la app")

        fecha_pedido_externo = None
        fecha_entrega_externa = None
        detalle_pedido_externo = ""
        dias_externo = 0
        porc_externo = 0.0
        regla_externa = ""
        comision_cobranza_externa = 0.0

        if pago_externo:
            st.info("Usá esta opción cuando el pedido no está cargado en la app, pero necesitás registrar el cobro y sumar la comisión por cobranza.")
            e1, e2 = st.columns(2)
            fecha_entrega_externa = e1.date_input("Fecha de entrega del pedido externo", date.today())
            detalle_pedido_externo = e2.text_input("Detalle / número del pedido externo", value="Pedido externo")

            fecha_pedido_externo = fecha_entrega_externa
            dias_externo = (pd.Timestamp(fecha_pago).normalize() - pd.Timestamp(fecha_entrega_externa).normalize()).days
            dias_externo = max(0, int(dias_externo))
            porc_externo, regla_externa = regla_cobranza(dias_externo)
            comision_cobranza_externa = monto_pago * porc_externo

            ce1, ce2, ce3 = st.columns(3)
            with ce1:
                metric_card("Días al cobro", dias_externo)
            with ce2:
                metric_card("Regla cobranza", regla_externa)
            with ce3:
                metric_card("Comisión cobranza externa", fmt_ars(comision_cobranza_externa))

        observacion_pago = st.text_area("Observación del pago")

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        if st.button("Guardar pago manual", use_container_width=True):
            if monto_pago <= 0:
                st.error("El monto abonado debe ser mayor a 0.")
            else:
                con = conectar()
                con.execute("""
                    INSERT INTO pagos (
                        fecha, hora, cliente, monto_abonado, medio_pago, observacion, aplicado_a_pedido,
                        tipo_pago, pedido_externo, fecha_pedido_externo, fecha_entrega_externa, importe_pedido_externo,
                        dias_al_cobro_externo, regla_cobranza_externa, comision_cobranza_externa
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(fecha_pago),
                    datetime.now().strftime("%H:%M:%S"),
                    cliente_pago,
                    monto_pago,
                    medio_pago,
                    observacion_pago,
                    aplicado_pedido if not pago_externo else detalle_pedido_externo,
                    "Pedido externo" if pago_externo else "Pago manual",
                    detalle_pedido_externo if pago_externo else "",
                    str(fecha_pedido_externo) if pago_externo else "",
                    str(fecha_entrega_externa) if pago_externo else "",
                    monto_pago if pago_externo else 0,
                    dias_externo if pago_externo else 0,
                    regla_externa if pago_externo else "",
                    comision_cobranza_externa if pago_externo else 0,
                ))
                con.commit()
                con.close()
                st.success("Pago guardado correctamente")
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("## Historial de pagos")
    mostrar_tabla_pro(df_pagos_f.sort_values(["Fecha", "Hora"], ascending=[False, False]))


elif menu == "Notas de Crédito":
    st.markdown('<span class="badge">Notas de Crédito</span>', unsafe_allow_html=True)

    if df_pedidos_f.empty:
        st.info("No hay pedidos disponibles con los filtros actuales.")
    else:
        st.markdown('<div class="card-yellow">', unsafe_allow_html=True)
        st.markdown("### Cargar nota de crédito")

        resumen_pedidos_nc = (
            df_pedidos_f.groupby("Pedido ID", as_index=False)
            .agg({
                "Cliente": "first",
                "Fecha": "first",
                "Importe": "sum",
                "Comisión Venta": "sum",
                "Producto": "first",
            })
        )

        resumen_pedidos_nc["Pedido para nota"] = (
            resumen_pedidos_nc["Cliente"].astype(str)
            + " | "
            + resumen_pedidos_nc["Pedido ID"].astype(str)
            + " | "
            + resumen_pedidos_nc["Importe"].apply(fmt_ars)
        )

        n1, n2, n3f = st.columns(3)
        pedido_label_nc = n1.selectbox("Cliente / pedido", resumen_pedidos_nc["Pedido para nota"].tolist())
        fecha_entrega_nota = n2.date_input("Fecha de entrega", date.today(), key="fecha_entrega_nota")
        fecha_nota = n3f.date_input("Fecha nota de crédito", date.today())

        pedido_nc = resumen_pedidos_nc.loc[resumen_pedidos_nc["Pedido para nota"] == pedido_label_nc, "Pedido ID"].iloc[0]
        fila_nc = resumen_pedidos_nc[resumen_pedidos_nc["Pedido ID"] == pedido_nc].iloc[0]

        importe_original = float(fila_nc["Importe"])
        comision_venta_original = float(fila_nc["Comisión Venta"])

        n3, n4, n5 = st.columns(3)
        with n3:
            metric_card("Cliente", fila_nc["Cliente"])
        with n4:
            metric_card("Importe pedido", fmt_ars(importe_original))
        with n5:
            metric_card("Comisión venta original", fmt_ars(comision_venta_original))

        monto_nota = st.number_input("Monto de nota de crédito", min_value=0.0, max_value=float(importe_original), step=1000.0)
        motivo = st.selectbox("Motivo", ["Entrega parcial", "Devolución", "Diferencia de precio", "Error de carga", "Otro"])
        observacion_nota = st.text_area("Observación")

        proporcion = monto_nota / importe_original if importe_original > 0 else 0
        comision_descontada = comision_venta_original * proporcion

        cna, cnb = st.columns(2)
        with cna:
            metric_card("Descuento sobre venta", fmt_ars(monto_nota))
        with cnb:
            metric_card("Comisión a descontar", fmt_ars(comision_descontada))

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        if st.button("Guardar nota de crédito", use_container_width=True):
            if monto_nota <= 0:
                st.error("El monto de la nota debe ser mayor a 0.")
            else:
                con = conectar()
                con.execute("""
                    INSERT INTO notas_credito (
                        fecha, hora, cliente, pedido_id, fecha_entrega, monto_nota, motivo, observacion, comision_venta_descontada
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(fecha_nota),
                    datetime.now().strftime("%H:%M:%S"),
                    fila_nc["Cliente"],
                    pedido_nc,
                    str(fecha_entrega_nota),
                    monto_nota,
                    motivo,
                    observacion_nota,
                    comision_descontada,
                ))
                con.commit()
                con.close()
                st.success("Nota de crédito guardada correctamente.")
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("## Historial de notas de crédito")
    mostrar_tabla_pro(df_notas_credito_f.sort_values("Fecha", ascending=False))


elif menu == "Cuenta Corriente":
    st.markdown('<span class="badge">Cuenta corriente por cliente</span>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Total vendido", fmt_ars(cuenta_corriente_f["Total Vendido"].sum()))
    with c2:
        metric_card("Total cobrado", fmt_ars(cuenta_corriente_f["Total Cobrado"].sum()))
    with c3:
        metric_card("Saldo pendiente", fmt_ars(cuenta_corriente_f["Saldo Pendiente"].sum()))
    with c4:
        metric_card("Clientes con deuda", len(cuenta_corriente_f[cuenta_corriente_f["Saldo Pendiente"] > 0]))

    mostrar_tabla_pro(
        cuenta_corriente_f,
        columnas=["Cliente", "Total Vendido", "Notas de Crédito", "Venta Neta", "Pedidos", "Cobrado por Pedido", "Pagos Manuales", "Total Cobrado", "Saldo Pendiente", "Estado Cuenta"]
    )

    st.markdown("## Ranking de clientes que más deben")
    ranking_deuda = cuenta_corriente_f[cuenta_corriente_f["Saldo Pendiente"] > 0].sort_values("Saldo Pendiente", ascending=False)

    if ranking_deuda.empty:
        st.success("No hay saldos pendientes")
    else:
        mostrar_tabla_pro(
            ranking_deuda.head(30),
            columnas=["Cliente", "Total Vendido", "Notas de Crédito", "Venta Neta", "Pedidos", "Cobrado por Pedido", "Pagos Manuales", "Total Cobrado", "Saldo Pendiente", "Estado Cuenta"]
        )
        st.bar_chart(ranking_deuda.head(10).set_index("Cliente")["Saldo Pendiente"])


elif menu == "Visitas":
    st.markdown('<span class="badge">Agenda inteligente de visitas</span>', unsafe_allow_html=True)

    agenda = df_vista.copy()
    agenda["Prioridad Orden"] = agenda["Estado Comercial"].apply(prioridad_visita)
    agenda = agenda.sort_values(["Prioridad Orden", "Dias sin comprar"], ascending=[True, False])

    clientes_para_visitar = agenda[agenda["Estado Comercial"].isin(["Pre-perdido", "Perdido"])].copy()

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Clientes para visitar", len(clientes_para_visitar))
    with c2:
        metric_card("Pre-perdidos", len(clientes_para_visitar[clientes_para_visitar["Estado Comercial"] == "Pre-perdido"]))
    with c3:
        metric_card("Perdidos", len(clientes_para_visitar[clientes_para_visitar["Estado Comercial"] == "Perdido"]))

    mostrar_tabla_pro(clientes_para_visitar)

    st.markdown("## Registrar visita")

    if df_vista.empty:
        st.warning("No hay clientes disponibles con los filtros actuales.")
    else:
        cliente_visita = st.selectbox("Cliente visitado", sorted(df_vista["Cliente"].dropna().unique()))
        fila_cliente = df_final[df_final["Cliente"] == cliente_visita]

        estado_actual = fila_cliente.iloc[0]["Estado Comercial"] if not fila_cliente.empty else ""
        dias_actuales = fila_cliente.iloc[0]["Dias sin comprar"] if not fila_cliente.empty else 0

        v1, v2, v3 = st.columns(3)
        fecha_visita = v1.date_input("Fecha visita", date.today())
        resultado_visita = v2.selectbox("Resultado", ["Visitado", "Vendí", "No compró", "No estaba", "Llamar luego"])
        proxima_accion = v3.selectbox("Próxima acción", ["Sin acción", "Volver a visitar", "Llamar", "Enviar precios", "Esperar pedido"])

        observacion = st.text_area("Observación")

        if st.button("Guardar visita", use_container_width=True):
            con = conectar()
            con.execute(
                """
                INSERT INTO visitas (fecha, hora, cliente, estado_cliente, dias_sin_comprar, resultado, observacion, proxima_accion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(fecha_visita),
                    datetime.now().strftime("%H:%M:%S"),
                    cliente_visita,
                    estado_actual,
                    float(dias_actuales) if pd.notna(dias_actuales) else 0,
                    resultado_visita,
                    observacion,
                    proxima_accion,
                ),
            )
            con.commit()
            con.close()
            st.success("Visita guardada correctamente")
            st.rerun()

    st.markdown("## Historial de visitas")
    mostrar_tabla_pro(df_visitas_f.sort_values(["Fecha", "Hora"], ascending=[False, False]))


elif menu == "Objetivos":
    st.markdown('<span class="badge">Objetivos comerciales</span>', unsafe_allow_html=True)
    st.markdown(f"## Ciclo actual: {periodo_actual}")

    o1, o2, o3 = st.columns(3)
    nueva_meta_facturacion = o1.number_input("Meta facturación del ciclo", min_value=0.0, value=float(meta_facturacion), step=100000.0)
    nueva_meta_toneladas = o2.number_input("Meta toneladas del ciclo", min_value=0.0, value=float(meta_toneladas), step=1.0)
    nueva_meta_pedidos = o3.number_input("Meta pedidos del ciclo", min_value=0.0, value=float(meta_pedidos), step=1.0)

    if st.button("Guardar objetivos del ciclo", use_container_width=True):
        con = conectar()
        con.execute(
            """
            INSERT OR REPLACE INTO objetivos (periodo, meta_facturacion, meta_toneladas, meta_pedidos, fecha_actualizacion)
            VALUES (?, ?, ?, ?, ?)
            """,
            (periodo_actual, nueva_meta_facturacion, nueva_meta_toneladas, nueva_meta_pedidos, str(datetime.now())),
        )
        con.commit()
        con.close()
        st.success("Objetivos guardados correctamente")
        st.rerun()

    st.markdown("## Avance según ciclo actual")
    if meta_facturacion <= 0 and meta_toneladas <= 0 and meta_pedidos <= 0:
        st.info("Todavía no cargaste objetivos para este ciclo.")
    else:
        st.write(f"Facturación: {texto_objetivo(facturacion_ciclo, meta_facturacion)}")
        st.progress(progreso(facturacion_ciclo, meta_facturacion))
        st.write(f"Toneladas: {texto_objetivo(toneladas_ciclo, meta_toneladas)}")
        st.progress(progreso(toneladas_ciclo, meta_toneladas))
        st.write(f"Pedidos: {texto_objetivo(pedidos_ciclo, meta_pedidos)}")
        st.progress(progreso(pedidos_ciclo, meta_pedidos))


elif menu == "Inteligencia":
    st.markdown('<span class="badge">Inteligencia comercial</span>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Objetivos")
        if meta_facturacion > 0 and facturacion_ciclo < meta_facturacion:
            st.markdown(f'<div class="alert-box">Falta facturar en el ciclo {fmt_ars(meta_facturacion - facturacion_ciclo)}</div>', unsafe_allow_html=True)
        elif meta_facturacion > 0:
            st.markdown('<div class="ok-box">Objetivo de facturación del ciclo cumplido</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-box">Todavía no cargaste meta de facturación.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Cuenta corriente")
        if saldo_pendiente_f > 0:
            st.markdown(f'<div class="danger-box">Saldo pendiente: {fmt_ars(saldo_pendiente_f)}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="ok-box">No hay saldo pendiente</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## Clientes prioritarios")
    clientes_alerta = df_vista[df_vista["Estado Comercial"].isin(["Pre-perdido", "Perdido"])].copy()
    mostrar_tabla_pro(clientes_alerta.sort_values("Dias sin comprar", ascending=False).head(30))

    st.markdown("## Clientes con mayor deuda")
    mostrar_tabla_pro(cuenta_corriente_f[cuenta_corriente_f["Saldo Pendiente"] > 0].head(30))


elif menu == "Clientes":
    st.markdown('<span class="badge">Clientes</span>', unsafe_allow_html=True)

    with st.expander("Agregar cliente nuevo"):
        c1, c2, c3, c4 = st.columns(4)
        nuevo_cliente = c1.text_input("Cliente / Razón social").strip().upper()
        nuevo_cuit = c2.text_input("CUIT")
        nuevo_tel = c3.text_input("Teléfono")
        nuevo_mail = c4.text_input("Mail")

        c5, c6, c7, c8 = st.columns(4)
        nueva_dir = c5.text_input("Dirección")
        nueva_loc = c6.text_input("Localidad")
        nueva_prov = c7.text_input("Provincia")
        nuevo_estado = c8.selectbox("Estado", ["Habilitada", "Inhabilitada"])

        if st.button("Guardar cliente"):
            if nuevo_cliente == "":
                st.error("El cliente es obligatorio.")
            else:
                con = conectar()
                con.execute(
                    """
                    INSERT OR IGNORE INTO clientes
                    (cliente, cuit, telefono, mail, direccion, localidad, provincia, estado)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (nuevo_cliente, nuevo_cuit, nuevo_tel, nuevo_mail, nueva_dir, nueva_loc, nueva_prov, nuevo_estado),
                )
                con.commit()
                con.close()
                st.success("Cliente guardado")
                st.rerun()

    st.markdown("## Clientes filtrados")
    mostrar_tabla_pro(df_vista)


elif menu == "Productos":
    st.markdown('<span class="badge">Productos</span>', unsafe_allow_html=True)

    st.markdown("## Actualizar lista de precios")
    st.caption("Subí acá el nuevo Excel de precios. La app reemplaza precios.xlsx y se actualiza automáticamente.")

    archivo_precios_nuevo = st.file_uploader(
        "Subir nuevo Excel de precios",
        type=["xlsx"],
        key="subir_nueva_lista_precios"
    )

    if archivo_precios_nuevo is not None:
        try:
            if os.path.exists("precios.xlsx"):
                respaldo = f"precios_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                with open("precios.xlsx", "rb") as original:
                    with open(respaldo, "wb") as backup:
                        backup.write(original.read())

            with open("precios.xlsx", "wb") as f:
                f.write(archivo_precios_nuevo.getbuffer())

            st.success("Lista de precios actualizada correctamente. La app se recargará con los nuevos precios.")
            st.rerun()

        except Exception as e:
            st.error(f"No pude actualizar la lista de precios: {e}")

    st.markdown('<div class="blue-line"></div>', unsafe_allow_html=True)

    st.markdown("## Actualizar reglas de comisión por venta")
    st.caption("Opcional: subí un Excel con columnas Categoria, Palabras clave, Hasta 250, 250 a 500, Mas 500, Fijo y Prioridad.")

    archivo_comisiones_nuevo = st.file_uploader(
        "Subir Excel de comisiones de venta",
        type=["xlsx"],
        key="subir_comisiones_venta"
    )

    if archivo_comisiones_nuevo is not None:
        try:
            df_com_new = pd.read_excel(archivo_comisiones_nuevo)
            df_com_new.columns = [str(c).strip().lower() for c in df_com_new.columns]

            def col_find(opciones):
                for op in opciones:
                    for c in df_com_new.columns:
                        if op in c:
                            return c
                return None

            c_cat = col_find(["categoria", "categoría", "producto"])
            c_pal = col_find(["palabra", "clave", "keyword"])
            c_bajo = col_find(["hasta", "250"])
            c_med = col_find(["500", "medio"])
            c_alto = col_find(["mas", "más", "alto"])
            c_fijo = col_find(["fijo"])
            c_prio = col_find(["prioridad"])

            if c_cat is None or c_pal is None or c_bajo is None:
                st.error("El Excel debe tener como mínimo Categoria, Palabras clave y Hasta 250.")
            else:
                con = conectar()
                con.execute("DELETE FROM comisiones_venta")

                for _, r in df_com_new.iterrows():
                    categoria = limpiar_txt(r.get(c_cat, ""))
                    palabras = limpiar_txt(r.get(c_pal, ""))
                    if not categoria or not palabras:
                        continue

                    hasta = float(pd.to_numeric(r.get(c_bajo, 0), errors="coerce") or 0)
                    medio = float(pd.to_numeric(r.get(c_med, hasta), errors="coerce") or 0) if c_med else hasta
                    alto = float(pd.to_numeric(r.get(c_alto, medio), errors="coerce") or 0) if c_alto else medio
                    fijo = float(pd.to_numeric(r.get(c_fijo, 0), errors="coerce") or 0) if c_fijo else 0
                    prio = float(pd.to_numeric(r.get(c_prio, 100), errors="coerce") or 100) if c_prio else 100

                    con.execute("""
                        INSERT OR REPLACE INTO comisiones_venta
                        (categoria, palabras_clave, hasta_250, desde_250_500, mas_500, porcentaje_fijo, prioridad)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (categoria, palabras, hasta, medio, alto, fijo, prio))

                con.commit()
                con.close()
                st.success("Reglas de comisión actualizadas. La app recalculará las comisiones de venta.")
                st.rerun()

        except Exception as e:
            st.error(f"No pude actualizar las reglas de comisión: {e}")

    st.markdown("### Reglas actuales de comisión por venta")
    mostrar_tabla_pro(df_comisiones_venta.rename(columns={
        "categoria": "Categoría",
        "palabras_clave": "Palabras clave",
        "hasta_250": "Hasta 250M",
        "desde_250_500": "250M a 500M",
        "mas_500": "Más de 500M",
        "porcentaje_fijo": "Fijo",
        "prioridad": "Prioridad",
    }))

    st.markdown('<div class="blue-line"></div>', unsafe_allow_html=True)

    st.markdown("## Lista de precios completa")
    st.caption("Se muestran todos los productos detectados en precios.xlsx con su presentación y precio correspondiente.")

    precios_vista = df_precios.copy()

    columnas_precio = []
    for c in ["Producto", "Presentacion", "Kilos por Bulto", "Precio Lista"]:
        if c in precios_vista.columns:
            columnas_precio.append(c)

    buscar_producto = st.text_input("Buscar producto", placeholder="Escribí parte del nombre del producto...")

    if buscar_producto and "Producto" in precios_vista.columns:
        precios_vista = precios_vista[
            precios_vista["Producto"].astype(str).str.contains(buscar_producto, case=False, na=False)
        ]

    mostrar_tabla_pro(precios_vista, columnas=columnas_precio)

    st.markdown('<div class="blue-line"></div>', unsafe_allow_html=True)

    st.markdown("## Ventas por producto")
    periodo = st.selectbox("Período de ventas", ["Acumulado", "Ciclo actual", "Hoy"])

    if periodo == "Ciclo actual":
        base = df_ciclo_f.copy()
    elif periodo == "Hoy":
        base = df_pedidos_f[df_pedidos_f["Fecha"].dt.date == date.today()].copy() if not df_pedidos_f.empty else df_pedidos_f.copy()
    else:
        base = df_pedidos_f.copy()

    if base.empty:
        st.info("No hay ventas de productos con los filtros actuales.")
    else:
        productos = (
            base.groupby(["Producto", "Presentacion"], as_index=False)
            .agg(
                {
                    "Cantidad Bultos": "sum",
                    "Toneladas": "sum",
                    "Importe": "sum",
                    "Precio Lista": "mean",
                    "Precio Venta": "mean",
                }
            )
            .rename(columns={"Cantidad Bultos": "Bultos", "Importe": "Facturación"})
            .sort_values("Facturación", ascending=False)
        )

        mostrar_tabla_pro(productos)
        st.bar_chart(productos.head(10).set_index("Producto")["Facturación"])


elif menu == "Ciclo comercial":
    st.markdown('<span class="badge">Ciclo comercial</span>', unsafe_allow_html=True)
    st.markdown(f"## Ciclo actual: {periodo_actual}")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Facturación neta ciclo", fmt_ars(facturacion_neta_ciclo))
    with c2:
        metric_card("Toneladas ciclo", fmt_num(toneladas_ciclo))
    with c3:
        metric_card("Pedidos ciclo", pedidos_ciclo)
    with c4:
        metric_card("Comisión ciclo", fmt_ars(comision_ciclo))

    st.markdown("### Detalle de comisiones del ciclo actual")
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        metric_card("Comisión venta ciclo", fmt_ars(comision_venta_ciclo))
    with cc2:
        metric_card("Comisión cobranza ciclo", fmt_ars(comision_cobranza_ciclo))
    with cc3:
        metric_card("Comisión total ciclo", fmt_ars(comision_ciclo))

    df_cierres = leer_sql("cierres").rename(
        columns={
            "periodo": "Periodo",
            "fecha_cierre": "Fecha Cierre",
            "pedidos": "Pedidos",
            "facturacion": "Facturación",
            "toneladas": "Toneladas",
            "comision_total": "Comisión Total",
        }
    )

    if st.button("Guardar / actualizar cierre del ciclo actual", use_container_width=True):
        con = conectar()
        con.execute(
            """
            INSERT OR REPLACE INTO cierres (periodo, fecha_cierre, pedidos, facturacion, toneladas, comision_total)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (periodo_actual, str(datetime.now()), pedidos_ciclo, facturacion_ciclo, toneladas_ciclo, comision_ciclo),
        )
        con.commit()
        con.close()
        st.success("Ciclo guardado. No se pierde: queda registrado en el historial.")
        st.rerun()

    st.markdown("## Historial de ciclos guardados")
    if df_cierres.empty:
        st.info("Todavía no hay ciclos guardados. Cuando guardes un ciclo, aparecerá acá con sus comisiones.")
    else:
        st.dataframe(df_cierres.sort_values("Fecha Cierre", ascending=False), use_container_width=True)

elif menu == "Informes":
    st.markdown('<span class="badge">Informes</span>', unsafe_allow_html=True)

    st.markdown("## Informe diario")
    if df_pedidos_f.empty:
        st.info("No hay pedidos con los filtros actuales.")
    else:
        fechas = sorted(df_pedidos_f["Fecha"].dropna().dt.date.unique().tolist())
        fecha_sel = st.selectbox("Fecha", ["Todas"] + fechas)

        informe = df_pedidos_f.copy()
        if fecha_sel != "Todas":
            informe = informe[informe["Fecha"].dt.date == fecha_sel]

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Pedidos", informe["Pedido ID"].nunique())
        with c2:
            metric_card("Toneladas", fmt_num(informe["Toneladas"].sum()))
        with c3:
            metric_card("Facturación", fmt_ars(informe["Importe"].sum()))
        with c4:
            metric_card("Comisión", fmt_ars(informe["Comisión Total"].sum()))

        mostrar_tabla_pro(informe)

    st.markdown("## Cuenta corriente")
    mostrar_tabla_pro(
        cuenta_corriente_f,
        columnas=["Cliente", "Total Vendido", "Notas de Crédito", "Venta Neta", "Pedidos", "Cobrado por Pedido", "Pagos Manuales", "Total Cobrado", "Saldo Pendiente", "Estado Cuenta"]
    )

    st.markdown("## Pagos manuales")
    mostrar_tabla_pro(df_pagos_f.sort_values(["Fecha", "Hora"], ascending=[False, False]))

    st.markdown("## Notas de crédito")
    mostrar_tabla_pro(df_notas_credito_f.sort_values("Fecha", ascending=False))

    st.markdown("## Visitas")
    mostrar_tabla_pro(df_visitas_f.sort_values(["Fecha", "Hora"], ascending=[False, False]))


# ============================================================
# EXPORTAR
# ============================================================
st.markdown('<div class="blue-line"></div>', unsafe_allow_html=True)

hojas = {
    "Pedidos": df_pedidos_f,
    "Pedidos Ciclo": df_ciclo_f,
    "Clientes": df_vista,
    "Cuenta Corriente": cuenta_corriente_f,
    "Precios": df_precios,
    "Visitas": df_visitas_f,
    "Pagos Manuales": df_pagos_f,
    "Notas de Crédito": df_notas_credito_f,
    "Objetivos": df_objetivos,
    "Reglas Comisión Venta": df_comisiones_venta,
}

excel = descargar_excel(hojas)

st.download_button(
    "Descargar informe completo filtrado",
    excel,
    "informe_clientes.xlsx",
    use_container_width=True,
)
