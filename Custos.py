"""
SYSCOST - Sistema de Apuração de Resultados e Gestão de Custos
Versão Streamlit para fins didáticos
Baseado no cronograma da disciplina de Gestão de Custos
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import base64
from jinja2 import Template
import json

# ─── CONFIGURAÇÃO DA PÁGINA ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="SysCost - Gestão de Custos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── ESTILOS CSS PERSONALIZADOS ────────────────────────────────────────────────
st.markdown("""
<style>
    /* Estilos globais */
    .main {
        background-color: #0d1117;
    }
    .stApp {
        background-color: #0d1117;
    }
    .stSidebar {
        background-color: #161b22;
    }
    .stSidebar .sidebar-content {
        background-color: #161b22;
    }
    
    /* Cards personalizados */
    .custom-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .custom-card-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #8d96a0;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .custom-card-title::before {
        content: '';
        display: block;
        width: 3px;
        height: 14px;
        background: #58a6ff;
        border-radius: 2px;
    }
    
    /* KPIs */
    .kpi-container {
        background-color: #1c2330;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 14px 16px;
    }
    .kpi-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #8d96a0;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 22px;
        font-weight: 700;
    }
    .kpi-sub {
        font-size: 11px;
        color: #8d96a0;
        margin-top: 2px;
        font-family: 'IBM Plex Mono', monospace;
    }
    
    /* Tags */
    .tag {
        display: inline-block;
        font-size: 10px;
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        padding: 2px 7px;
        border-radius: 12px;
    }
    
    /* Alertas */
    .alert-info {
        background-color: #1f468020;
        border: 1px solid #1f4680;
        color: #cae8ff;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 13px;
        margin-bottom: 12px;
    }
    .alert-warn {
        background-color: #d2992220;
        border: 1px solid #d2992260;
        color: #f0e68c;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 13px;
        margin-bottom: 12px;
    }
    .alert-success {
        background-color: #196c2e20;
        border: 1px solid #196c2e;
        color: #aff5b4;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 13px;
        margin-bottom: 12px;
    }
    .alert-danger {
        background-color: #6e1c1a20;
        border: 1px solid #6e1c1a;
        color: #ffa198;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 13px;
        margin-bottom: 12px;
    }
    
    /* Métricas do Streamlit */
    [data-testid="metric-container"] {
        background-color: #1c2330;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 14px 16px;
    }
    [data-testid="metric-container"] label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10px !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #8d96a0 !important;
    }
    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 22px !important;
        font-weight: 700 !important;
    }
    
    /* Dataframes */
    .stDataFrame {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    .stDataFrame thead tr th {
        background-color: #21262d !important;
        color: #8d96a0 !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 0.06em !important;
    }
    
    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox select, .stTextArea textarea {
        background-color: #1c2330 !important;
        border: 1px solid #30363d !important;
        color: #e6edf3 !important;
        border-radius: 6px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
        border-color: #58a6ff !important;
    }
    
    /* Botões */
    .stButton button {
        border-radius: 6px !important;
        font-weight: 500 !important;
        transition: all 0.15s !important;
    }
    .stButton button:focus {
        box-shadow: none !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px !important;
        background-color: #161b22 !important;
        border-bottom: 1px solid #30363d !important;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 20px !important;
        color: #8d96a0 !important;
        border-bottom: 2px solid transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #e6edf3 !important;
        border-bottom-color: #58a6ff !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        font-family: 'IBM Plex Mono', monospace !important;
    }
    .streamlit-expanderContent {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }
    
    /* Upload */
    .stFileUploader > div {
        border: 2px dashed #30363d !important;
        border-radius: 10px !important;
        background-color: #161b22 !important;
        padding: 28px !important;
        text-align: center !important;
        transition: all 0.15s !important;
    }
    .stFileUploader > div:hover {
        border-color: #58a6ff !important;
        background-color: #58a6ff0a !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── UTILITÁRIOS ────────────────────────────────────────────────────────────────

def fmt(v, d=2):
    """Formata um número com casas decimais"""
    try:
        return f"{float(v or 0):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return f"0,{'0' * d}"

def fmtR(v):
    """Formata como moeda R$"""
    return f"R$ {fmt(v)}"

def fmtP(v):
    """Formata como percentual"""
    return f"{fmt(v)}%"

def num(v):
    """Converte para float, retorna 0 se inválido"""
    try:
        return float(v) if v is not None and v != "" else 0.0
    except:
        return 0.0

def safe_div(a, b):
    """Divisão segura com tratamento de zero"""
    return a / b if b != 0 else 0

# ─── DADOS INICIAIS ──────────────────────────────────────────────────────────────

def get_initial_state():
    """Retorna o estado inicial da aplicação"""
    return {
        # Dados da empresa
        "nome_empresa": "Estrela Ltda",
        "periodo": "Janeiro/2026",
        "regime": "Lucro Real",
        
        # Plano de Contas - ESTRUTURA CORRIGIDA
        # Removido "codigo" - agora apenas: nome, tipo, natureza, comportamento
        # Tipos de gasto: receita, custo_direto, custo_indireto, despesa, investimento, perda
        # Natureza (para custos): direto, indireto
        # Comportamento: fixo, variavel, semivariavel, ---
        "plano_contas": [
            # === RECEITAS ===
            {"id": 1, "nome": "Receita Bruta de Vendas", "tipo": "receita", "natureza": "---", "comportamento": "---"},
            {"id": 2, "nome": "Deduções de Vendas", "tipo": "receita", "natureza": "---", "comportamento": "---"},
            
            # === CUSTOS DIRETOS ===
            {"id": 3, "nome": "Matéria-Prima Consumida", "tipo": "custo_direto", "natureza": "direto", "comportamento": "variavel"},
            {"id": 4, "nome": "Material de Embalagem", "tipo": "custo_direto", "natureza": "direto", "comportamento": "variavel"},
            {"id": 5, "nome": "Mão de Obra Direta", "tipo": "custo_direto", "natureza": "direto", "comportamento": "variavel"},
            
            # === CUSTOS INDIRETOS ===
            {"id": 6, "nome": "Mão de Obra Indireta", "tipo": "custo_indireto", "natureza": "indireto", "comportamento": "fixo"},
            {"id": 7, "nome": "Aluguel da Fábrica", "tipo": "custo_indireto", "natureza": "indireto", "comportamento": "fixo"},
            {"id": 8, "nome": "Depreciação de Máquinas", "tipo": "custo_indireto", "natureza": "indireto", "comportamento": "fixo"},
            {"id": 9, "nome": "Manutenção de Equipamentos", "tipo": "custo_indireto", "natureza": "indireto", "comportamento": "semivariavel"},
            {"id": 10, "nome": "Energia Elétrica - Fábrica (fixa)", "tipo": "custo_indireto", "natureza": "indireto", "comportamento": "fixo"},
            {"id": 11, "nome": "Energia Elétrica - Fábrica (variável)", "tipo": "custo_indireto", "natureza": "indireto", "comportamento": "variavel"},
            {"id": 12, "nome": "Materiais de Consumo (fábrica)", "tipo": "custo_indireto", "natureza": "indireto", "comportamento": "variavel"},
            {"id": 13, "nome": "Seguros da Fábrica", "tipo": "custo_indireto", "natureza": "indireto", "comportamento": "fixo"},
            
            # === DESPESAS ADMINISTRATIVAS ===
            {"id": 14, "nome": "Salários Administrativos", "tipo": "despesa", "natureza": "---", "comportamento": "fixo"},
            {"id": 15, "nome": "Aluguel Administrativo", "tipo": "despesa", "natureza": "---", "comportamento": "fixo"},
            {"id": 16, "nome": "Depreciação de Equipamentos Adm.", "tipo": "despesa", "natureza": "---", "comportamento": "fixo"},
            
            # === DESPESAS COMERCIAIS ===
            {"id": 17, "nome": "Comissões sobre Vendas", "tipo": "despesa", "natureza": "---", "comportamento": "variavel"},
            {"id": 18, "nome": "Propaganda e Publicidade", "tipo": "despesa", "natureza": "---", "comportamento": "semivariavel"},
            {"id": 19, "nome": "Frete sobre Vendas", "tipo": "despesa", "natureza": "---", "comportamento": "variavel"},
            
            # === DESPESAS FINANCEIRAS ===
            {"id": 20, "nome": "Juros Passivos", "tipo": "despesa", "natureza": "---", "comportamento": "fixo"},
            {"id": 21, "nome": "Despesas Bancárias", "tipo": "despesa", "natureza": "---", "comportamento": "variavel"},
            
            # === INVESTIMENTOS E PERDAS ===
            {"id": 22, "nome": "Aquisição de Máquinas", "tipo": "investimento", "natureza": "---", "comportamento": "---"},
            {"id": 23, "nome": "Perdas com Mercadorias", "tipo": "perda", "natureza": "---", "comportamento": "---"},
            {"id": 24, "nome": "Perdas com Inadimplência", "tipo": "perda", "natureza": "---", "comportamento": "---"},
        ],
        
        # Produtos
        "produtos": [
            {"id": 1, "nome": "Produto A", "unidade": "un"},
            {"id": 2, "nome": "Produto B", "unidade": "kg"},
            {"id": 3, "nome": "Produto C", "unidade": "cx"},
        ],
        
        # Vendas
        "vendas": [
            {"produto_id": 1, "qtd": 500, "preco_unit": 120, "custo_unit": 65, "custo_direto": 55, "impostos": 12},
            {"produto_id": 2, "qtd": 300, "preco_unit": 85, "custo_unit": 40, "custo_direto": 32, "impostos": 8.5},
            {"produto_id": 3, "qtd": 200, "preco_unit": 200, "custo_unit": 100, "custo_direto": 80, "impostos": 20},
        ],
        
        # Despesas - ajustado para contas indiretas e despesas
        "despesas": [
            {"conta_id": 6, "valor": 25000, "rateio": "proporcional"},  # Mão de Obra Indireta
            {"conta_id": 7, "valor": 8000, "rateio": "proporcional"},   # Aluguel da Fábrica
            {"conta_id": 8, "valor": 5000, "rateio": "proporcional"},   # Depreciação de Máquinas
            {"conta_id": 9, "valor": 3500, "rateio": "proporcional"},   # Manutenção de Equipamentos
            {"conta_id": 10, "valor": 2000, "rateio": "proporcional"},  # Energia Elétrica - Fábrica (fixa)
            {"conta_id": 11, "valor": 1500, "rateio": "proporcional"},  # Energia Elétrica - Fábrica (variável)
            {"conta_id": 12, "valor": 1000, "rateio": "proporcional"},  # Materiais de Consumo (fábrica)
            {"conta_id": 13, "valor": 3000, "rateio": "proporcional"},  # Seguros da Fábrica
            {"conta_id": 14, "valor": 18000, "rateio": "---"},          # Salários Administrativos
            {"conta_id": 15, "valor": 4000, "rateio": "---"},           # Aluguel Administrativo
            {"conta_id": 16, "valor": 2000, "rateio": "---"},           # Depreciação de Equipamentos Adm.
            {"conta_id": 17, "valor": 0, "rateio": "---"},              # Comissões sobre Vendas (calculada)
            {"conta_id": 18, "valor": 4000, "rateio": "---"},           # Propaganda e Publicidade
            {"conta_id": 19, "valor": 0, "rateio": "---"},              # Frete sobre Vendas (calculado)
            {"conta_id": 20, "valor": 1500, "rateio": "---"},           # Juros Passivos
            {"conta_id": 21, "valor": 500, "rateio": "---"},            # Despesas Bancárias
        ],
        
        # Estoque
        "estoque_inicial": [
            {"produto_id": 1, "qtd": 80, "custo_medio": 63},
            {"produto_id": 2, "qtd": 50, "custo_medio": 38},
            {"produto_id": 3, "qtd": 30, "custo_medio": 97},
        ],
        "estoque_final": [
            {"produto_id": 1, "qtd": 60, "custo_medio": 65},
            {"produto_id": 2, "qtd": 40, "custo_medio": 40},
            {"produto_id": 3, "qtd": 20, "custo_medio": 100},
        ],
        "producao_mes": [
            {"produto_id": 1, "qtd": 480},
            {"produto_id": 2, "qtd": 290},
            {"produto_id": 3, "qtd": 190},
        ],
        
        # Comissão
        "comissao_perc": 5,
        
        # Critérios de rateio
        "criterios_rateio": [
            {"id": "proporcional", "nome": "Proporcional à Receita", "base": "receita", "tipo": "sistema"},
            {"id": "igual", "nome": "Igual entre Produtos", "base": "igual", "tipo": "sistema"},
            {"id": "custo", "nome": "Proporcional ao Custo", "base": "custo", "tipo": "sistema"},
            {"id": "qtd", "nome": "Proporcional à Quantidade", "base": "qtd", "tipo": "sistema"},
        ],
        
        # Pesos manuais para rateio
        "pesos_rateio": {},
        
        # Configurações de precificação
        "markup_perc": {1: 30, 2: 25, 3: 35},
        "preco_mercado": {1: 125, 2: 90, 3: 210},
        
        # Laudo
        "laudo": {
            "analista": "",
            "data": datetime.now().strftime("%d/%m/%Y"),
            "situacao_geral": "",
            "pontos_fortes": "",
            "pontos_fracos": "",
            "recomendacoes": "",
            "observacoes": "",
        }
    }

# ─── FUNÇÕES DE CÁLCULO ──────────────────────────────────────────────────────────

def calcular_indicadores(state):
    """Calcula todos os indicadores financeiros e gerenciais"""
    vendas = state["vendas"]
    produtos = state["produtos"]
    despesas = state["despesas"]
    plano_contas = state["plano_contas"]
    comissao_perc = num(state["comissao_perc"])
    
    # Receita Bruta
    rb = sum(num(v["qtd"]) * num(v["preco_unit"]) for v in vendas)
    
    # Deduções de Vendas (impostos por produto)
    deducoes_perc = sum(
        num(v["qtd"]) * num(v["preco_unit"]) * num(v["impostos"]) / 100 
        for v in vendas
    )
    
    # Deduções do plano de contas
    deducoes_plano = sum(
        num(d["valor"]) for d in despesas
        if any(c["id"] == d["conta_id"] and c["tipo"] == "receita" and "dedução" in c["nome"].lower() for c in plano_contas)
    )
    deducoes = deducoes_perc + deducoes_plano
    
    # Comissões
    comissoes = rb * comissao_perc / 100
    
    # Receita Líquida
    rl = rb - deducoes - comissoes
    
    # CPV Direto (custos diretos)
    cpv_direto = sum(num(v["qtd"]) * num(v["custo_unit"]) for v in vendas)
    
    # Custos Indiretos (rateio)
    custos_indiretos = sum(
        num(d["valor"]) for d in despesas
        if any(c["id"] == d["conta_id"] and c["tipo"] == "custo_indireto" for c in plano_contas)
    )
    
    # Despesas (administrativas, comerciais, financeiras)
    despesas_operacionais = sum(
        num(d["valor"]) for d in despesas
        if any(c["id"] == d["conta_id"] and c["tipo"] == "despesa" for c in plano_contas)
    )
    
    # Custos e despesas variáveis
    custos_var = cpv_direto + comissoes
    
    # Margem de Contribuição
    mc = rl - custos_var
    mc_perc = safe_div(mc, rl) * 100
    
    # Custos Fixos (indiretos + despesas fixas)
    custos_fixos = custos_indiretos + sum(
        num(d["valor"]) for d in despesas
        if any(c["id"] == d["conta_id"] and c["comportamento"] == "fixo" and c["tipo"] == "despesa" for c in plano_contas)
    )
    
    # Depreciação (para PE Financeiro)
    depreciacao = sum(
        num(d["valor"]) for d in despesas
        if any(c["id"] == d["conta_id"] and ("depreciação" in c["nome"].lower() or "depreciacao" in c["nome"].lower()) for c in plano_contas)
    )
    custos_fixos_desembolsaveis = custos_fixos - depreciacao
    
    # Lucro desejado (30% dos custos fixos)
    lucro_desejado = custos_fixos * 0.3
    
    # Pontos de Equilíbrio
    pec = safe_div(custos_fixos, mc_perc / 100) if mc_perc > 0 else 0  # Contábil
    pef = safe_div(custos_fixos_desembolsaveis, mc_perc / 100) if mc_perc > 0 else 0  # Financeiro
    pee = safe_div((custos_fixos + lucro_desejado), mc_perc / 100) if mc_perc > 0 else 0  # Econômico
    
    # Margem de Segurança
    ms_abs = rl - pec
    ms_perc = safe_div(ms_abs, rl) * 100 if rl > 0 else 0
    qtd_total = sum(num(v["qtd"]) for v in vendas)
    ms_qtd = qtd_total * (ms_perc / 100)
    
    # Resultado Operacional - Absorção
    cpv_absorcao = cpv_direto + custos_indiretos
    lb_absorcao = rl - cpv_absorcao
    lo_absorcao = lb_absorcao - despesas_operacionais
    ircsll_abs = lo_absorcao * 0.34 if lo_absorcao > 0 else 0
    ll_absorcao = lo_absorcao - ircsll_abs
    
    # Resultado Operacional - Variável
    lo_variavel = mc - custos_fixos
    ircsll_var = lo_variavel * 0.34 if lo_variavel > 0 else 0
    ll_variavel = lo_variavel - ircsll_var
    
    return {
        "rb": rb,
        "deducoes": deducoes,
        "deducoes_perc": deducoes_perc,
        "deducoes_plano": deducoes_plano,
        "comissoes": comissoes,
        "rl": rl,
        "cpv_direto": cpv_direto,
        "custos_indiretos": custos_indiretos,
        "custos_var": custos_var,
        "mc": mc,
        "mc_perc": mc_perc,
        "custos_fixos": custos_fixos,
        "depreciacao": depreciacao,
        "custos_fixos_desembolsaveis": custos_fixos_desembolsaveis,
        "lucro_desejado": lucro_desejado,
        "pec": pec,
        "pef": pef,
        "pee": pee,
        "ms_abs": ms_abs,
        "ms_perc": ms_perc,
        "ms_qtd": ms_qtd,
        "qtd_total": qtd_total,
        "cpv_absorcao": cpv_absorcao,
        "lb_absorcao": lb_absorcao,
        "despesas_operacionais": despesas_operacionais,
        "lo_absorcao": lo_absorcao,
        "ircsll_abs": ircsll_abs,
        "ll_absorcao": ll_absorcao,
        "lo_variavel": lo_variavel,
        "ircsll_var": ircsll_var,
        "ll_variavel": ll_variavel,
    }

def calcular_rateio(state, conta_id, criterio_id):
    """Calcula a distribuição de uma despesa por critério de rateio"""
    vendas = state["vendas"]
    produtos = state["produtos"]
    criterios = state["criterios_rateio"]
    pesos = state.get("pesos_rateio", {})
    
    # Encontra o critério
    criterio = next((c for c in criterios if c["id"] == criterio_id), None)
    if not criterio:
        return []
    
    base = criterio["base"]
    n_prod = len(produtos)
    
    # Calcula totais para bases
    receita_total = sum(num(v["qtd"]) * num(v["preco_unit"]) for v in vendas)
    custo_total = sum(num(v["qtd"]) * num(v["custo_unit"]) for v in vendas)
    qtd_total = sum(num(v["qtd"]) for v in vendas)
    
    resultado = []
    for i, v in enumerate(vendas):
        produto = next((p for p in produtos if p["id"] == v["produto_id"]), None)
        nome = produto["nome"] if produto else f"Produto {i+1}"
        
        if base == "manual":
            # Pesos manuais
            pesos_crit = pesos.get(criterio_id, {})
            peso = num(pesos_crit.get(v["produto_id"], 0))
            total_peso = sum(num(pesos_crit.get(p["id"], 0)) for p in produtos)
            perc = safe_div(peso, total_peso)
        elif base == "receita":
            rec = num(v["qtd"]) * num(v["preco_unit"])
            perc = safe_div(rec, receita_total)
        elif base == "custo":
            cst = num(v["qtd"]) * num(v["custo_unit"])
            perc = safe_div(cst, custo_total)
        elif base == "qtd":
            qtd = num(v["qtd"])
            perc = safe_div(qtd, qtd_total)
        else:  # igual
            perc = 1 / n_prod if n_prod > 0 else 0
        
        # Encontra o valor da despesa
        despesa = next((d for d in state["despesas"] if d["conta_id"] == conta_id), None)
        valor = num(despesa["valor"]) if despesa else 0
        
        resultado.append({
            "produto": nome,
            "produto_id": v["produto_id"],
            "perc": perc * 100,
            "valor": valor * perc
        })
    
    return resultado

# ─── FUNÇÕES DE UI ──────────────────────────────────────────────────────────────

def render_kpi(label, value, sub=None, color="#e6edf3"):
    """Renderiza um KPI no estilo da aplicação"""
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color: {color}">{value}</div>
        {f'<div class="kpi-sub">{sub}</div>' if sub else ''}
    </div>
    """, unsafe_allow_html=True)

def render_tag(text, color="#58a6ff"):
    """Renderiza uma tag"""
    st.markdown(f'<span class="tag" style="background: {color}22; color: {color}">{text}</span>', unsafe_allow_html=True)

def render_alert(message, type="info"):
    """Renderiza um alerta"""
    type_map = {
        "info": "alert-info",
        "warn": "alert-warn", 
        "success": "alert-success",
        "danger": "alert-danger"
    }
    st.markdown(f'<div class="{type_map.get(type, "alert-info")}">{message}</div>', unsafe_allow_html=True)

# ─── MÓDULOS DA APLICAÇÃO ──────────────────────────────────────────────────────

def modulo_plano_contas():
    """Módulo: Plano de Contas"""
    st.header("📋 Plano de Contas")
    
    render_alert("""
    O plano de contas classifica os gastos da empresa. 
    Para cada conta, identifique:
    - <strong>Tipo de Gasto</strong>: Receita, Custo Direto, Custo Indireto, Despesa, Investimento ou Perda
    - <strong>Natureza</strong> (para custos): Direto ou Indireto
    - <strong>Comportamento</strong>: Fixo, Variável ou Semivariável
    """)
    
    # Importar planilha
    with st.expander("📥 Importar Plano de Contas (XLSX/CSV)"):
        uploaded_file = st.file_uploader(
            "Arraste ou selecione uma planilha",
            type=["xlsx", "xls", "csv"],
            key="plano_upload"
        )
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(('.xlsx', '.xls')) else pd.read_csv(uploaded_file)
                
                col_nome = next((c for c in df.columns if 'nome' in c.lower() or 'conta' in c.lower()), None)
                if col_nome is None:
                    st.error("Coluna 'Nome' não encontrada. Verifique o cabeçalho da planilha.")
                else:
                    col_tipo = next((c for c in df.columns if 'tipo' in c.lower()), None)
                    col_natureza = next((c for c in df.columns if 'natureza' in c.lower()), None)
                    col_comportamento = next((c for c in df.columns if 'comportamento' in c.lower()), None)
                    
                    novas_contas = []
                    for _, row in df.iterrows():
                        if pd.isna(row[col_nome]):
                            continue
                        conta = {
                            "id": len(st.session_state.plano_contas) + len(novas_contas) + 1000,
                            "nome": str(row[col_nome]),
                            "tipo": "despesa",
                            "natureza": "---",
                            "comportamento": "---"
                        }
                        if col_tipo and not pd.isna(row[col_tipo]):
                            tipo = str(row[col_tipo]).lower()
                            if "receita" in tipo:
                                conta["tipo"] = "receita"
                            elif "custo_direto" in tipo or "direto" in tipo:
                                conta["tipo"] = "custo_direto"
                            elif "custo_indireto" in tipo or "indireto" in tipo:
                                conta["tipo"] = "custo_indireto"
                            elif "investimento" in tipo:
                                conta["tipo"] = "investimento"
                            elif "perda" in tipo:
                                conta["tipo"] = "perda"
                            else:
                                conta["tipo"] = "despesa"
                        if col_natureza and not pd.isna(row[col_natureza]):
                            nat = str(row[col_natureza]).lower()
                            if "direto" in nat:
                                conta["natureza"] = "direto"
                            elif "indireto" in nat:
                                conta["natureza"] = "indireto"
                        if col_comportamento and not pd.isna(row[col_comportamento]):
                            comp = str(row[col_comportamento]).lower()
                            if "fixo" in comp:
                                conta["comportamento"] = "fixo"
                            elif "variavel" in comp:
                                conta["comportamento"] = "variavel"
                            elif "semivariavel" in comp or "misto" in comp:
                                conta["comportamento"] = "semivariavel"
                        novas_contas.append(conta)
                    
                    if novas_contas:
                        st.session_state.plano_contas.extend(novas_contas)
                        st.success(f"✅ {len(novas_contas)} conta(s) importada(s) com sucesso!")
            except Exception as e:
                st.error(f"Erro ao importar: {str(e)}")
    
    # Editor do Plano de Contas
    df_contas = pd.DataFrame(st.session_state.plano_contas)
    # Garante que as colunas existem
    colunas = ["nome", "tipo", "natureza", "comportamento"]
    for col in colunas:
        if col not in df_contas.columns:
            df_contas[col] = "---"
    df_contas = df_contas[colunas]
    
    edited_df = st.data_editor(
        df_contas,
        column_config={
            "nome": st.column_config.TextColumn("Nome da Conta", width="large"),
            "tipo": st.column_config.SelectboxColumn(
                "Tipo de Gasto",
                options=["receita", "custo_direto", "custo_indireto", "despesa", "investimento", "perda"],
                width="medium"
            ),
            "natureza": st.column_config.SelectboxColumn(
                "Natureza (Custos)",
                options=["---", "direto", "indireto"],
                width="medium"
            ),
            "comportamento": st.column_config.SelectboxColumn(
                "Comportamento",
                options=["---", "fixo", "variavel", "semivariavel"],
                width="medium"
            ),
        },
        use_container_width=True,
        num_rows="dynamic",
        key="plano_contas_editor"
    )
    
    # Atualiza o estado com as edições
    if not edited_df.equals(df_contas):
        novas_contas = []
        for idx, row in edited_df.iterrows():
            original = st.session_state.plano_contas[idx] if idx < len(st.session_state.plano_contas) else None
            novas_contas.append({
                "id": original["id"] if original else idx + 1000,
                "nome": row["nome"],
                "tipo": row["tipo"],
                "natureza": row["natureza"],
                "comportamento": row["comportamento"],
            })
        st.session_state.plano_contas = novas_contas
    
    # Adicionar nova conta
    with st.expander("➕ Adicionar Nova Conta"):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            novo_nome = st.text_input("Nome da Conta", placeholder="Ex: Seguros da Fábrica")
        with col2:
            novo_tipo = st.selectbox("Tipo de Gasto", 
                ["receita", "custo_direto", "custo_indireto", "despesa", "investimento", "perda"])
        with col3:
            nova_natureza = st.selectbox("Natureza", ["---", "direto", "indireto"])
        
        col4, col5 = st.columns([1, 4])
        with col4:
            novo_comportamento = st.selectbox("Comportamento", ["---", "fixo", "variavel", "semivariavel"])
        
        if st.button("Adicionar Conta", use_container_width=True):
            if novo_nome:
                st.session_state.plano_contas.append({
                    "id": len(st.session_state.plano_contas) + 1000,
                    "nome": novo_nome,
                    "tipo": novo_tipo,
                    "natureza": nova_natureza,
                    "comportamento": novo_comportamento,
                })
                st.rerun()
            else:
                st.warning("Preencha pelo menos o nome da conta.")

def modulo_rateio():
    """Módulo: Critérios de Rateio - APENAS PARA CONTAS INDIRETAS"""
    st.header("⚖️ Critérios de Rateio")
    
    render_alert("""
    O rateio é utilizado para distribuir <strong>custos indiretos</strong> entre os produtos.
    Apenas contas classificadas como <strong>Custo Indireto</strong> são rateadas.
    """)
    
    # Indicadores gerais
    indicadores = calcular_indicadores(st.session_state)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi("Receita Total", fmtR(indicadores["rb"]), color="#3fb950")
    with col2:
        render_kpi("Custo Total", fmtR(indicadores["cpv_direto"]), color="#e3b341")
    with col3:
        render_kpi("Qtd Total Vendida", fmt(indicadores["qtd_total"], 0), color="#58a6ff")
    with col4:
        render_kpi("Nº Produtos", len(st.session_state.produtos), color="#bc8cff")
    
    # Gerenciar critérios
    with st.expander("⚙️ Gerenciar Critérios de Rateio"):
        st.write("**Critérios disponíveis:**")
        
        for c in st.session_state.criterios_rateio:
            tipo = "Sistema" if c.get("tipo") == "sistema" else "Personalizado"
            cor = "#58a6ff" if c.get("tipo") == "sistema" else "#bc8cff"
            
            if c.get("tipo") == "usuario":
                col1, col2 = st.columns([3, 1])
                with col1:
                    render_tag(f"{c['nome']} ({tipo})", color=cor)
                with col2:
                    if st.button(f"✕ Remover", key=f"remove_{c['id']}"):
                        st.session_state.criterios_rateio = [
                            crit for crit in st.session_state.criterios_rateio 
                            if crit["id"] != c["id"]
                        ]
                        st.rerun()
            else:
                render_tag(f"{c['nome']} ({tipo})", color=cor)
        
        st.divider()
        
        if st.button("➕ Criar critério próprio"):
            st.session_state.show_criar_criterio = True
        
        if st.session_state.get("show_criar_criterio", False):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                novo_nome = st.text_input("Nome do critério", placeholder="Ex: Horas-Máquina")
            with col2:
                nova_base = st.selectbox("Base de cálculo", ["receita", "custo", "qtd", "igual", "manual"])
            with col3:
                if st.button("Criar"):
                    if novo_nome:
                        st.session_state.criterios_rateio.append({
                            "id": f"custom_{len(st.session_state.criterios_rateio) + 1000}",
                            "nome": novo_nome,
                            "tipo": "usuario",
                            "base": nova_base
                        })
                        st.session_state.show_criar_criterio = False
                        st.rerun()
                    else:
                        st.warning("Digite um nome para o critério.")
            
            if st.button("Cancelar"):
                st.session_state.show_criar_criterio = False
                st.rerun()
    
    # Lista de CUSTOS INDIRETOS (rateio)
    st.subheader("📊 Distribuição de Custos Indiretos")
    
    despesas_rateio = [
        d for d in st.session_state.despesas
        if any(c["id"] == d["conta_id"] and c["tipo"] == "custo_indireto" for c in st.session_state.plano_contas)
    ]
    
    if not despesas_rateio:
        st.info("Nenhum custo indireto cadastrado para rateio.")
        return
    
    for despesa in despesas_rateio:
        conta = next((c for c in st.session_state.plano_contas if c["id"] == despesa["conta_id"]), None)
        if not conta:
            continue
        
        with st.expander(f"📌 {conta['nome']} - {fmtR(despesa['valor'])}", expanded=True):
            # Mostrar classificação
            col1, col2 = st.columns(2)
            with col1:
                render_tag(f"Tipo: {conta['tipo']}", color="#f85149" if conta['tipo'] == 'custo_indireto' else "#58a6ff")
            with col2:
                render_tag(f"Comportamento: {conta['comportamento']}", color="#e3b341")
            
            # Selecionar critério
            col1, col2 = st.columns([3, 1])
            with col1:
                novo_criterio = st.selectbox(
                    "Critério de rateio",
                    options=[c["id"] for c in st.session_state.criterios_rateio],
                    format_func=lambda x: next(c["nome"] for c in st.session_state.criterios_rateio if c["id"] == x),
                    index=next((i for i, c in enumerate(st.session_state.criterios_rateio) if c["id"] == despesa["rateio"]), 0),
                    key=f"rateio_{despesa['conta_id']}"
                )
                if novo_criterio != despesa["rateio"]:
                    for d in st.session_state.despesas:
                        if d["conta_id"] == despesa["conta_id"]:
                            d["rateio"] = novo_criterio
                            break
                    st.rerun()
            
            # Se for manual, mostrar pesos
            criterio_obj = next((c for c in st.session_state.criterios_rateio if c["id"] == novo_criterio), None)
            if criterio_obj and criterio_obj["base"] == "manual":
                st.write("**Pesos por produto:**")
                pesos = st.session_state.pesos_rateio.get(novo_criterio, {})
                cols = st.columns(len(st.session_state.produtos))
                for i, produto in enumerate(st.session_state.produtos):
                    with cols[i]:
                        peso = st.number_input(
                            produto["nome"],
                            value=float(pesos.get(produto["id"], 0)),
                            step=0.1,
                            key=f"peso_{novo_criterio}_{produto['id']}"
                        )
                        if peso != pesos.get(produto["id"], 0):
                            if novo_criterio not in st.session_state.pesos_rateio:
                                st.session_state.pesos_rateio[novo_criterio] = {}
                            st.session_state.pesos_rateio[novo_criterio][produto["id"]] = peso
                            st.rerun()
            
            # Mostrar distribuição
            rateio = calcular_rateio(st.session_state, despesa["conta_id"], novo_criterio)
            
            if rateio:
                df_rateio = pd.DataFrame(rateio)
                df_rateio["% Rateio"] = df_rateio["perc"].apply(lambda x: f"{fmt(x)}%")
                df_rateio["Valor Rateado"] = df_rateio["valor"].apply(fmtR)
                st.dataframe(
                    df_rateio[["produto", "% Rateio", "Valor Rateado"]],
                    use_container_width=True,
                    hide_index=True
                )

def modulo_vendas():
    """Módulo: Vendas"""
    st.header("🛒 Volume de Vendas")
    
    render_alert("""
    Informe quantidade, preço unitário, custo unitário e percentual de impostos para cada produto.
    As comissões sobre vendas são calculadas automaticamente.
    """)
    
    # Comissão
    col1, col2 = st.columns([1, 4])
    with col1:
        comissao = st.number_input(
            "Comissão %",
            value=float(st.session_state.comissao_perc),
            step=0.5,
            min_value=0.0,
            max_value=100.0
        )
        st.session_state.comissao_perc = comissao
    
    # Importar planilha
    with st.expander("📥 Importar Vendas (XLSX/CSV)"):
        uploaded_file = st.file_uploader(
            "Arraste ou selecione uma planilha",
            type=["xlsx", "xls", "csv"],
            key="vendas_upload"
        )
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(('.xlsx', '.xls')) else pd.read_csv(uploaded_file)
                
                col_produto = next((c for c in df.columns if 'produto' in c.lower() or 'nome' in c.lower()), None)
                if col_produto is None:
                    st.error("Coluna 'Produto' não encontrada.")
                else:
                    col_qtd = next((c for c in df.columns if 'qtd' in c.lower() or 'quant' in c.lower()), None)
                    col_preco = next((c for c in df.columns if 'preco' in c.lower() or 'valor' in c.lower()), None)
                    col_custo = next((c for c in df.columns if 'custo' in c.lower()), None)
                    col_imp = next((c for c in df.columns if 'impost' in c.lower() or 'tribut' in c.lower()), None)
                    
                    for _, row in df.iterrows():
                        if pd.isna(row[col_produto]):
                            continue
                        produto_id = len(st.session_state.produtos) + 1000
                        st.session_state.produtos.append({
                            "id": produto_id,
                            "nome": str(row[col_produto]),
                            "unidade": "un"
                        })
                        st.session_state.vendas.append({
                            "produto_id": produto_id,
                            "qtd": float(row[col_qtd]) if col_qtd and not pd.isna(row[col_qtd]) else 0,
                            "preco_unit": float(row[col_preco]) if col_preco and not pd.isna(row[col_preco]) else 0,
                            "custo_unit": float(row[col_custo]) if col_custo and not pd.isna(row[col_custo]) else 0,
                            "custo_direto": 0,
                            "impostos": float(row[col_imp]) if col_imp and not pd.isna(row[col_imp]) else 0,
                        })
                    st.success("✅ Produtos importados com sucesso!")
                    st.rerun()
            except Exception as e:
                st.error(f"Erro ao importar: {str(e)}")
    
    # Editor de vendas
    df_vendas = pd.DataFrame([
        {
            "Produto": next((p["nome"] for p in st.session_state.produtos if p["id"] == v["produto_id"]), f"ID {v['produto_id']}"),
            "Qtd": v["qtd"],
            "Preço Unit.": v["preco_unit"],
            "Custo Unit.": v["custo_unit"],
            "Impostos %": v["impostos"],
        }
        for v in st.session_state.vendas
    ])
    
    edited_df = st.data_editor(
        df_vendas,
        column_config={
            "Produto": st.column_config.TextColumn("Produto", disabled=True),
            "Qtd": st.column_config.NumberColumn("Quantidade", min_value=0, step=1),
            "Preço Unit.": st.column_config.NumberColumn("Preço Unitário", min_value=0, step=0.01, format="R$ %.2f"),
            "Custo Unit.": st.column_config.NumberColumn("Custo Unitário", min_value=0, step=0.01, format="R$ %.2f"),
            "Impostos %": st.column_config.NumberColumn("Impostos (%)", min_value=0, max_value=100, step=0.1),
        },
        use_container_width=True,
        num_rows="dynamic",
        key="vendas_editor"
    )
    
    # Atualiza o estado com as edições
    if not edited_df.equals(df_vendas):
        for idx, row in edited_df.iterrows():
            if idx < len(st.session_state.vendas):
                v = st.session_state.vendas[idx]
                v["qtd"] = float(row["Qtd"])
                v["preco_unit"] = float(row["Preço Unit."])
                v["custo_unit"] = float(row["Custo Unit."])
                v["impostos"] = float(row["Impostos %"])
        st.rerun()
    
    # Adicionar novo produto
    with st.expander("➕ Adicionar Produto"):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            novo_nome = st.text_input("Nome do produto", placeholder="Produto D")
        with col2:
            nova_unidade = st.selectbox("Unidade", ["un", "kg", "cx", "lt", "m", "m²", "par"])
        with col3:
            if st.button("Adicionar", use_container_width=True):
                if novo_nome:
                    produto_id = len(st.session_state.produtos) + 1000
                    st.session_state.produtos.append({
                        "id": produto_id,
                        "nome": novo_nome,
                        "unidade": nova_unidade
                    })
                    st.session_state.vendas.append({
                        "produto_id": produto_id,
                        "qtd": 0,
                        "preco_unit": 0,
                        "custo_unit": 0,
                        "custo_direto": 0,
                        "impostos": 0,
                    })
                    st.rerun()
    
    # KPIs de vendas
    indicadores = calcular_indicadores(st.session_state)
    
    st.subheader("📊 Resumo de Vendas")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi("Receita Bruta", fmtR(indicadores["rb"]), color="#3fb950")
    with col2:
        render_kpi("Impostos/Deduções", fmtR(indicadores["deducoes"]), color="#f85149")
    with col3:
        render_kpi("Receita Líquida", fmtR(indicadores["rl"]), color="#58a6ff")
    with col4:
        render_kpi("Lucro Bruto", fmtR(indicadores["lb_absorcao"]), 
                   sub=f"Margem: {fmtP(safe_div(indicadores['lb_absorcao'], indicadores['rl']) * 100)}",
                   color="#39d353")

def modulo_estoque():
    """Módulo: Estoque"""
    st.header("📦 Apuração do Estoque")
    
    render_alert("""
    Método: <strong>Custo Médio Ponderado</strong>. 
    CPV = Estoque Inicial + Compras/Produção − Estoque Final.
    """)
    
    # Tabela de estoque
    dados_estoque = []
    for i, produto in enumerate(st.session_state.produtos):
        ei = st.session_state.estoque_inicial[i] if i < len(st.session_state.estoque_inicial) else {"qtd": 0, "custo_medio": 0}
        ef = st.session_state.estoque_final[i] if i < len(st.session_state.estoque_final) else {"qtd": 0, "custo_medio": 0}
        prod = st.session_state.producao_mes[i] if i < len(st.session_state.producao_mes) else {"qtd": 0}
        venda = st.session_state.vendas[i] if i < len(st.session_state.vendas) else {"custo_unit": 0}
        
        dados_estoque.append({
            "Produto": produto["nome"],
            "EI Qtd": ei["qtd"],
            "EI Custo": ei["custo_medio"],
            "EI Valor": ei["qtd"] * ei["custo_medio"],
            "Produção Qtd": prod["qtd"],
            "EF Qtd": ef["qtd"],
            "EF Custo": ef["custo_medio"],
            "EF Valor": ef["qtd"] * ef["custo_medio"],
            "CPV": ei["qtd"] * ei["custo_medio"] + prod["qtd"] * venda["custo_unit"] - ef["qtd"] * ef["custo_medio"],
        })
    
    df_estoque = pd.DataFrame(dados_estoque)
    
    edited_df = st.data_editor(
        df_estoque,
        column_config={
            "Produto": st.column_config.TextColumn("Produto", disabled=True),
            "EI Qtd": st.column_config.NumberColumn("EI Qtd", min_value=0, step=1),
            "EI Custo": st.column_config.NumberColumn("EI Custo", min_value=0, step=0.01, format="R$ %.2f"),
            "EI Valor": st.column_config.NumberColumn("EI Valor", disabled=True, format="R$ %.2f"),
            "Produção Qtd": st.column_config.NumberColumn("Produção Qtd", min_value=0, step=1),
            "EF Qtd": st.column_config.NumberColumn("EF Qtd", min_value=0, step=1),
            "EF Custo": st.column_config.NumberColumn("EF Custo", min_value=0, step=0.01, format="R$ %.2f"),
            "EF Valor": st.column_config.NumberColumn("EF Valor", disabled=True, format="R$ %.2f"),
            "CPV": st.column_config.NumberColumn("CPV", disabled=True, format="R$ %.2f"),
        },
        use_container_width=True,
        key="estoque_editor"
    )
    
    # Atualiza o estado
    if not edited_df.equals(df_estoque):
        for idx, row in edited_df.iterrows():
            if idx < len(st.session_state.produtos):
                if idx < len(st.session_state.estoque_inicial):
                    st.session_state.estoque_inicial[idx]["qtd"] = float(row["EI Qtd"])
                    st.session_state.estoque_inicial[idx]["custo_medio"] = float(row["EI Custo"])
                if idx < len(st.session_state.estoque_final):
                    st.session_state.estoque_final[idx]["qtd"] = float(row["EF Qtd"])
                    st.session_state.estoque_final[idx]["custo_medio"] = float(row["EF Custo"])
                if idx < len(st.session_state.producao_mes):
                    st.session_state.producao_mes[idx]["qtd"] = float(row["Produção Qtd"])
        st.rerun()
    
    # Totais
    col1, col2, col3 = st.columns(3)
    with col1:
        total_ei = sum(d["EI Valor"] for d in dados_estoque)
        render_kpi("Total Estoque Inicial", fmtR(total_ei), color="#58a6ff")
    with col2:
        total_ef = sum(d["EF Valor"] for d in dados_estoque)
        render_kpi("Total Estoque Final", fmtR(total_ef), color="#39d353")
    with col3:
        total_cpv = sum(d["CPV"] for d in dados_estoque)
        render_kpi("CPV Total", fmtR(total_cpv), color="#e3b341")

def modulo_dre():
    """Módulo: DRE - Absorção e Variável"""
    st.header("📊 Demonstração do Resultado")
    
    indicadores = calcular_indicadores(st.session_state)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Custeio por Absorção")
        render_alert("""
        Todos os custos de produção (diretos + indiretos) são alocados ao produto.
        Exigido pela legislação (CPC/IFRS).
        """, type="warn")
        
        # DRE Absorção
        dre_abs = [
            ("Receita Bruta de Vendas", indicadores["rb"], "#3fb950", True),
            ("(−) Deduções e Impostos s/ Vendas", -indicadores["deducoes"], "#f85149", False),
            ("(−) Comissões s/ Vendas", -indicadores["comissoes"], "#f85149", False),
            ("  Custos Diretos", -indicadores["cpv_direto"], "#e6edf3", False),
            ("  Custos Indiretos Rateados", -indicadores["custos_indiretos"], "#e6edf3", False),
            ("= Lucro Bruto", indicadores["lb_absorcao"], "#39d353" if indicadores["lb_absorcao"] >= 0 else "#f85149", True),
            ("(−) Despesas Operacionais", -indicadores["despesas_operacionais"], "#f85149", False),
            ("= Resultado Operacional (EBIT)", indicadores["lo_absorcao"], "#3fb950" if indicadores["lo_absorcao"] >= 0 else "#f85149", True),
            ("(−) IR/CSLL (34%)", -indicadores["ircsll_abs"], "#f85149", False),
            ("= Lucro Líquido", indicadores["ll_absorcao"], "#3fb950" if indicadores["ll_absorcao"] >= 0 else "#f85149", True),
        ]
        
        for label, value, color, bold in dre_abs:
            prefix = ""
            if value < 0:
                prefix = "−"
                value = abs(value)
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; padding: 4px 0; 
                            font-family: 'IBM Plex Mono', monospace; 
                            font-weight: {'700' if bold else '400'};
                            color: {color};">
                    <span>{label}</span>
                    <span>{prefix}{fmtR(value)}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        col1a, col1b = st.columns(2)
        with col1a:
            render_kpi("Margem Bruta", fmtP(safe_div(indicadores["lb_absorcao"], indicadores["rl"]) * 100),
                       color="#39d353" if indicadores["lb_absorcao"] >= 0 else "#f85149")
        with col1b:
            render_kpi("Margem Líquida", fmtP(safe_div(indicadores["ll_absorcao"], indicadores["rl"]) * 100),
                       color="#3fb950" if indicadores["ll_absorcao"] >= 0 else "#f85149")
    
    with col2:
        st.subheader("📋 Custeio Variável (Gerencial)")
        render_alert("""
        Separa custos fixos dos variáveis. Evidencia a <strong>Margem de Contribuição</strong>.
        Ideal para decisões gerenciais.
        """, type="info")
        
        # DRE Variável
        dre_var = [
            ("Receita Bruta de Vendas", indicadores["rb"], "#3fb950", True),
            ("(−) Deduções e Impostos s/ Vendas", -indicadores["deducoes"], "#f85149", False),
            ("(−) Comissões s/ Vendas", -indicadores["comissoes"], "#f85149", False),
            ("= Receita Líquida", indicadores["rl"], "#58a6ff", True),
            ("(−) Custos e Despesas Variáveis", -indicadores["custos_var"], "#e3b341", False),
            ("  CPV Direto", -indicadores["cpv_direto"], "#e6edf3", False),
            ("= Margem de Contribuição (MC)", indicadores["mc"], "#39d353" if indicadores["mc"] >= 0 else "#f85149", True),
            ("  MC %", indicadores["mc_perc"], "#8d96a0", False),
            ("(−) Custos Fixos (Indiretos + Desp. Fixas)", -indicadores["custos_fixos"], "#f85149", True),
            ("= Resultado Operacional", indicadores["lo_variavel"], "#3fb950" if indicadores["lo_variavel"] >= 0 else "#f85149", True),
            ("(−) IR/CSLL (34%)", -indicadores["ircsll_var"], "#f85149", False),
            ("= Lucro Líquido", indicadores["ll_variavel"], "#3fb950" if indicadores["ll_variavel"] >= 0 else "#f85149", True),
        ]
        
        for label, value, color, bold in dre_var:
            prefix = ""
            if value < 0:
                prefix = "−"
                value = abs(value)
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; padding: 4px 0; 
                            font-family: 'IBM Plex Mono', monospace; 
                            font-weight: {'700' if bold else '400'};
                            color: {color};">
                    <span>{label}</span>
                    <span>{prefix}{fmtR(value)}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        col2a, col2b = st.columns(2)
        with col2a:
            render_kpi("Margem de Contribuição", fmtP(indicadores["mc_perc"]), color="#39d353")
        with col2b:
            render_kpi("Margem Líquida", fmtP(safe_div(indicadores["ll_variavel"], indicadores["rl"]) * 100),
                       color="#3fb950" if indicadores["ll_variavel"] >= 0 else "#f85149")
    
    # Comparativo
    st.subheader("📊 Comparativo Absorção vs Variável")
    comparativo = pd.DataFrame([
        {"Indicador": "Receita Líquida", "Absorção": fmtR(indicadores["rl"]), "Variável": fmtR(indicadores["rl"]), "Diferença": fmtR(0)},
        {"Indicador": "Resultado Bruto / MC", "Absorção": fmtR(indicadores["lb_absorcao"]), "Variável": fmtR(indicadores["mc"]), "Diferença": fmtR(indicadores["lb_absorcao"] - indicadores["mc"])},
        {"Indicador": "Resultado Operacional", "Absorção": fmtR(indicadores["lo_absorcao"]), "Variável": fmtR(indicadores["lo_variavel"]), "Diferença": fmtR(indicadores["lo_absorcao"] - indicadores["lo_variavel"])},
        {"Indicador": "Lucro Líquido", "Absorção": fmtR(indicadores["ll_absorcao"]), "Variável": fmtR(indicadores["ll_variavel"]), "Diferença": fmtR(indicadores["ll_absorcao"] - indicadores["ll_variavel"])},
    ])
    st.dataframe(comparativo, use_container_width=True, hide_index=True)
    
    st.markdown(f"""
    <div style="font-size: 12px; color: #8d96a0; margin-top: 10px;">
    💡 A diferença entre os métodos equivale aos custos indiretos rateados 
    (<strong style="color: #e3b341;">{fmtR(indicadores['custos_indiretos'])}</strong>). 
    No Absorção, esse valor vai para o CPV; no Variável, vai direto para os custos fixos do período.
    </div>
    """, unsafe_allow_html=True)

def modulo_cvl():
    """Módulo: CVL - Custo-Volume-Lucro"""
    st.header("📐 Análise CVL - Custo, Volume e Lucro")
    
    indicadores = calcular_indicadores(st.session_state)
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi("Receita Líquida", fmtR(indicadores["rl"]), color="#58a6ff")
    with col2:
        render_kpi("Custos/Desp. Variáveis", fmtR(indicadores["custos_var"]), color="#e3b341")
    with col3:
        render_kpi("Margem de Contribuição", fmtR(indicadores["mc"]), 
                   sub=f"%MC = {fmtP(indicadores['mc_perc'])}",
                   color="#39d353")
    with col4:
        render_kpi("Custos Fixos", fmtR(indicadores["custos_fixos"]), color="#f85149")
    
    if indicadores["depreciacao"] > 0:
        render_alert(f"💡 Identificamos <strong>{fmtR(indicadores['depreciacao'])}</strong> em depreciação nos custos fixos — esse valor é excluído no cálculo do PE Financeiro.", type="info")
    
    # Simulação
    with st.expander("🎯 Simulação - 'O que acontece se...'", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Variação de Volume**")
            volume_var = st.slider(
                "Variação % no volume de vendas",
                min_value=-50,
                max_value=100,
                value=0,
                step=5,
                key="volume_sim"
            )
        with col2:
            st.write("**Variação de Preço**")
            preco_var = st.slider(
                "Variação % no preço de venda",
                min_value=-30,
                max_value=50,
                value=0,
                step=5,
                key="preco_sim"
            )
        
        if st.button("Aplicar Simulação"):
            for v in st.session_state.vendas:
                v["qtd"] = max(0, v["qtd"] * (1 + volume_var / 100))
                v["preco_unit"] = max(0, v["preco_unit"] * (1 + preco_var / 100))
            st.rerun()
        
        if st.button("Restaurar Dados Originais"):
            estado_inicial = get_initial_state()
            for key in ["vendas"]:
                st.session_state[key] = estado_inicial[key]
            st.rerun()
    
    # Pontos de Equilíbrio
    st.subheader("📊 Pontos de Equilíbrio")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="custom-card">
            <div class="custom-card-title"><span style="width:3px;height:14px;background:#58a6ff;border-radius:2px;display:block;"></span>PE Contábil (PEC)</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:28px;font-weight:700;color:#58a6ff;">{fmtR(indicadores['pec'])}</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#8d96a0;margin-top:4px;">Custos Fixos ÷ %MC</div>
            <div style="font-size:12px;color:#8d96a0;margin-top:8px;">Cobre todos os custos. LL = 0</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="custom-card">
            <div class="custom-card-title"><span style="width:3px;height:14px;background:#39d353;border-radius:2px;display:block;"></span>PE Financeiro (PEF)</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:28px;font-weight:700;color:#39d353;">{fmtR(indicadores['pef'])}</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#8d96a0;margin-top:4px;">(Custos Fixos − Depreciação) ÷ %MC</div>
            <div style="font-size:12px;color:#8d96a0;margin-top:8px;">Exclui despesas não-desembolsáveis</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="custom-card">
            <div class="custom-card-title"><span style="width:3px;height:14px;background:#bc8cff;border-radius:2px;display:block;"></span>PE Econômico (PEE)</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:28px;font-weight:700;color:#bc8cff;">{fmtR(indicadores['pee'])}</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#8d96a0;margin-top:4px;">(Custos Fixos + Lucro Mín.) ÷ %MC</div>
            <div style="font-size:12px;color:#8d96a0;margin-top:8px;">Inclui remuneração do capital</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Margem de Segurança
    st.subheader("🛡️ Margem de Segurança")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi("Margem de Segurança R$", fmtR(indicadores["ms_abs"]),
                   sub="Acima do PE" if indicadores["ms_abs"] >= 0 else "ABAIXO do PE — prejuízo!",
                   color="#3fb950" if indicadores["ms_abs"] >= 0 else "#f85149")
    with col2:
        render_kpi("Margem de Segurança %", fmtP(indicadores["ms_perc"]),
                   color="#3fb950" if indicadores["ms_perc"] >= 0 else "#f85149")
    with col3:
        render_kpi("Margem de Segurança Qtd", f"{fmt(indicadores['ms_qtd'], 0)} un",
                   sub="Unidades acima do PE",
                   color="#39d353" if indicadores["ms_perc"] >= 0 else "#f85149")
    
    # Gráfico do PE
    st.subheader("📈 Visualização do Ponto de Equilíbrio")
    
    volumes = np.linspace(0, max(indicadores["qtd_total"] * 2, 1000), 100)
    receita_sim = [v * (indicadores["rl"] / indicadores["qtd_total"]) for v in volumes] if indicadores["qtd_total"] > 0 else [0] * 100
    custo_total = [v * (indicadores["cpv_direto"] / indicadores["qtd_total"]) + indicadores["custos_fixos"] for v in volumes] if indicadores["qtd_total"] > 0 else [0] * 100
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=volumes, y=receita_sim, name="Receita Total", line=dict(color="#3fb950")))
    fig.add_trace(go.Scatter(x=volumes, y=custo_total, name="Custo Total", line=dict(color="#f85149")))
    
    pe_qtd = safe_div(indicadores["pec"], indicadores["rl"] / indicadores["qtd_total"]) if indicadores["qtd_total"] > 0 else 0
    fig.add_vline(x=pe_qtd, line_dash="dash", line_color="#58a6ff")
    fig.add_annotation(x=pe_qtd, y=max(receita_sim) * 0.8, text=f"PE: {fmt(pe_qtd, 0)} un", showarrow=True, arrowhead=1)
    
    fig.update_layout(
        title="Análise Custo-Volume-Lucro",
        xaxis_title="Quantidade Vendida (un)",
        yaxis_title="Valor (R$)",
        plot_bgcolor="#161b22",
        paper_bgcolor="#161b22",
        font_color="#e6edf3",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def modulo_precificacao():
    """Módulo: Precificação"""
    st.header("🏷️ Precificação")
    
    st.subheader("💰 Mark-up")
    render_alert("""
    <strong>Mark-up divisor:</strong> Preço = Custo ÷ (1 − %Deduções − %Lucro). 
    Garante cobertura de todos os custos + margem desejada.
    """)
    
    dados_markup = []
    for v in st.session_state.vendas:
        produto = next((p for p in st.session_state.produtos if p["id"] == v["produto_id"]), None)
        if not produto:
            continue
        
        lucro = st.session_state.markup_perc.get(v["produto_id"], 30)
        imposto = v["impostos"]
        divisor = 1 - imposto / 100 - lucro / 100
        preco_markup = v["custo_unit"] / divisor if divisor > 0 else 0
        mult = preco_markup / v["custo_unit"] if v["custo_unit"] > 0 else 0
        
        dados_markup.append({
            "Produto": produto["nome"],
            "Custo Unit.": fmtR(v["custo_unit"]),
            "Impostos %": fmtP(imposto),
            "Lucro Desejado %": f"{lucro}%",
            "Preço Mark-up": fmtR(preco_markup),
            "Mark-up Divisor": fmt(divisor, 4),
            "Mark-up Mult.": f"{fmt(mult, 2)}×",
        })
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.dataframe(pd.DataFrame(dados_markup), use_container_width=True, hide_index=True)
    with col2:
        st.write("**Ajustar Lucro Desejado**")
        for v in st.session_state.vendas:
            produto = next((p for p in st.session_state.produtos if p["id"] == v["produto_id"]), None)
            if produto:
                novo_lucro = st.number_input(
                    produto["nome"],
                    value=float(st.session_state.markup_perc.get(v["produto_id"], 30)),
                    min_value=0.0,
                    max_value=100.0,
                    step=1.0,
                    key=f"lucro_{v['produto_id']}"
                )
                st.session_state.markup_perc[v["produto_id"]] = novo_lucro
    
    st.subheader("🏪 Precificação a Mercado")
    render_alert("""
    Informe o preço praticado no mercado. O sistema calcula a margem real obtida 
    para análise de posicionamento competitivo.
    """)
    
    dados_mercado = []
    for v in st.session_state.vendas:
        produto = next((p for p in st.session_state.produtos if p["id"] == v["produto_id"]), None)
        if not produto:
            continue
        
        pm = st.session_state.preco_mercado.get(v["produto_id"], v["preco_unit"])
        mu = pm / v["custo_unit"] if v["custo_unit"] > 0 else 0
        mg_preco = (pm - v["custo_unit"]) / pm * 100 if pm > 0 else 0
        mg_custo = (pm - v["custo_unit"]) / v["custo_unit"] * 100 if v["custo_unit"] > 0 else 0
        
        dados_mercado.append({
            "Produto": produto["nome"],
            "Custo Unit.": fmtR(v["custo_unit"]),
            "Preço Mercado": fmtR(pm),
            "Markup Real": f"{fmt(mu, 2)}×",
            "Margem s/ Preço": fmtP(mg_preco),
            "Margem s/ Custo": fmtP(mg_custo),
        })
    
    df_mercado = pd.DataFrame(dados_mercado)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.dataframe(df_mercado, use_container_width=True, hide_index=True)
    with col2:
        st.write("**Ajustar Preço de Mercado**")
        for v in st.session_state.vendas:
            produto = next((p for p in st.session_state.produtos if p["id"] == v["produto_id"]), None)
            if produto:
                novo_preco = st.number_input(
                    produto["nome"],
                    value=float(st.session_state.preco_mercado.get(v["produto_id"], v["preco_unit"])),
                    min_value=0.0,
                    step=0.5,
                    key=f"pm_{v['produto_id']}"
                )
                st.session_state.preco_mercado[v["produto_id"]] = novo_preco
    
    st.subheader("📊 Comparativo de Preços")
    
    dados_comparativo = []
    for v in st.session_state.vendas:
        produto = next((p for p in st.session_state.produtos if p["id"] == v["produto_id"]), None)
        if not produto:
            continue
        
        lucro = st.session_state.markup_perc.get(v["produto_id"], 30)
        divisor = 1 - v["impostos"] / 100 - lucro / 100
        preco_mu = v["custo_unit"] / divisor if divisor > 0 else 0
        pm = st.session_state.preco_mercado.get(v["produto_id"], v["preco_unit"])
        preco_atual = v["preco_unit"]
        
        if preco_atual >= pm:
            posicao = "Premium"
            pos_color = "#bc8cff"
            rec = "Justifique o diferencial"
        elif preco_atual >= preco_mu:
            posicao = "Adequado"
            pos_color = "#3fb950"
            rec = "Preço equilibrado"
        else:
            posicao = "Abaixo do MU"
            pos_color = "#f85149"
            rec = "Risco de margem insuficiente"
        
        dados_comparativo.append({
            "Produto": produto["nome"],
            "Preço Atual": fmtR(preco_atual),
            "Preço Mark-up": fmtR(preco_mu),
            "Preço Mercado": fmtR(pm),
            "Posição": posicao,
            "Recomendação": rec,
        })
    
    st.dataframe(pd.DataFrame(dados_comparativo), use_container_width=True, hide_index=True)

def modulo_relatorio():
    """Módulo: Relatório/Dashboard"""
    st.header("📈 Relatório Consolidado")
    
    indicadores = calcular_indicadores(st.session_state)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi("Receita Líquida", fmtR(indicadores["rl"]), 
                   sub=f"Bruta: {fmtR(indicadores['rb'])}",
                   color="#58a6ff")
    with col2:
        render_kpi("Margem de Contribuição", fmtP(indicadores["mc_perc"]),
                   sub=fmtR(indicadores["mc"]),
                   color="#39d353")
    with col3:
        render_kpi("Lucro Líquido", fmtR(indicadores["ll_absorcao"]),
                   sub=f"Margem: {fmtP(safe_div(indicadores['ll_absorcao'], indicadores['rl']) * 100)}",
                   color="#3fb950" if indicadores["ll_absorcao"] >= 0 else "#f85149")
    with col4:
        render_kpi("Margem de Segurança", fmtP(indicadores["ms_perc"]),
                   sub=f"PE: {fmtR(indicadores['pec'])}",
                   color="#3fb950" if indicadores["ms_perc"] >= 0 else "#f85149")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Composição da Receita por Produto")
        
        dados_receita = []
        for v in st.session_state.vendas:
            produto = next((p for p in st.session_state.produtos if p["id"] == v["produto_id"]), None)
            if produto:
                rec = num(v["qtd"]) * num(v["preco_unit"])
                dados_receita.append({
                    "Produto": produto["nome"],
                    "Receita": rec,
                    "%": rec / indicadores["rb"] * 100 if indicadores["rb"] > 0 else 0
                })
        
        df_receita = pd.DataFrame(dados_receita)
        fig = px.bar(df_receita, x="Produto", y="Receita", title="Receita por Produto",
                     text=df_receita["%"].apply(lambda x: f"{fmt(x)}%"),
                     color_discrete_sequence=["#58a6ff"])
        fig.update_layout(
            plot_bgcolor="#161b22",
            paper_bgcolor="#161b22",
            font_color="#e6edf3",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Composição de Custos")
        
        dados_custos = [
            {"Categoria": "CPV Direto", "Valor": indicadores["cpv_direto"], "Color": "#e3b341"},
            {"Categoria": "Custos Indiretos", "Valor": indicadores["custos_indiretos"], "Color": "#d29922"},
            {"Categoria": "Despesas Operacionais", "Valor": indicadores["despesas_operacionais"], "Color": "#f85149"},
            {"Categoria": "Comissões", "Valor": indicadores["comissoes"], "Color": "#bc8cff"},
            {"Categoria": "Impostos/Deduções", "Valor": indicadores["deducoes"], "Color": "#6e1c1a"},
        ]
        df_custos = pd.DataFrame(dados_custos)
        fig = px.pie(df_custos, values="Valor", names="Categoria", title="Composição de Custos",
                     color="Categoria", color_discrete_map={d["Categoria"]: d["Color"] for d in dados_custos})
        fig.update_layout(
            plot_bgcolor="#161b22",
            paper_bgcolor="#161b22",
            font_color="#e6edf3"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🩺 Diagnóstico Executivo")
    
    diagnosticos = [
        (indicadores["ll_absorcao"] >= 0, f"✅ Operação lucrativa: {fmtR(indicadores['ll_absorcao'])}", f"❌ Resultado negativo: {fmtR(indicadores['ll_absorcao'])}"),
        (indicadores["mc_perc"] >= 30, f"✅ MC saudável: {fmtP(indicadores['mc_perc'])}", f"⚠️ MC abaixo de 30%: {fmtP(indicadores['mc_perc'])}"),
        (indicadores["ms_perc"] >= 15, f"✅ Margem de segurança adequada: {fmtP(indicadores['ms_perc'])}", f"⚠️ MS baixa: {fmtP(indicadores['ms_perc'])} — próximo ao PE"),
        (indicadores["rl"] > indicadores["pec"], f"✅ Receita acima do PE Contábil ({fmtR(indicadores['pec'])})", f"❌ Receita abaixo do PE — prejuízo operacional!"),
        (safe_div(indicadores["comissoes"], indicadores["rl"]) < 0.1, 
         f"✅ Comissões sob controle: {fmtP(safe_div(indicadores['comissoes'], indicadores['rl']) * 100)}",
         f"⚠️ Comissões elevadas: {fmtR(indicadores['comissoes'])}"),
    ]
    
    for ok, msg_ok, msg_bad in diagnosticos:
        if ok:
            st.markdown(f'<div style="background:#196c2e33;border:1px solid #196c2e;border-radius:6px;padding:8px 12px;margin-bottom:8px;font-size:13px;">{msg_ok}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:#6e1c1a33;border:1px solid #6e1c1a;border-radius:6px;padding:8px 12px;margin-bottom:8px;font-size:13px;">{msg_bad}</div>', unsafe_allow_html=True)

def modulo_laudo():
    """Módulo: Laudo"""
    st.header("📄 Laudo de Análise")
    
    indicadores = calcular_indicadores(st.session_state)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.nome_empresa = st.text_input("Nome da Empresa", value=st.session_state.nome_empresa)
    with col2:
        st.session_state.periodo = st.text_input("Período", value=st.session_state.periodo)
    with col3:
        st.session_state.regime = st.text_input("Regime Tributário", value=st.session_state.regime)
    
    st.subheader("📊 Indicadores Consolidados")
    
    indicadores_lista = [
        ("Receita Bruta", fmtR(indicadores["rb"]), "#3fb950"),
        ("Receita Líquida", fmtR(indicadores["rl"]), "#58a6ff"),
        ("CMV / CPV Total", fmtR(indicadores["cpv_direto"]), "#e3b341"),
        ("Margem de Contribuição", f"{fmtR(indicadores['mc'])} ({fmtP(indicadores['mc_perc'])})", "#39d353"),
        ("Custos Fixos", fmtR(indicadores["custos_fixos"]), "#f85149"),
        ("PE Contábil", fmtR(indicadores["pec"]), "#58a6ff"),
        ("Margem de Segurança", fmtP(indicadores["ms_perc"]), "#3fb950" if indicadores["ms_perc"] >= 0 else "#f85149"),
        ("Lucro Líquido (Absorção)", fmtR(indicadores["ll_absorcao"]), "#3fb950" if indicadores["ll_absorcao"] >= 0 else "#f85149"),
        ("Lucro Líquido (Variável)", fmtR(indicadores["ll_variavel"]), "#3fb950" if indicadores["ll_variavel"] >= 0 else "#f85149"),
    ]
    
    cols = st.columns(3)
    for i, (label, value, color) in enumerate(indicadores_lista):
        with cols[i % 3]:
            render_kpi(label, value, color=color)
    
    st.subheader("✍️ Conclusões e Análise")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.laudo["analista"] = st.text_input("Analista Responsável", value=st.session_state.laudo.get("analista", ""))
    with col2:
        st.session_state.laudo["data"] = st.date_input("Data do Laudo", value=datetime.now().date()).strftime("%d/%m/%Y")
    
    st.session_state.laudo["situacao_geral"] = st.text_area(
        "Situação Geral da Empresa",
        value=st.session_state.laudo.get("situacao_geral", ""),
        placeholder="Descreva o panorama geral: a empresa é lucrativa? Como está o fluxo de caixa?",
        height=100
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.laudo["pontos_fortes"] = st.text_area(
            "Pontos Fortes",
            value=st.session_state.laudo.get("pontos_fortes", ""),
            placeholder="Ex: boa margem de contribuição, portfólio diversificado...",
            height=100
        )
        st.session_state.laudo["recomendacoes"] = st.text_area(
            "Recomendações",
            value=st.session_state.laudo.get("recomendacoes", ""),
            placeholder="Ex: revisar a precificação do produto X, reduzir custo fixo...",
            height=100
        )
    with col2:
        st.session_state.laudo["pontos_fracos"] = st.text_area(
            "Pontos Fracos / Riscos",
            value=st.session_state.laudo.get("pontos_fracos", ""),
            placeholder="Ex: margem de segurança estreita, alta dependência de um produto...",
            height=100
        )
        st.session_state.laudo["observacoes"] = st.text_area(
            "Observações Adicionais",
            value=st.session_state.laudo.get("observacoes", ""),
            placeholder="Qualquer informação complementar relevante",
            height=100
        )
    
    if st.button("📄 Gerar Laudo Completo", use_container_width=True):
        render_alert("📄 Laudo gerado com sucesso! Use a função de impressão do navegador (Ctrl+P) para salvar como PDF.", type="success")
        
        laudo_html = criar_laudo_html(st.session_state, indicadores)
        b64 = base64.b64encode(laudo_html.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="laudo_{st.session_state.nome_empresa.replace(" ", "_")}.html" style="display:inline-block;background:#58a6ff;color:#fff;padding:10px 24px;border-radius:6px;text-decoration:none;font-weight:500;">⬇ Baixar Laudo (HTML)</a>'
        st.markdown(href, unsafe_allow_html=True)

def criar_laudo_html(state, indicadores):
    """Cria o HTML do laudo para exportação"""
    
    template_str = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Laudo - {{ nome_empresa }}</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: Arial, sans-serif; font-size: 13px; color: #1a1a1a; background: #fff; padding: 40px; max-width: 900px; margin: 0 auto; }
            h1 { font-size: 20px; color: #1F4E79; border-bottom: 3px solid #1F4E79; padding-bottom: 10px; margin-bottom: 6px; }
            h2 { font-size: 14px; color: #1F4E79; margin: 24px 0 10px; border-left: 4px solid #1F4E79; padding-left: 10px; }
            .subtitle { color: #666; font-size: 12px; margin-bottom: 24px; }
            .meta { display: flex; gap: 32px; margin-bottom: 20px; background: #f4f8fc; border-radius: 6px; padding: 14px 18px; flex-wrap: wrap; }
            .meta-item { display: flex; flex-direction: column; gap: 2px; }
            .meta-label { font-size: 10px; text-transform: uppercase; letter-spacing: .06em; color: #888; }
            .meta-value { font-size: 13px; font-weight: 700; color: #1F4E79; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 8px; }
            th { background: #EAF1F8; color: #1F4E79; font-size: 11px; text-transform: uppercase; letter-spacing: .05em; padding: 7px 12px; text-align: left; }
            td { padding: 6px 12px; border-bottom: 1px solid #eee; }
            .text-right { text-align: right; }
            .kpis { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 6px; }
            .kpi { border: 1px solid #dde3ec; border-radius: 6px; padding: 12px 14px; }
            .kpi-label { font-size: 10px; text-transform: uppercase; letter-spacing: .06em; color: #888; margin-bottom: 3px; }
            .kpi-value { font-size: 16px; font-weight: 700; }
            .section-box { border: 1px solid #dde3ec; border-radius: 6px; padding: 14px 16px; margin-bottom: 10px; white-space: pre-wrap; line-height: 1.7; color: #333; min-height: 40px; }
            .footer { margin-top: 36px; padding-top: 14px; border-top: 1px solid #dde3ec; display: flex; justify-content: space-between; color: #999; font-size: 11px; }
            .assinatura { margin-top: 50px; border-top: 1px solid #555; display: inline-block; padding-top: 6px; min-width: 220px; color: #555; font-size: 12px; text-align: center; }
            @media print { body { padding: 20px; } }
            .pos { color: #1a7a3a; } .neg { color: #c0392b; } .neu { color: #666; }
            .mono { font-family: 'Courier New', monospace; }
        </style>
    </head>
    <body>
        <h1>LAUDO DE ANÁLISE ECONÔMICO-FINANCEIRA</h1>
        <p class="subtitle">Sys_Cost — Sistema de Apuração de Resultados e Gestão de Custos</p>
        
        <div class="meta">
            <div class="meta-item"><span class="meta-label">Empresa</span><span class="meta-value">{{ nome_empresa }}</span></div>
            <div class="meta-item"><span class="meta-label">Período</span><span class="meta-value">{{ periodo }}</span></div>
            <div class="meta-item"><span class="meta-label">Regime Tributário</span><span class="meta-value">{{ regime }}</span></div>
            <div class="meta-item"><span class="meta-label">Analista</span><span class="meta-value">{{ laudo.analista or "—" }}</span></div>
            <div class="meta-item"><span class="meta-label">Data do Laudo</span><span class="meta-value">{{ laudo.data }}</span></div>
        </div>
        
        <h2>1. Indicadores Consolidados</h2>
        <table>
            <thead><tr><th>Indicador</th><th class="text-right">Valor</th></tr></thead>
            <tbody>
                {% for label, value in indicadores_lista %}
                <tr><td>{{ label }}</td><td class="text-right mono">{{ value }}</td></tr>
                {% endfor %}
            </tbody>
        </table>
        
        <h2>2. Rentabilidade por Produto</h2>
        <table>
            <thead><tr><th>Produto</th><th class="text-right">Qtd Vendida</th><th class="text-right">Receita</th><th class="text-right">CMV</th><th class="text-right">Margem Bruta</th></tr></thead>
            <tbody>
                {% for p in produtos %}
                <tr>
                    <td>{{ p.nome }}</td>
                    <td class="text-right mono">{{ p.qtd }}</td>
                    <td class="text-right mono">{{ p.receita }}</td>
                    <td class="text-right mono">{{ p.cmv }}</td>
                    <td class="text-right mono {{ 'pos' if p.margem >= 0 else 'neg' }}">{{ p.margem_pct }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <h2>3. Situação Geral da Empresa</h2>
        <div class="section-box">{{ laudo.situacao_geral or "(não preenchido)" }}</div>
        
        <h2>4. Pontos Fortes</h2>
        <div class="section-box">{{ laudo.pontos_fortes or "(não preenchido)" }}</div>
        
        <h2>5. Pontos Fracos / Riscos</h2>
        <div class="section-box">{{ laudo.pontos_fracos or "(não preenchido)" }}</div>
        
        <h2>6. Recomendações</h2>
        <div class="section-box">{{ laudo.recomendacoes or "(não preenchido)" }}</div>
        
        <h2>7. Observações Adicionais</h2>
        <div class="section-box">{{ laudo.observacoes or "(não preenchido)" }}</div>
        
        <div style="margin-top:40px;">
            <div class="assinatura">{{ laudo.analista or "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" }}<br/>Analista Responsável</div>
        </div>
        
        <div class="footer">
            <span>Sys_Cost</span>
            <span>Gerado em {{ data_atual }}</span>
        </div>
    </body>
    </html>
    """
    
    produtos_data = []
    for v in state["vendas"]:
        produto = next((p for p in state["produtos"] if p["id"] == v["produto_id"]), None)
        if produto:
            rec = num(v["qtd"]) * num(v["preco_unit"])
            cmv = num(v["qtd"]) * num(v["custo_unit"])
            margem = (rec - cmv) / rec * 100 if rec > 0 else 0
            produtos_data.append({
                "nome": produto["nome"],
                "qtd": fmt(v["qtd"], 0),
                "receita": fmtR(rec),
                "cmv": fmtR(cmv),
                "margem": margem,
                "margem_pct": fmtP(margem),
            })
    
    indicadores_lista = [
        ("Receita Bruta", fmtR(indicadores["rb"])),
        ("Receita Líquida", fmtR(indicadores["rl"])),
        ("CMV / CPV Total", fmtR(indicadores["cpv_direto"])),
        ("Margem de Contribuição", f"{fmtR(indicadores['mc'])} ({fmtP(indicadores['mc_perc'])})"),
        ("Custos Fixos", fmtR(indicadores["custos_fixos"])),
        ("PE Contábil", fmtR(indicadores["pec"])),
        ("Margem de Segurança", fmtP(indicadores["ms_perc"])),
        ("Lucro Líquido (Absorção)", fmtR(indicadores["ll_absorcao"])),
        ("Lucro Líquido (Variável)", fmtR(indicadores["ll_variavel"])),
    ]
    
    template = Template(template_str)
    html = template.render(
        nome_empresa=state["nome_empresa"],
        periodo=state["periodo"],
        regime=state["regime"],
        laudo=state["laudo"],
        indicadores_lista=indicadores_lista,
        produtos=produtos_data,
        data_atual=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )
    
    return html

def modulo_info():
    """Módulo: Informações"""
    st.header("ℹ️ Informações e Documentação")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Manual de Uso", "📥 Importar Planilha", "📚 Referências", "📝 Observações"])
    
    with tab1:
        st.markdown("""
        ### Manual de Uso do SysCost
        
        **1. Plano de Contas**
        Configure as contas da empresa com:
        - **Tipo de Gasto**: Receita, Custo Direto, Custo Indireto, Despesa, Investimento, Perda
        - **Natureza** (para custos): Direto ou Indireto
        - **Comportamento**: Fixo, Variável ou Semivariável
        
        **2. Critérios de Rateio**
        Apenas custos indiretos são rateados. Defina como cada custo indireto será distribuído.
        
        **3. Volume de Vendas**
        Informe quantidade, preço unitário, custo unitário e percentual de impostos.
        
        **4. Apuração do Estoque**
        Insira estoque inicial, produção/compra e estoque final.
        
        **5. DRE**
        Visualize a Demonstração do Resultado por Absorção e Variável.
        
        **6. CVL / Ponto de Equilíbrio**
        Calcule PE Contábil, Financeiro e Econômico.
        
        **7. Precificação**
        Compare Mark-up e Preço de Mercado.
        
        **8. Relatório**
        Dashboard consolidado com KPIs e diagnóstico.
        
        **9. Laudo**
        Gere um relatório executivo completo.
        """)
    
    with tab2:
        st.markdown("""
        ### Tutorial: Importar Planilha
        
        A planilha deve ter os cabeçalhos: **Nome**, **Tipo**, **Natureza**, **Comportamento**
        
        **Valores aceitos:**
        - Tipo: receita, custo_direto, custo_indireto, despesa, investimento, perda
        - Natureza: direto, indireto (apenas para custos)
        - Comportamento: fixo, variavel, semivariavel
        
        **Exemplo:**
        """)
        
        exemplo_df = pd.DataFrame([
            {"Nome": "Matéria-Prima", "Tipo": "custo_direto", "Natureza": "direto", "Comportamento": "variavel"},
            {"Nome": "Aluguel da Fábrica", "Tipo": "custo_indireto", "Natureza": "indireto", "Comportamento": "fixo"},
            {"Nome": "Salários Administrativos", "Tipo": "despesa", "Natureza": "---", "Comportamento": "fixo"},
        ])
        st.dataframe(exemplo_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("""
        ### Referências Técnicas
        
        **Contabilidade de Custos**
        MARTINS, Eliseu. Contabilidade de Custos. 11. ed. São Paulo: Atlas, 2018.
        
        **Custeio Variável e Absorção**
        HORNGREN, Charles T.; DATAR, Srikant M.; RAJAN, Madhav. Contabilidade de Custos. 14. ed. São Paulo: Pearson, 2016.
        
        **Análise CVL**
        GARRISON, Ray H.; NOREEN, Eric W.; BREWER, Peter C. Contabilidade Gerencial. 14. ed. Porto Alegre: AMGH, 2013.
        
        **Mark-up e Formação de Preços**
        ASSEF, Roberto. Guia Prático de Formação de Preços. 3. ed. Rio de Janeiro: Campus, 2005.
        """)
    
    with tab4:
        st.markdown("""
        ### Observações Importantes para o Curso
        
        **📚 Classificação de Gastos:**
        - **Custo**: Gastos com produção (diretos e indiretos)
        - **Despesa**: Gastos administrativos, comerciais e financeiros
        - **Investimento**: Gastos que geram benefícios futuros
        - **Perda**: Gastos anormais e involuntários
        
        **📊 Custeio por Absorção vs Variável:**
        - Absorção: Todos os custos vão para o produto
        - Variável: Apenas custos variáveis vão para o produto
        
        **📐 Ponto de Equilíbrio:**
        - Contábil: Cobre todos os custos (LL = 0)
        - Financeiro: Cobre apenas desembolsos
        - Econômico: Inclui lucro mínimo
        
        **💰 Mark-up:**
        Preço = Custo ÷ (1 − %Impostos − %Lucro)
        """)

# ─── FUNÇÃO PRINCIPAL ───────────────────────────────────────────────────────────

def main():
    """Função principal da aplicação"""
    
    if "initialized" not in st.session_state:
        estado_inicial = get_initial_state()
        for key, value in estado_inicial.items():
            st.session_state[key] = value
        st.session_state.initialized = True
        st.session_state.show_criar_criterio = False
    
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:16px 0;">
            <div style="font-family:'IBM Plex Mono',monospace;font-weight:700;font-size:18px;color:#e6edf3;">
                <span style="color:#3fb950;">Sys</span><span style="color:#8d96a0;"></span><span style="color:#58a6ff;">Cost</span>
            </div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#57606a;letter-spacing:0.08em;">
                GESTÃO DE CUSTOS
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        menu = {
            "📋 Plano de Contas": "plano",
            "⚖️ Rateio": "rateio",
            "🛒 Vendas": "vendas",
            "📦 Estoque": "estoque",
            "📊 DRE": "dre",
            "📐 CVL / PE": "cvl",
            "🏷️ Precificação": "precificacao",
            "📈 Relatório": "relatorio",
            "📄 Laudo": "laudo",
            "ℹ️ Info": "info",
        }
        
        for label, key in menu.items():
            if st.button(label, use_container_width=True, key=f"nav_{key}"):
                st.session_state.page = key
                st.rerun()
        
        st.divider()
        
        st.markdown("""
        <div style="font-size:12px;color:#8d96a0;padding:8px 0;">
            <div>🏢 <strong style="color:#e6edf3;">{}</strong></div>
            <div>📅 {}</div>
        </div>
        """.format(st.session_state.get("nome_empresa", "Empresa não definida"), 
                  st.session_state.get("periodo", "Período não definido")), 
        unsafe_allow_html=True)
        
        st.divider()
        
        if st.button("🔄 Restaurar Dados de Exemplo", use_container_width=True):
            estado_inicial = get_initial_state()
            for key, value in estado_inicial.items():
                st.session_state[key] = value
            st.session_state.initialized = True
            st.rerun()
        
        st.caption("SysCost")
    
    page = st.session_state.get("page", "plano")
    
    if page == "plano":
        modulo_plano_contas()
    elif page == "rateio":
        modulo_rateio()
    elif page == "vendas":
        modulo_vendas()
    elif page == "estoque":
        modulo_estoque()
    elif page == "dre":
        modulo_dre()
    elif page == "cvl":
        modulo_cvl()
    elif page == "precificacao":
        modulo_precificacao()
    elif page == "relatorio":
        modulo_relatorio()
    elif page == "laudo":
        modulo_laudo()
    elif page == "info":
        modulo_info()
    else:
        modulo_plano_contas()

if __name__ == "__main__":
    main()
