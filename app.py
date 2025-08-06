import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
from streamlit_autorefresh import st_autorefresh 
from io import BytesIO
import base64
from PIL import Image
import plotly.express as px
import streamlit.components.v1 as components
from datetime import datetime
st.session_state.page_height = 900  # ou use st.window_height, futuramente
# Configuração de locale removida para compatibilidade com Streamlit Cloud
# import locale
# try:
#     locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
# except (locale.Error, OSError):
#     try:
#         locale.setlocale(locale.LC_TIME, 'pt_BR')
#     except (locale.Error, OSError):
#         pass

# ---- Tela cheia + tema escuro da PRECS ----
st.set_page_config(
    page_title="Precs Propostas", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo elegante com tema escuro e dourado
st.markdown("""
    <style>
    /* Reset e configurações gerais */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Esconder header do Streamlit */
    header {
        visibility: hidden;
    }
    
    /* Fundo escuro elegante */
    body {
        background: #0a0a0a !important;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        overflow-x: hidden;
    }
    
    /* Container principal */
    .main {
        background: #0a0a0a !important;
        padding: 0;
    }
    
    .stApp {
        background: #0a0a0a !important;
        padding: 1rem;
        max-width: 100%;
    }
    
    /* Títulos com gradiente dourado */
    h1, h2, h3, h4 {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
    }
    
    /* Botões modernos */
    .stButton>button {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #000;
        border-radius: 15px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 14px;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(45deg, #FFA500, #FFD700);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5);
    }
    
    /* Container principal */
    .block-container {
        background: #1a1a1a;
        border-radius: 15px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar estilizada */
    .css-1v0mbdj {
        background: #1a1a1a !important;
        color: white;
        border-right: 2px solid #FFD700;
    }
    
    .css-1d391kg {
        background: #1a1a1a !important;
    }
    
    /* DataFrames */
    .stDataFrame {
        background: rgba(26, 26, 26, 0.9);
        color: white;
        border-radius: 15px;
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    
    /* Cards simples */
    .glass-card {
        background: #1a1a1a;
        border-radius: 12px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Animações suaves */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .slide-in-left {
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* Scrollbar personalizada */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #FFA500, #FFD700);
    }
    
    /* Responsividade otimizada para 100% de escala */
    @media screen and (min-width: 1400px) {
        .stApp {
            padding: 1.5rem;
        }
        
        .block-container {
            padding: 2rem;
        }
        
        .glass-card {
            padding: 20px;
        }
        
        h1 { font-size: 2.5rem !important; }
        h2 { font-size: 2rem !important; }
        h3 { font-size: 1.8rem !important; }
        h4 { font-size: 1.3rem !important; }
        
        table {
            font-size: 0.9rem !important;
        }
        
        .stButton>button {
            font-size: 0.9rem !important;
            padding: 10px 20px !important;
        }
    }
    
    @media screen and (min-width: 1200px) and (max-width: 1399px) {
        .stApp {
            padding: 1rem;
        }
        
        .block-container {
            padding: 1.5rem;
        }
        
        .glass-card {
            padding: 18px;
        }
        
        h1 { font-size: 2.2rem !important; }
        h2 { font-size: 1.8rem !important; }
        h3 { font-size: 1.5rem !important; }
        h4 { font-size: 1.1rem !important; }
        
        table {
            font-size: 0.85rem !important;
        }
        
        .stButton>button {
            font-size: 0.85rem !important;
            padding: 8px 16px !important;
        }
    }
    
    @media screen and (max-width: 1199px) {
        .stApp {
            padding: 0.8rem;
        }
        
        .block-container {
            padding: 1.2rem;
        }
        
        .glass-card {
            padding: 15px;
        }
        
        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.6rem !important; }
        h3 { font-size: 1.3rem !important; }
        h4 { font-size: 1rem !important; }
        
        table {
            font-size: 0.8rem !important;
        }
        
        .stButton>button {
            font-size: 0.8rem !important;
            padding: 8px 14px !important;
        }
    }
    
    /* Ajustes específicos para 100% de escala */
    @media screen and (min-width: 1000px) {
        .stColumns {
            gap: 1rem !important;
        }
        
        .glass-card {
            margin: 8px 0 !important;
        }
        
        /* Reduzir tamanho das imagens */
        img {
            max-width: 100% !important;
            height: auto !important;
        }
        
        /* Ajustar altura da tabela */
        .tabela-container {
            max-height: 70vh !important;
            overflow-y: auto !important;
        }
        
        /* Otimizar espaçamentos */
        .block-container {
            margin: 0.5rem 0 !important;
        }
        
        /* Reduzir padding dos cards */
        .glass-card {
            padding: 15px !important;
        }
        
        /* Ajustar tamanho das fontes */
        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.6rem !important; }
        h3 { font-size: 1.4rem !important; }
        h4 { font-size: 1.1rem !important; }
        
        /* Otimizar tabela */
        table {
            font-size: 0.85rem !important;
        }
        
        /* Reduzir altura das barras de progresso */
        .progress-bar {
            height: 14px !important;
        }
    }
    
    /* Animação de pulse para o sino */
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
            filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.4));
        }
        50% {
            transform: scale(1.03);
            filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.6));
        }
    }
    
    /* Barras de progresso contornadas */
    .progress-bar {
        background: #2C2C2C;
        border-radius: 6px;
        border: 2px solid #FFD700;
        overflow: hidden;
        position: relative;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);
        margin: 2px;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.8s ease;
        position: relative;
        border: 1px solid rgba(255, 215, 0, 0.5);
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Efeitos de brilho sutis */
    .glow {
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
    }
    
    .glow:hover {
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.5);
    }
    
    /* Esconder botão "Manage app" do Streamlit Cloud */
    .stDeployButton {
        display: none !important;
    }
    
    /* Esconder outros elementos do Streamlit Cloud */
    [data-testid="stDeployButton"] {
        display: none !important;
    }
    
    /* Sidebar elegante e oculta por padrão */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%) !important;
        color: white !important;
        border-right: 2px solid #FFD700 !important;
        min-width: 280px !important;
        max-width: 350px !important;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Estilizar elementos da sidebar */
    .css-1v0mbdj .stSelectbox > div > div {
        background: rgba(42, 42, 42, 0.9) !important;
        color: white !important;
        border: 1px solid rgba(255, 215, 0, 0.4) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(5px) !important;
    }
    
    .css-1v0mbdj .stMultiSelect > div > div {
        background: rgba(42, 42, 42, 0.9) !important;
        color: white !important;
        border: 1px solid rgba(255, 215, 0, 0.4) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(5px) !important;
    }
    
    .css-1v0mbdj .stDateInput > div > div {
        background: rgba(42, 42, 42, 0.9) !important;
        color: white !important;
        border: 1px solid rgba(255, 215, 0, 0.4) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(5px) !important;
    }
    
    /* Estilizar checkbox da sidebar */
    .css-1v0mbdj .stCheckbox > div {
        background: rgba(42, 42, 42, 0.9) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 8px !important;
        margin: 4px 0 !important;
    }
    
    /* Estilizar headers da sidebar */
    .css-1v0mbdj h1, .css-1v0mbdj h2, .css-1v0mbdj h3 {
        background: linear-gradient(45deg, #FFD700, #FFA500) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-shadow: 0 0 8px rgba(255, 215, 0, 0.3) !important;
        margin-bottom: 15px !important;
    }
    
    /* Hover effects para elementos da sidebar */
    .css-1v0mbdj .stSelectbox > div > div:hover,
    .css-1v0mbdj .stMultiSelect > div > div:hover,
    .css-1v0mbdj .stDateInput > div > div:hover {
        border-color: rgba(255, 215, 0, 0.8) !important;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.3) !important;
        transform: translateY(-1px) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Ajustar layout quando sidebar está oculta */
    .main .block-container {
        padding-left: 1rem !important;
        max-width: 100% !important;
    }
    
    /* Quando sidebar está oculta, expandir conteúdo */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .block-container {
        padding-left: 0 !important;
        margin-left: 0 !important;
        width: 100% !important;
    }
    
    /* Sidebar oculta por padrão, mas elegante quando visível */
    [data-testid="stSidebar"] {
        transition: all 0.3s ease !important;
    }
    
    /* Ocultar menu hambúrguer se existir */
    .css-1d391kg {
        display: none !important;
    }
    
    /* Permitir comportamento normal da sidebar */
    [data-testid="stSidebar"] {
        transition: all 0.3s ease !important;
    }
    
    /* Sidebar com comportamento dinâmico */
    section[data-testid="stSidebar"] {
        transition: all 0.3s ease !important;
    }
    
    /* Permitir que a sidebar seja dinâmica */
    .css-1v0mbdj {
        transition: all 0.3s ease !important;
    }
    
    /* Sidebar dinâmica - aparece e desaparece normalmente */
    [data-testid="stSidebar"] {
        transition: all 0.3s ease !important;
    }
    
    /* Ajustar colunas quando sidebar oculta */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .stColumns {
        width: 100% !important;
        margin-left: 0 !important;
    }
    
    /* Correção mais robusta para eliminar espaço vazio */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main {
        margin-left: 0 !important;
        padding-left: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Forçar layout full-width quando sidebar oculta */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .block-container {
        margin-left: 0 !important;
        padding-left: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Ajustar colunas para ocupar toda largura quando sidebar oculta */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .stColumns {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Ajustar colunas individuais quando sidebar oculta */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .stColumns > div {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Forçar container principal a ocupar toda largura */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main {
        width: 100% !important;
        max-width: 100% !important;
        margin-left: 0 !important;
        padding-left: 0 !important;
    }
    
    /* CSS mais agressivo para eliminar espaço vazio */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main {
        margin-left: 0 !important;
        padding-left: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        left: 0 !important;
        position: relative !important;
    }
    
    /* Forçar layout responsivo */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .block-container {
        margin-left: 0 !important;
        padding-left: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Ajustar colunas específicas */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .stColumns {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Ajustar colunas individuais */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .stColumns > div {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Forçar container principal */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main {
        width: 100% !important;
        max-width: 100% !important;
        margin-left: 0 !important;
        padding-left: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)



# ---- Autoatualização (a cada 10 segundos) ----
st_autorefresh(interval=70 * 1000, key="atualizacao")

print(f"Página atualizada em: {datetime.now().strftime('%H:%M:%S')}")

def image_to_base64(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()
    return img_b64

def formatar_data_pt_br():
    """Formata a data atual em português brasileiro sem depender de locale"""
    from datetime import datetime
    hoje = datetime.now()
    
    # Mapeamento de dias da semana
    dias_semana = {
        0: "Segunda-feira",
        1: "Terça-feira", 
        2: "Quarta-feira",
        3: "Quinta-feira",
        4: "Sexta-feira",
        5: "Sábado",
        6: "Domingo"
    }
    
    # Mapeamento de meses
    meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    
    dia_semana = dias_semana[hoje.weekday()]
    dia = hoje.day
    mes = meses[hoje.month]
    ano = hoje.year
    
    return f"{dia_semana} - {dia:02d}/{hoje.month:02d}/{ano}"

# ---- Carrega variáveis do .env ou Streamlit Secrets ----
try:
    # Tentar carregar do .env (desenvolvimento local)
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
except:
    # Usar Streamlit Secrets (produção)
    DB_HOST = st.secrets["DB_HOST"]
    DB_PORT = st.secrets["DB_PORT"]
    DB_NAME = st.secrets["DB_NAME"]
    DB_USER = st.secrets["DB_USER"]
    DB_PASSWORD = st.secrets["DB_PASSWORD"]

# ---- Conectar ao PostgreSQL ----
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode="require"
    )

# ---- Carregar dados ----
@st.cache_data(ttl=10)
def carregar_dados_propostas():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM dashmetas", conn)
    df["data"] = pd.to_datetime(df["data"])
    conn.close()
    return df

@st.cache_data(ttl=10)
def carregar_dados_campanhas():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM campanhas", conn)
    conn.close()
    return df

def atualizar_status_campanhas(campanhas_selecionadas):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE campanhas SET status_campanha = FALSE")
        for campanha in campanhas_selecionadas:
            cur.execute(
                "UPDATE campanhas SET status_campanha = TRUE WHERE nome_campanha = %s",
                (campanha,)
            )
        conn.commit()
    except Exception as e:
        st.error(f"Erro ao atualizar status das campanhas: {e}")
    finally:
        cur.close()
        conn.close()

def contar_propostas(df, df_original):
    # Garante que a coluna 'data' é datetime
    df['data'] = pd.to_datetime(df['data'])

    # Ordena pela data (da mais recente primeiro)
    df_sorted = df.sort_values(by='data', ascending=False)

    # Mantém a última vez que cada negócio passou por cada etapa
    df_ultimos = df_sorted.drop_duplicates(subset=['id_negocio', 'id_etapa'], keep='first')


    # Lista de todos os proprietários (caso queira usar depois)
    all_proprietarios = df_original['proprietario'].unique()

    # Contagem de negócios que passaram pela etapa 'Cálculo' (última vez de cada um)
    df_adquiridas = df_ultimos[df_ultimos['id_etapa'] == 'Cálculo'] \
        .groupby('proprietario').agg(quantidade_adquiridas=('id_negocio', 'nunique')).reset_index()

    # Contagem de negócios que passaram pela etapa 'Negociações iniciadas' (última vez de cada um)
    df_apresentadas = df_ultimos[df_ultimos['id_etapa'] == 'Negociações iniciadas'] \
        .groupby('proprietario').agg(quantidade_apresentadas=('id_negocio', 'nunique')).reset_index()

    # Garante todos os proprietários no resultado final
    df_adquiridas_full = pd.DataFrame({'proprietario': all_proprietarios}) \
        .merge(df_adquiridas, on='proprietario', how='left').fillna(0)
    
    df_apresentadas_full = pd.DataFrame({'proprietario': all_proprietarios}) \
        .merge(df_apresentadas, on='proprietario', how='left').fillna(0)

    # Junta os resultados
    return pd.merge(df_adquiridas_full, df_apresentadas_full, on='proprietario', how='outer').fillna(0)

def get_cor_barra(valor, maximo=6):
    if valor >= maximo:
        return "background: linear-gradient(45deg, #FFD700, #FFA500); box-shadow: 0 0 10px rgba(255, 215, 0, 0.6), 0 0 20px rgba(255, 215, 0, 0.4), 0 0 30px rgba(255, 215, 0, 0.2);"
    return "background: linear-gradient(45deg, #c3a43e, #d4af37); box-shadow: 0 0 5px rgba(195, 164, 62, 0.4);"



df_original = carregar_dados_propostas()
df = df_original.copy()
df_campanhas = carregar_dados_campanhas()

# ---- Sidebar ----
with st.sidebar:
    st.header("Filtros")
    mostrar_gestao = st.checkbox("Mostrar proprietário 'Gestão'", value=False)
    
    proprietarios_disponiveis = df["proprietario"].unique().tolist()
    if not mostrar_gestao:
        proprietarios_disponiveis = [p for p in proprietarios_disponiveis if p != "Gestão"]
    
    proprietarios = st.multiselect("Proprietário", options=proprietarios_disponiveis, default=proprietarios_disponiveis)
    etapas = st.multiselect("Etapa", df["id_etapa"].unique(), default=df["id_etapa"].unique())
    data_ini = st.date_input("Data inicial", df["data"].max().date())
    data_fim = st.date_input("Data final", df["data"].max().date())
    
    campanhas_disponiveis = df_campanhas["nome_campanha"].tolist()
    campanhas_selecionadas = st.multiselect(
        "Campanhas",
        options=campanhas_disponiveis,
        default=df_campanhas[df_campanhas["status_campanha"] == True]["nome_campanha"].tolist(),
        key="campanhas_filtro"
    )

atualizar_status_campanhas(campanhas_selecionadas)

if not mostrar_gestao:
    df = df[df["proprietario"] != "Gestão"]
    df_original = df_original[df_original["proprietario"] != "Gestão"]

df_filtrado = df.copy()
if proprietarios:
    df_filtrado = df_filtrado[df_filtrado["proprietario"].isin(proprietarios)]
if etapas:
    df_filtrado = df_filtrado[df_filtrado["id_etapa"].isin(etapas)]
df_filtrado = df_filtrado[
    (df_filtrado["data"].dt.date >= data_ini) &
    (df_filtrado["data"].dt.date <= data_fim)
]

df_propostas = contar_propostas(df_filtrado, df_original)
total_adquiridas = df_propostas['quantidade_adquiridas'].sum()
total_apresentadas = df_propostas['quantidade_apresentadas'].sum()

# Card de estatísticas removido conforme solicitado

# ---- Visualizações principais ----
col2, col1 = st.columns([1,3])

with col1:
    medalha_b64 = image_to_base64("medalha.png")
    if not df_propostas.empty:
        tabela_html = f"""
        <div class="glass-card fade-in-up" style="border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 10px; overflow: hidden; margin: 10px 0;">
            <h3 style='background: linear-gradient(45deg, #FFD700, #FFA500); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-align: center; font-size: 1.5rem; margin: 10px 0; text-shadow: 0 0 8px rgba(255, 215, 0, 0.3);'>
                Propostas Diárias
            </h3>
            <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; background: #1a1a1a; border-radius: 8px; overflow: hidden;">
            <thead>
                <tr style="border-bottom: 1px solid rgba(255, 215, 0, 0.3); background: #000000;">
                    <th style="font-size: 1rem; text-align: left; background: #000000; color: #FFD700; padding: 8px 12px; text-shadow: 0 0 3px rgba(255, 215, 0, 0.3);">Nome</th>
                    <th style="font-size: 1rem; text-align: center; background: #1A1A1A; color: #FFD700; padding: 8px 12px; text-shadow: 0 0 3px rgba(255, 215, 0, 0.3);">Adquiridas: {int(total_adquiridas)}/90</th>
                    <th style="font-size: 1rem; text-align: center; background: #333333; color: #FFD700; padding: 8px 12px; text-shadow: 0 0 3px rgba(255, 215, 0, 0.3);">Apresentadas: {int(total_apresentadas)}/90</th>
                </tr>
            </thead>
            <tbody>
        """

        maximo = 6
        for _, row in df_propostas.iterrows():
            nome = row['proprietario']
            valor1 = int(row['quantidade_adquiridas'])
            valor2 = int(row['quantidade_apresentadas'])
            medalha_html = f"""<img src="data:image/png;base64,{medalha_b64}" width="18" style="margin-left: 6px; vertical-align: middle;">""" \
                if valor1 >= 6 or valor2 >= 6 else ""
            
            proporcao1 = min(valor1 / maximo, 1.0)
            proporcao2 = min(valor2 / maximo, 1.0)
            cor_barra1 = get_cor_barra(valor1)
            cor_barra2 = get_cor_barra(valor2)

            barra1 = f"""
            <div class="progress-bar" style='width: 100%; height: 12px; margin-bottom: 4px; border: 2px solid #FFD700;'>
                <div class="progress-fill" style='width: {proporcao1*100:.1f}%; {cor_barra1} height: 100%; border: 1px solid rgba(255, 215, 0, 0.6);'></div>
            </div>
            <span style='font-size: 0.8rem; color: #FFD700; font-weight: bold; text-shadow: 0 0 2px rgba(255, 215, 0, 0.3);'>{valor1}/{maximo}</span>
            """

            barra2 = f"""
            <div class="progress-bar" style='width: 100%; height: 12px; margin-bottom: 4px; border: 2px solid #FFD700;'>
                <div class="progress-fill" style='width: {proporcao2*100:.1f}%; {cor_barra2} height: 100%; border: 1px solid rgba(255, 215, 0, 0.6);'></div>
            </div>
            <span style='font-size: 0.8rem; color: #FFD700; font-weight: bold; text-shadow: 0 0 2px rgba(255, 215, 0, 0.3);'>{valor2}/{maximo}</span>
            """

            tabela_html += f"""
            <tr style="border-bottom: 1px solid rgba(255, 215, 0, 0.2); background: #2a2a2a;">
                <td style="font-size: 0.9rem; background: #000000; padding: 6px 10px; color: #FFF; vertical-align: middle; text-align: left; text-shadow: 0 0 2px rgba(255, 255, 255, 0.3);">
                    {nome} {medalha_html}
                </td>
                <td style="padding: 6px 10px; background: #1A1A1A; color: #FFD700; vertical-align: middle; text-align: center; text-shadow: 0 0 2px rgba(255, 215, 0, 0.3);">
                    {barra1}
                </td>
                <td style="padding: 6px 10px; background: #333333; color: #FFD700; vertical-align: middle; text-align: center; text-shadow: 0 0 2px rgba(255, 215, 0, 0.3);">
                    {barra2}
                </td>
            </tr>
            """

        tabela_html += "</tbody></table></div>"
        components.html(tabela_html, height=1000, scrolling=False)


with col2:
    logo_b64 = image_to_base64("precs2.png")
    sino_b64 = image_to_base64("sino.png")  # Seu arquivo de sino
    
    st.markdown(f"""
        <div class="glass-card slide-in-left" style="display: flex; justify-content: center; align-items: center; text-align: center; margin-bottom: 20px;"> 
            <img src="data:image/png;base64,{logo_b64}" width="200" style="border-radius: 12px; box-shadow: 0 8px 25px rgba(255, 215, 0, 0.2); filter: drop-shadow(0 0 6px rgba(255, 215, 0, 0.3));">
        </div> 
    """, unsafe_allow_html=True)
    
    # Cabeçalho com logo e título
    st.markdown(f"""
        <div class="glass-card fade-in-up" style="display: flex; justify-content: center; align-items: center; text-align: center; margin-bottom: 15px;">
            <h1 style="background: linear-gradient(45deg, #FFD700, #FFA500); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2rem; margin: 0; text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);">Precs Propostas</h1> 
        </div>
        <div class="glass-card fade-in-up" style="text-align: center; margin-bottom: 15px;">
            <h3 style='background: linear-gradient(45deg, #C5A45A, #D4AF37); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 1rem; font-weight: bold; text-shadow: 0 0 8px rgba(197, 164, 90, 0.3);'>
                {formatar_data_pt_br()}
            </h3>
        </div>
    """, unsafe_allow_html=True)

    # Título das campanhas + sino
    st.markdown("""
        <div class="glass-card fade-in-up" style="text-align: center; margin-bottom: 15px;">
            <h2 style='background: linear-gradient(45deg, #D4AF37, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-shadow: 0 0 8px rgba(212, 175, 55, 0.3);'>Campanhas Ativas</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="glass-card fade-in-up" style='text-align: center; margin-bottom: 15px;'>
            <img src="data:image/png;base64,{sino_b64}" width="100px;" style="filter: drop-shadow(0 0 8px rgba(255, 215, 0, 0.4)); animation: pulse 2s ease-in-out infinite;">
        </div>
    """, unsafe_allow_html=True)

    # Lista de campanhas
    campanhas_ativas = df_campanhas[df_campanhas["status_campanha"] == True]
    for i, (_, campanha) in enumerate(campanhas_ativas.iterrows()):
        st.markdown(f"""
            <div class="glass-card fade-in-up" style="display: flex; justify-content: center; align-items: center; text-align: center; margin-bottom: 8px; padding: 12px; animation-delay: {i * 0.2}s;">
                <span style="font-size: 1.2rem; background: linear-gradient(45deg, #FFF, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-shadow: 0 0 8px rgba(255, 255, 255, 0.3);">{campanha['nome_campanha']}</span>
            </div>
        """, unsafe_allow_html=True)
