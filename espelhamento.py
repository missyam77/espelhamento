# --- START OF FILE valor_unidade_teste.py ---

import streamlit as st
import pandas as pd
import altair as alt
import locale

# Tenta configurar o locale para pt_BR (opcional, apenas para fins locais)
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR')
    except locale.Error:
        pass

# ============================
# CONFIGURAÇÃO DA PÁGINA
# ============================
st.set_page_config(
    page_title="SISAP - Análise Patrimonial",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================
# CSS Personalizado
# ============================
def load_custom_css():
    css = """
    <style>
    .custom-header {
        background-color: #002147; /* Azul UFF */
        padding: 15px;
        text-align: center;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .custom-header h1 {
        color: #ffffff;
        font-size: 26px;
        font-weight: bold;
    }
    .functionality-list {
        list-style: none;
        padding-left: 20px;
    }
    .functionality-list li:before {
        content: "🔹";
        margin-right: 5px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ============================
# FUNÇÃO: Carregar Dados
# ============================
@st.cache_data
def load_data():
    try:
        file_name = "02_06-2025_sisap_processado.xlsx" # CERTIFIQUE-SE QUE ESTE ARQUIVO EXISTE
        df = pd.read_excel(file_name)
        if "Data de Ingresso" in df.columns:
            df["Data de Ingresso"] = pd.to_datetime(df["Data de Ingresso"], errors='coerce').dt.normalize()
        if "Valor Contabil" in df.columns:
            df["Valor Contabil"] = pd.to_numeric(df["Valor Contabil"], errors='coerce')
        if "Valor" in df.columns:
            df["Valor"] = pd.to_numeric(df["Valor"], errors='coerce')
        if "Conta SIAFI" in df.columns:
            df["Conta SIAFI"] = pd.to_numeric(df["Conta SIAFI"], errors='coerce')
        if "Tombamento" in df.columns:
            # Garante que a coluna Tombamento seja tratada como número, ignorando erros
            df["Tombamento"] = pd.to_numeric(df["Tombamento"], errors='coerce')
        return df
    except FileNotFoundError:
        st.error(f"Erro: O arquivo '{file_name}' não foi encontrado. Verifique o caminho e o nome do arquivo.")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return None

# ============================
# FUNÇÃO: Formatar Valores
# ============================
def format_currency(x):
    if pd.isna(x):
        return "N/A"
    return "R$ {:,.2f}".format(float(x)).replace(",", "X").replace(".", ",").replace("X", ".")

# ============================
# FUNÇÃO AUXILIAR: Formatar Data de Ingresso para exibição
# ============================
def format_date_for_display(series_data_ingresso):
    if series_data_ingresso is None or not isinstance(series_data_ingresso, pd.Series):
        return pd.Series(dtype='object')
    if series_data_ingresso.empty:
        return pd.Series(dtype='object')
    parsed_dates = pd.to_datetime(series_data_ingresso, errors='coerce')
    return parsed_dates.apply(lambda x: x.strftime('%d/%m/%Y') if pd.notnull(x) and hasattr(x, 'strftime') else "N/A")

# ============================
# ABA: Apresentação (COM A LISTA CORRIGIDA)
# ============================
def exibir_apresentacao():
    st.subheader("📑 Apresentação")
    st.markdown("""
    **Análise Exploratória Amostral do SISAP**  
    Esta ferramenta foi desenvolvida a partir da troca de informações entre os membros da Comissão de Processamento de Inventário, Mario Missao e Ana Lúcia. 
    Seu objetivo é  auxiliar na análise e verificação da carga patrimonial das unidades da Universidade Federal Fluminense (UFF).   
    
    A base de dados foi coletada manualmente junto às 62 unidades que participaram do último inventário, totalizando 300 mil registros. 
    
    Os dados foram tratados e consolidados com o propósito de aprimorar a compreensão da distribuição dos bens, facilitando a 
    identificação de padrões, a detecção de inconsistências e o exame da alocação patrimonial dentro da universidade.

    Para interpretação dos dados, deve-se considerar que o Valor Analisado corresponde ao Valor de Ingresso, enquanto o Valor Contábil equivale ao Valor Depreciado.
    **Destaca-se que esta análise representa apenas uma amostra representativa e não deve ser interpretada como um relatório completo ou definitivo.**                          
    """)
    st.markdown("### Funcionalidades Disponíveis")
    funcionalidades = """
    <ul class="functionality-list">
      <li><b>Carga Patrimonial por Unidade</b>: Apresenta o total de ativos e o valor patrimonial por unidade, ajudando a detectar quais setores possuem maior concentração patrimonial.</li>
      <li><b>Bens de Alto Valor por Unidade</b>: Destaca os ativos mais relevantes, permitindo uma análise detalhada dos principais bens de cada unidade.</li>
      <li><b>Top 10 Institucional</b>: Fornece um ranking dos 10 bens com maior valor.</li>
      <li><b>Valor Discrepante</b>: Compara o valor original dos bens com o valor contábil registrado, evidenciando possíveis inconsistências que merecem atenção.</li>
      <li><b>Data Discrepante</b>: Identifica registros cuja “Data de Ingresso” esteja fora do esperado.</li>
      <li><b>Conta Siafi 18 - Livros</b>: Apresenta um resumo por unidade de todos os bens classificados na conta contábil 18 (Livros e Documentos), não considerando a SDC.</li>
      <li><b>Centavos</b>: Apresenta um resumo por unidade e o detalhamento dos bens com valor contábil igual ou inferior a R$ 0,01.</li>
      <li><b>Conta SIAFI</b>: Agrupa os dados por Conta SIAFI, exibindo o total de itens, valor de aquisição total e valor contábil total para cada conta.</li>
      <li><b>Bens</b>: Analisa e resume a situação dos bens com base no seu status (Regular vs. Diversos), considerando os 03 bens patrimoniais de maior em cada unidade.</li>
    </ul>
    """
    st.markdown(funcionalidades, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
     
    **Mario Missao Yamamoto**  
    **Comissão de Processamento de Inventário - UFF**  
    **Endereço**: R. Miguel de Frias, 9, 5º Andar, sala 502, Niterói - RJ  
    **E-mail**: processamento.dpm.cap@id.uff.br
    """)

# ============================
# ABA: Carga Patrimonial (MODIFICADA CONFORME SOLICITAÇÃO)
# ============================
def exibir_carga_patrimonial():
    st.subheader("📊 Carga Patrimonial por Unidade")
    data_original = load_data()
    if data_original is None: return

    # 1. Validação: Agora verifica também a existência da coluna "Valor"
    required_cols = ["Id", "Valor Contabil", "Valor"]
    if not all(col in data_original.columns for col in required_cols):
        missing_cols = [col for col in required_cols if col not in data_original.columns]
        st.warning(f"Colunas essenciais não encontradas: {', '.join(missing_cols)}. Não é possível gerar a carga patrimonial.")
        return

    # 2. Agregação: Soma tanto o 'Valor Contabil' quanto o 'Valor'
    df_resumo_unidade = data_original.groupby("Id", as_index=False).agg(
        Soma_Valor_Contabil=("Valor Contabil", "sum"),
        Soma_Valor=("Valor", "sum"),
        Contagem_Bens=("Id", "count")
    )
    
    # 3. Ordenação: Agora ordena pelo 'Soma_Valor' para refletir no gráfico
    df_resumo_unidade = df_resumo_unidade.sort_values("Soma_Valor", ascending=False)
    
    # Renomeia colunas numéricas para uso interno (gráfico e cálculos)
    df_resumo_unidade.rename(columns={
        "Soma_Valor": "_Valor_Numerico",
        "Soma_Valor_Contabil": "_Valor_Contabil_Numerico", 
        "Contagem_Bens": "Total de Bens"
    }, inplace=True)
    
    # 4. Criação de Colunas: Cria as colunas formatadas com os novos títulos solicitados
    df_resumo_unidade["Valor Analisado (R$)"] = df_resumo_unidade["_Valor_Numerico"].apply(format_currency)
    df_resumo_unidade["Valor Contábil Analisado (R$)"] = df_resumo_unidade["_Valor_Contabil_Numerico"].apply(format_currency)

    # Layout com as métricas primeiro
    st.markdown("##### Totais Institucionais")
    total_valor_analisado = df_resumo_unidade["_Valor_Numerico"].sum()
    total_valor_contabil = df_resumo_unidade["_Valor_Contabil_Numerico"].sum()
    total_bens_institucional = df_resumo_unidade["Total de Bens"].sum()
    try:
        formatted_total_bens = f"{total_bens_institucional:n}"
    except (ValueError, locale.Error):
        formatted_total_bens = f"{total_bens_institucional:,}".replace(",", ".")
        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Valor Analisado Total (Aquisição)", format_currency(total_valor_analisado))
    with col2:
        st.metric("Valor Contábil Total", format_currency(total_valor_contabil))
    with col3:
        st.metric("Quantidade Total de Bens", formatted_total_bens)

    st.markdown("---")
    
    # 5. Tabela de Detalhamento: Exibe a tabela com as novas colunas e títulos
    st.markdown("##### Detalhamento por Unidade")
    st.dataframe(
        df_resumo_unidade[["Id", "Total de Bens", "Valor Analisado (R$)", "Valor Contábil Analisado (R$)"]],
        column_config={
            "Id": st.column_config.TextColumn("Unidade (Id)", help="Identificador da Unidade"),
            # ALTERAÇÃO APLICADA AQUI:
            "Total de Bens": st.column_config.TextColumn("Total de Bens", help="Quantidade de bens patrimoniais na unidade"),
            "Valor Analisado (R$)": st.column_config.TextColumn("Valor Analisado (R$)", help="Soma do valor de aquisição ('Valor') dos bens na unidade"),
            "Valor Contábil Analisado (R$)": st.column_config.TextColumn("Valor Contábil Analisado (R$)", help="Soma do valor contábil dos bens na unidade"),
        }, height=450, use_container_width=True)

    # 6. Gráfico Principal: Agora reflete as informações da coluna 'Valor'
    st.subheader("📈 Top 10 Unidades por Valor Analisado (Aquisição)")
    top10_unidades = df_resumo_unidade.head(10)
    
    chart = alt.Chart(top10_unidades).mark_bar().encode(
        x=alt.X("_Valor_Numerico:Q", title="Valor Analisado (R$)"),
        y=alt.Y("Id:N", sort=alt.SortField(field="_Valor_Numerico", order="descending"), title="Unidade (Id)"),
        tooltip=[
            alt.Tooltip("Id:N", title="Unidade"), 
            alt.Tooltip("Total de Bens:Q", title="Qtd. Bens", format=","), 
            alt.Tooltip("_Valor_Numerico:Q", title="Valor Analisado (R$)", format=",.2f"),
            alt.Tooltip("_Valor_Contabil_Numerico:Q", title="Valor Contábil (R$)", format=",.2f")
        ]
    ).properties(height=400)
    
    st.altair_chart(chart, use_container_width=True)

# ============================
# ABA: Bens de Alto Valor
# ============================
def exibir_bens_alto_valor():
    st.subheader("💎 Ativos de Alto Valor por Unidade")
    data = load_data()
    if data is None: return

    # ALTERAÇÃO 1: Adicionadas as colunas 'Valor' e 'Status' aos requisitos
    required_cols = ["Id", "Valor Contabil", "Tombamento", "Bem Móvel", "Conta SIAFI", "Valor", "Status"]
    if not all(col in data.columns for col in required_cols):
        missing = [col for col in required_cols if col not in data.columns]
        st.warning(f"Colunas necessárias não encontradas: {', '.join(missing)}. Não é possível gerar a lista de bens de alto valor.")
        return

    # 03 Primeiros Bens de Alto Valor de cada Id Unico
    df_trabalho = data.groupby("Id", group_keys=False, observed=True).apply(
        lambda x: x.nlargest(3, "Valor")
    ).reset_index(drop=True)
    df_trabalho.dropna(subset=['Valor'], inplace=True)

    if df_trabalho.empty:
        st.info("Nenhum bem de alto valor encontrado para agregar por unidade.")
        return

    # ALTERAÇÃO 3: Adicionada a formatação para a nova coluna 'Valor'
    df_trabalho["Valor Analisado Formatado"] = df_trabalho["Valor"].apply(format_currency)
    df_trabalho["Valor Contabil Analisado Formatado"] = df_trabalho["Valor Contabil"].apply(format_currency)
    
    col_data_display_name = "Data de Ingresso"
    if "Data de Ingresso" in df_trabalho.columns:
        df_trabalho["Data de Ingresso Formatada"] = format_date_for_display(df_trabalho["Data de Ingresso"])
        col_data_source_for_df = "Data de Ingresso Formatada"
    else:
        df_trabalho["Data de Ingresso Formatada"] = "N/A"
        col_data_source_for_df = "Data de Ingresso Formatada"

    # ALTERAÇÃO 4: Adicionadas as colunas 'Status' e 'Valor Analisado Formatado' à lista de exibição
    cols_to_show = ["Id", "Tombamento", "Bem Móvel", "Conta SIAFI","Valor Analisado Formatado", "Valor Contabil Analisado Formatado", "Status", col_data_source_for_df]
    
    st.dataframe(
        df_trabalho[cols_to_show],
        # ALTERAÇÃO 5: Atualizado o column_config com os novos campos e o título renomeado
        column_config={
            "Id": "Unidade (Id)",
            "Tombamento": "Nº Tombamento",
            "Bem Móvel": "Descrição do Bem",
            "Conta SIAFI": "Conta Contábil",            
            "Valor Analisado Formatado": st.column_config.TextColumn("Valor Analisado (R$)"),
            "Valor Contabil Analisado Formatado": st.column_config.TextColumn("Valor Contábil Analisado (R$)"),
            "Status": st.column_config.TextColumn("Status"),
            col_data_source_for_df: st.column_config.TextColumn(col_data_display_name)
        }, height=400, use_container_width=True
    )

# ============================
# ABA: Top 10 Institucional
# ============================
def exibir_top_10():
    st.subheader("🏆 Top 10 Bens de Alto Valor Institucional")
    data = load_data()
    if data is None: return

    # ALTERAÇÃO 1: Adicionadas as colunas 'Valor' e 'Status' aos requisitos
    required_cols = ["Id", "Valor Contabil", "Tombamento", "Bem Móvel", "Conta SIAFI", "Valor", "Status"]
    if not all(col in data.columns for col in required_cols):
        missing = [col for col in required_cols if col not in data.columns]
        st.warning(f"Colunas necessárias não encontradas: {', '.join(missing)}. Não é possível gerar o Top 10.")
        return

    df_trabalho = data.nlargest(10, "Valor").reset_index(drop=True)
    df_trabalho.dropna(subset=['Valor'], inplace=True)

    if df_trabalho.empty:
        st.info("Nenhum bem encontrado para compor o Top 10.")
        return

    # ALTERAÇÃO 2: Adicionada a formatação para 'Valor' e renomeada a variável de 'Valor Contabil' para clareza
    df_trabalho["Valor Analisado Formatado"] = df_trabalho["Valor"].apply(format_currency)
    df_trabalho["Valor Contabil Analisado Formatado"] = df_trabalho["Valor Contabil"].apply(format_currency)

    col_data_display_name = "Data de Ingresso"
    if "Data de Ingresso" in df_trabalho.columns:
        df_trabalho["Data de Ingresso Formatada"] = format_date_for_display(df_trabalho["Data de Ingresso"])
        col_data_source_for_df = "Data de Ingresso Formatada"
    else:
        df_trabalho["Data de Ingresso Formatada"] = "N/A"
        col_data_source_for_df = "Data de Ingresso Formatada"
        
    # ALTERAÇÃO 3: Adicionadas as novas colunas à lista de exibição na ordem solicitada
    cols_to_show = ["Id", "Tombamento", "Bem Móvel", "Conta SIAFI", "Valor Analisado Formatado", "Valor Contabil Analisado Formatado", "Status", col_data_source_for_df]

    st.dataframe(
        df_trabalho[cols_to_show],
        # ALTERAÇÃO 4: Atualizado o column_config com os novos campos e títulos
        column_config={
            "Id": "Unidade (Id)",
            "Tombamento": "Nº Tombamento",
            "Bem Móvel": "Descrição do Bem",
            "Conta SIAFI": "Conta Contábil",
            "Valor Analisado Formatado": st.column_config.TextColumn("Valor Analisado (R$)"),
            "Valor Contabil Analisado Formatado": st.column_config.TextColumn("Valor Contábil Analisado (R$)"),
            "Status": st.column_config.TextColumn("Status"),
            col_data_source_for_df: st.column_config.TextColumn(col_data_display_name)
        }, height=400, use_container_width=True
    )
# ============================
# ABA: Análise dos Bens de Maior Valor por Unidade (MODIFICADA)
# ============================
def exibir_aba_bens():
    # Título da aba atualizado para refletir a nova funcionalidade
    st.subheader("🔎 Bens de Maior Valor: Visão por Status")

    data_original = load_data()
    if data_original is None: return

    # Verificação de colunas necessárias para a nova lógica
    required_cols = ['Id', 'Valor', 'Valor Contabil', 'Tombamento', 'Bem Móvel', 'Status', 'Conta SIAFI']
    if not all(col in data_original.columns for col in required_cols):
        missing_cols = [col for col in required_cols if col not in data_original.columns]
        st.warning(f"Colunas essenciais não encontradas para esta análise: {', '.join(missing_cols)}.")
        return

    # Busca os 3 bens de maior valor (coluna 'Valor') para cada Id único.
    df_trabalho = data_original.groupby("Id", group_keys=False, observed=True).apply(
        lambda x: x.nlargest(3, "Valor")
    ).reset_index(drop=True)

    if df_trabalho.empty:
        st.error("Nenhum bem encontrado para realizar a análise. Verifique os dados de origem.")
        return
        
    # Resumo do Subconjunto
    st.markdown("##### Top 3 por Unidade")
    total_itens_selecionados = len(df_trabalho)
    total_valor_analisado = df_trabalho['Valor'].sum()
    total_valor_contabil = df_trabalho['Valor Contabil'].sum()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Itens Selecionados", f"{total_itens_selecionados:,}".replace(",", "."))
    with col2:
        st.metric("Soma do Valor Analisado (R$)", format_currency(total_valor_analisado))
    with col3:
        st.metric("Soma do Valor Contábil (R$)", format_currency(total_valor_contabil))

    st.markdown("---")

    # Gráfico de Unidades
    st.markdown("##### As 10 Unidades com os Maiores Valores de Ingresso")
    
    df_para_grafico = df_trabalho.groupby('Id', as_index=False).agg(
        _Soma_Valor_Numerico=('Valor', 'sum')
    ).nlargest(10, '_Soma_Valor_Numerico')

    chart = alt.Chart(df_para_grafico).mark_bar().encode(
        x=alt.X('_Soma_Valor_Numerico:Q', title="Valor Analisado Somado (R$)"),
        y=alt.Y('Id:N', title="Unidade (Id)", sort='-x'),
        tooltip=[
            alt.Tooltip('Id:N', title='Unidade'), 
            alt.Tooltip('_Soma_Valor_Numerico:Q', title='Soma Valor Analisado (R$)', format='$,.2f')
        ]
    ).properties(title="- Baseado na Avaliação dos 3 Principais Bens de Cada Unidade", height=350)
    st.altair_chart(chart, use_container_width=True)

    st.markdown("---")
    
    # Painel de Detalhamento
    with st.expander(f"Visualizar Detalhamento dos {total_itens_selecionados} Bens Selecionados", expanded=False):
        df_trabalho['Valor Analisado Formatado'] = df_trabalho['Valor'].apply(format_currency)
        df_trabalho['Valor Contabil Analisado Formatado'] = df_trabalho['Valor Contabil'].apply(format_currency)
        
        col_data_source = 'Data Ingresso Formatada'
        if 'Data de Ingresso' in df_trabalho.columns:
            df_trabalho[col_data_source] = format_date_for_display(df_trabalho['Data de Ingresso'])
        else:
            df_trabalho[col_data_source] = "N/A"

        cols_to_show = [
            'Id', 'Tombamento', 'Bem Móvel', 'Conta SIAFI', 
            'Valor Analisado Formatado', 'Valor Contabil Analisado Formatado', 
            'Status', col_data_source
        ]
        
        df_detalhado_ordenado = df_trabalho.sort_values(by=["Id", "Valor"], ascending=[True, False])
        
        st.dataframe(
            df_detalhado_ordenado[cols_to_show],
            column_config={
                "Id": "Unidade (Id)",
                "Tombamento": "Nº Tombamento",
                "Bem Móvel": "Descrição do Bem",
                "Conta SIAFI": "Conta Contábil",
                "Valor Analisado Formatado": st.column_config.TextColumn("Valor Analisado (R$)"),
                "Valor Contabil Analisado Formatado": st.column_config.TextColumn("Valor Contábil Analisado (R$)"),
                "Status": st.column_config.TextColumn("Status"),
                "Data Ingresso Formatada": "Data de Ingresso"
            },
            height=400,
            use_container_width=True
        )

    # ============================
    # Resumo por Status dos Bens
    # ============================
    st.markdown("---")
    st.markdown("##### Resumo por Status dos Bens")

    df_regular = df_trabalho[df_trabalho['Status'] == 'Regular']
    quantidade_regular = len(df_regular)
    valor_ingresso_regular = df_regular['Valor'].sum()
    valor_contabil_regular = df_regular['Valor Contabil'].sum()

    df_irregular = df_trabalho[df_trabalho['Status'] != 'Regular']
    quantidade_irregular = len(df_irregular)
    valor_ingresso_irregular = df_irregular['Valor'].sum()
    valor_contabil_irregular = df_irregular['Valor Contabil'].sum()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Bens com Status Regular")
        st.metric("Quantidade", f"{quantidade_regular:,}".replace(",", "."))
        st.metric("Valor de Ingresso (R$)", format_currency(valor_ingresso_regular))
        st.metric("Valor Contábil (R$)", format_currency(valor_contabil_regular))

    with col2:
        st.markdown("##### Bens com Status Diversos")
        st.metric("Quantidade", f"{quantidade_irregular:,}".replace(",", "."))
        st.metric("Valor de Ingresso (R$)", format_currency(valor_ingresso_irregular))
        st.metric("Valor Contábil (R$)", format_currency(valor_contabil_irregular))

    st.markdown("---")

# ============================
# ABA: Relatório (Valor Contábil > Valor)
# ============================
def exibir_valor_discrepante():
    st.subheader("📝 Relatório: Bens com Valor Contábil Superior ao Valor de Aquisição")
    data = load_data()
    if data is None: return

    required_cols = ["Id", "Valor Contabil", "Valor", "Tombamento", "Bem Móvel", "Conta SIAFI"]
    if not all(col in data.columns for col in required_cols):
        missing = [col for col in required_cols if col not in data.columns]
        st.warning(f"Colunas necessárias não encontradas: {', '.join(missing)}. Não é possível gerar o relatório de valor discrepante.")
        return
    
    df_trabalho = data[data["Valor Contabil"] > data["Valor"]].copy()

    if df_trabalho.empty:
        st.info("Nenhum registro encontrado onde o Valor Contábil seja superior ao Valor de Aquisição.")
        return

    df_trabalho.sort_values("Valor Contabil", ascending=False, inplace=True)
    df_trabalho["Valor Aquisição Formatado"] = df_trabalho["Valor"].apply(format_currency)
    df_trabalho["Valor Contabil Formatado"] = df_trabalho["Valor Contabil"].apply(format_currency)

    col_data_display_name = "Data de Ingresso"
    if "Data de Ingresso" in df_trabalho.columns:
        df_trabalho["Data de Ingresso Formatada"] = format_date_for_display(df_trabalho["Data de Ingresso"])
        col_data_source_for_df = "Data de Ingresso Formatada"
    else:
        df_trabalho["Data de Ingresso Formatada"] = "N/A"
        col_data_source_for_df = "Data de Ingresso Formatada"
    
    cols_to_show = ["Id", "Tombamento", "Bem Móvel", "Conta SIAFI", "Valor Aquisição Formatado", "Valor Contabil Formatado", col_data_source_for_df]

    st.dataframe(
        df_trabalho[cols_to_show],
        column_config={
            "Id": "Unidade (Id)", "Tombamento": "Nº Tombamento", "Bem Móvel": "Descrição do Bem",
            "Conta SIAFI": "Conta Contábil", "Valor Aquisição Formatado": "Valor Analisado (R$)",
            "Valor Contabil Formatado": "Valor Contábil Analisado (R$)",
            col_data_source_for_df: st.column_config.TextColumn(col_data_display_name),
        }, height=400, use_container_width=True
    )

    total_valor_aquisicao = df_trabalho["Valor"].dropna().sum()
    total_valor_contabil = df_trabalho["Valor Contabil"].dropna().sum()
    qtd_registros = len(df_trabalho)

    st.markdown("---"); st.markdown("### Resumo dos Itens com Divergência")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Valor Aquisição (R$)", format_currency(total_valor_aquisicao))
    col2.metric("Total Valor Contábil (R$)", format_currency(total_valor_contabil))
    col3.metric("Qtd. Registros", f"{qtd_registros:,}".replace(",", "."))

# ============================
# ABA: Data Discrepante
# ============================
def exibir_data_discrepante():
    st.subheader("📅 Data de Ingresso Discrepante")
    data_original = load_data()
    if data_original is None: return

    data = data_original.copy()

    required_cols_base = ["Id", "Valor Contabil", "Valor", "Tombamento", "Bem Móvel", "Conta SIAFI"]
    if "Data de Ingresso" not in data.columns:
        st.warning("A coluna 'Data de Ingresso' não foi encontrada nos dados. Não é possível gerar o relatório de data discrepante.")
        return
    if not all(col in data.columns for col in required_cols_base):
        missing = [col for col in required_cols_base if col not in data.columns]
        st.warning(f"Colunas base necessárias não encontradas: {', '.join(missing)}. Não é possível gerar o relatório de data discrepante.")
        return

    data["Data de Ingresso Convertida"] = pd.to_datetime(data["Data de Ingresso"], errors="coerce")
    data_valid_dates = data.dropna(subset=["Data de Ingresso Convertida"]).copy()

    data_limite_futura = pd.to_datetime("2025-12-31")
    data_limite_antiga = pd.to_datetime("1900-01-01")

    df_data_discrepante = data_valid_dates[
        (data_valid_dates["Data de Ingresso Convertida"] > data_limite_futura) |
        (data_valid_dates["Data de Ingresso Convertida"] < data_limite_antiga)
    ].copy()

    if df_data_discrepante.empty:
        st.info(f"Nenhum registro com data de ingresso posterior a {data_limite_futura.strftime('%d/%m/%Y')} ou anterior a {data_limite_antiga.strftime('%d/%m/%Y')} encontrado, ou com datas inválidas.")
        return

    df_data_discrepante["Valor Aquisição Formatado"] = df_data_discrepante["Valor"].apply(format_currency)
    df_data_discrepante["Valor Contabil Formatado"] = df_data_discrepante["Valor Contabil"].apply(format_currency)
    
    df_data_discrepante["Data de Ingresso Formatada"] = df_data_discrepante["Data de Ingresso Convertida"].dt.strftime("%d/%m/%Y")
    
    col_data_display_name = "Data de Ingresso"
    col_data_source_for_df = "Data de Ingresso Formatada"

    cols_to_show = ["Id", "Tombamento", "Bem Móvel", "Conta SIAFI", "Valor Aquisição Formatado", "Valor Contabil Formatado", col_data_source_for_df]
    
    st.dataframe(
        df_data_discrepante[cols_to_show],
        column_config={
            "Id": "Unidade (Id)", "Tombamento": "Nº Tombamento", "Bem Móvel": "Descrição do Bem",
            "Conta SIAFI": "Conta Contábil", "Valor Aquisição Formatado": "Valor Aquisição (R$)",
            "Valor Contabil Formatado": "Valor Contábil (R$)",
            col_data_source_for_df: st.column_config.TextColumn(col_data_display_name)
        }, height=400, use_container_width=True
    )

    total_registros = len(df_data_discrepante)
    total_valor_aquisicao = df_data_discrepante["Valor"].dropna().sum()
    total_valor_contabil = df_data_discrepante["Valor Contabil"].dropna().sum()

    st.markdown("---"); st.markdown("### Resumo Consolidado dos Itens com Data Discrepante")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Registros", f"{total_registros:,}".replace(",", "."))
    col2.metric("Total Valor Aquisição (R$)", format_currency(total_valor_aquisicao))
    col3.metric("Total Valor Contábil (R$)", format_currency(total_valor_contabil))

# ============================
# ABA: Conta Siafi 18 - Livros
# ============================
def exibir_conta_siafi_18():
    st.subheader("📚 Conta SIAFI 18 - Livros e Documentos")
    data_original = load_data()
    if data_original is None:
        return

    data = data_original.copy()

    required_cols = ["Id", "Conta SIAFI", "Valor", "Valor Contabil", "Tombamento", "Bem Móvel"]
    if not all(col in data.columns for col in required_cols):
        missing = [col for col in required_cols if col not in data.columns]
        st.warning(f"Colunas necessárias não encontradas: {', '.join(missing)}. Não é possível gerar a aba Conta SIAFI 18.")
        return
    
    df_trabalho = data[data["Conta SIAFI"] == 18].copy()

    if df_trabalho.empty:
        st.info("Nenhum registro encontrado para a Conta SIAFI 18 (Livros e Documentos).")
        return

    st.markdown("##### Detalhamento por Unidade (Conta SIAFI 18)")
    
    df_resumo_id_siafi18 = df_trabalho.groupby("Id", as_index=False).agg(
        Quantidade_Bens_Siafi18=("Tombamento", "count"),
        _Soma_Valor_Analisado_Numerico=("Valor", "sum"),
        _Soma_Valor_Contabil_Siafi18_Numerico=("Valor Contabil", "sum")
    ).sort_values("_Soma_Valor_Contabil_Siafi18_Numerico", ascending=False)
    
    df_resumo_id_siafi18["Valor Analisado Total (R$)"] = df_resumo_id_siafi18["_Soma_Valor_Analisado_Numerico"].apply(format_currency)
    df_resumo_id_siafi18["Valor Contábil Analisado Total (R$)"] = df_resumo_id_siafi18["_Soma_Valor_Contabil_Siafi18_Numerico"].apply(format_currency)
    
    st.dataframe(
        df_resumo_id_siafi18[["Id", "Quantidade_Bens_Siafi18", "Valor Analisado Total (R$)", "Valor Contábil Analisado Total (R$)"]],
        column_config={
            "Id": st.column_config.TextColumn("Unidade (Id)", help="Identificador da Unidade"),
            # ALTERAÇÃO APLICADA AQUI: Trocado para TextColumn para alinhar à esquerda
            "Quantidade_Bens_Siafi18": st.column_config.TextColumn("Qtd. Bens na Conta 18", help="Quantidade de bens da Conta SIAFI 18 na unidade"),
            "Valor Analisado Total (R$)": st.column_config.TextColumn("Valor Analisado Total (R$)", help="Soma do valor analisado dos bens da Conta SIAFI 18 na unidade"),
            "Valor Contábil Analisado Total (R$)": st.column_config.TextColumn("Valor Contábil Analisado Total (R$)", help="Soma do valor contábil dos bens da Conta SIAFI 18 na unidade"),
        },
        height=300,
        use_container_width=True
    )
    st.markdown("---")

    with st.expander("Visualizar Detalhamento de Todos os Bens (Conta SIAFI 18)", expanded=False):
        df_trabalho["Valor Analisado Formatado"] = df_trabalho["Valor"].apply(format_currency)
        df_trabalho["Valor Contabil Analisado Formatado"] = df_trabalho["Valor Contabil"].apply(format_currency)
        
        cols_to_show_detalhado = ["Id", "Tombamento", "Bem Móvel", "Conta SIAFI", "Valor Analisado Formatado", "Valor Contabil Analisado Formatado"]
        
        st.dataframe(
            df_trabalho[cols_to_show_detalhado],
            column_config={
                "Id": st.column_config.TextColumn("Unidade (Id)"),
                "Tombamento": st.column_config.TextColumn("Nº Tombamento"),
                "Bem Móvel": st.column_config.TextColumn("Descrição do Bem"),
                "Conta SIAFI": st.column_config.NumberColumn("Conta Contábil", format="%d"),
                "Valor Analisado Formatado": st.column_config.TextColumn("Valor Analisado (R$)"),
                "Valor Contabil Analisado Formatado": st.column_config.TextColumn("Valor Contábil Analisado (R$)")
            },
            height=400,
            use_container_width=True
        )
    
    st.markdown("---")
    st.markdown("### Resumo Consolidado Geral (Conta SIAFI 18)")

    ids_unicos_na_conta18 = df_trabalho["Id"].nunique()
    quantidade_total_bens_conta18 = len(df_trabalho)
    
    soma_total_valor_analisado_conta18 = df_trabalho["Valor"].dropna().sum()
    soma_total_valor_contabil_conta18 = df_trabalho["Valor Contabil"].dropna().sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Unidades (Id) Distintas com Itens na Conta 18", f"{ids_unicos_na_conta18}")
    col2.metric("Qtd. Total de Bens na Conta 18", f"{quantidade_total_bens_conta18:,}".replace(",", "."))
    col3.metric("Valor Analisado Total da Conta 18 (R$)", format_currency(soma_total_valor_analisado_conta18))
    col4.metric("Valor Contábil Analisado Total da Conta 18 (R$)", format_currency(soma_total_valor_contabil_conta18))

# ============================
# ABA: Centavos
# ============================
def exibir_aba_centavos():
    st.subheader("🪙 Bens com Valor Residual (Centavos)")
    data_original = load_data()
    if data_original is None:
        return

    data = data_original.copy()

    required_cols_base_centavos = ["Id", "Valor Contabil", "Valor", "Tombamento", "Bem Móvel", "Conta SIAFI"]
    if not all(col in data.columns for col in required_cols_base_centavos):
        missing = [col for col in required_cols_base_centavos if col not in data.columns]
        st.warning(f"Colunas necessárias não encontradas: {', '.join(missing)}. Não é possível gerar a aba Centavos.")
        return
    
    # Criando a nova coluna "Valor Analisado"
    data["Valor Analisado"] = data["Valor"]

    # Aplicando o filtro **apenas** na coluna "Valor Analisado" (≤ 0,01)
    df_trabalho_centavos = data[data["Valor Analisado"].notna() & (data["Valor Analisado"] <= 0.01)].copy()

    if df_trabalho_centavos.empty:
        st.info("Nenhum bem encontrado com valor analisado igual ou inferior a R$ 0,01.")
        return

    st.markdown("##### Detalhamento por Unidade")
    df_resumo_id_centavos = df_trabalho_centavos.groupby("Id", as_index=False).agg(
        Quantidade_Bens_Centavos=("Tombamento", "count"), 
        _Soma_Valor_Analisado_Numerico=("Valor Analisado", "sum"),
        _Soma_Valor_Contabil_Numerico=("Valor Contabil", "sum")
    ).sort_values("_Soma_Valor_Analisado_Numerico", ascending=True)
    
    df_resumo_id_centavos["Valor Analisado Total (R$)"] = df_resumo_id_centavos["_Soma_Valor_Analisado_Numerico"].apply(format_currency)
    df_resumo_id_centavos["Valor Contábil Total Residual (R$)"] = df_resumo_id_centavos["_Soma_Valor_Contabil_Numerico"].apply(format_currency)

    st.dataframe(
        df_resumo_id_centavos[["Id", "Quantidade_Bens_Centavos", "Valor Analisado Total (R$)", "Valor Contábil Total Residual (R$)"]],
        column_config={
            "Id": st.column_config.TextColumn("Unidade (Id)", help="Identificador da Unidade"),
            # ALTERAÇÃO APLICADA AQUI:
            "Quantidade_Bens_Centavos": st.column_config.TextColumn("Qtd. Bens Residuais", help="Quantidade de bens com valor residual na unidade"),
            "Valor Analisado Total (R$)": st.column_config.TextColumn("Valor Analisado Total (R$)"),
            "Valor Contábil Total Residual (R$)": st.column_config.TextColumn("Valor Contábil Total (R$)")
        },
        height=300,
        use_container_width=True
    )
    st.markdown("---")

    df_trabalho_centavos["Valor Analisado Formatado"] = df_trabalho_centavos["Valor Analisado"].apply(format_currency)
    df_trabalho_centavos["Valor Contabil Formatado"] = df_trabalho_centavos["Valor Contabil"].apply(format_currency)
    cols_to_show_detalhado_centavos = ["Id", "Tombamento", "Bem Móvel", "Conta SIAFI", "Valor Analisado Formatado", "Valor Contabil Formatado"]

    st.markdown("##### Detalhamento de Todos os Bens com Valor Residual")
    df_detalhado_ordenado_centavos = df_trabalho_centavos.sort_values(by=["Id", "Valor Analisado", "Tombamento"])

    st.dataframe(
        df_detalhado_ordenado_centavos[cols_to_show_detalhado_centavos],
        column_config={
            "Id": st.column_config.TextColumn("Unidade (Id)"),
            "Tombamento": st.column_config.TextColumn("Nº Tombamento"),
            "Bem Móvel": st.column_config.TextColumn("Descrição do Bem"),
            "Conta SIAFI": st.column_config.NumberColumn("Conta Contábil", format="%d"),
            "Valor Analisado Formatado": st.column_config.TextColumn("Valor Analisado (R$)"),
            "Valor Contabil Formatado": st.column_config.TextColumn("Valor Contábil (R$)")
        },
        height=450,
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("### Resumo Consolidado Geral")
        
    ids_unicos_com_centavos = df_trabalho_centavos["Id"].nunique()
    quantidade_total_bens_centavos = len(df_trabalho_centavos)
    soma_total_valor_analisado_centavos = df_trabalho_centavos["Valor Analisado"].dropna().sum()
    soma_total_valor_contabil_centavos = df_trabalho_centavos["Valor Contabil"].dropna().sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Unidades (Id) Distintas com Itens Residuais", f"{ids_unicos_com_centavos}")
    col2.metric("Qtd. Total de Bens Residuais", f"{quantidade_total_bens_centavos:,}".replace(",", "."))
    col3.metric("Valor Analisado Total dos Itens Residuais (R$)", format_currency(soma_total_valor_analisado_centavos))
    col4.metric("Valor Contábil Total dos Itens Residuais (R$)", format_currency(soma_total_valor_contabil_centavos))

# ============================
# ABA: Resumo por Conta SIAFI
# ============================
def exibir_aba_siafi():
    st.subheader("📊 Conta SIAFI")
    data_original = load_data()
    if data_original is None:
        return

    data = data_original.copy()
    
    col_para_contagem = "Id" 
    if col_para_contagem not in data.columns:
        if "Tombamento" in data.columns:
            col_para_contagem = "Tombamento"
        else:
            st.warning("Nenhuma coluna identificadora de item ('Id' ou 'Tombamento') encontrada para contagem.")
            return
            
    required_cols = ["Conta SIAFI", "Valor", "Valor Contabil", col_para_contagem]
    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        st.warning(f"Colunas essenciais não encontradas para gerar o resumo por Conta SIAFI: {', '.join(missing_cols)}.")
        return
        
    df_resumo_siafi = data.groupby("Conta SIAFI", as_index=False).agg(
        Total_Itens=(col_para_contagem, "count"),
        _Soma_Valor_Numerico=("Valor", "sum"),
        _Soma_Valor_Contabil_Numerico=("Valor Contabil", "sum")
    )

    if df_resumo_siafi.empty:
        st.info("Nenhum dado encontrado para agrupar por Conta SIAFI.")
        return

    df_resumo_siafi["Valor Total Analisado (R$)"] = df_resumo_siafi["_Soma_Valor_Numerico"].apply(format_currency)
    df_resumo_siafi["Valor Contábil Analisado (R$)"] = df_resumo_siafi["_Soma_Valor_Contabil_Numerico"].apply(format_currency)

    df_resumo_siafi = df_resumo_siafi.sort_values("Conta SIAFI", ascending=True)

    st.markdown("##### Detalhamento por Conta SIAFI")
    cols_para_exibir_siafi = ["Conta SIAFI", "Total_Itens", "Valor Total Analisado (R$)", "Valor Contábil Analisado (R$)"]
    st.dataframe(
        df_resumo_siafi[cols_para_exibir_siafi],
        column_config={
            # ALTERAÇÃO APLICADA AQUI:
            "Conta SIAFI": st.column_config.TextColumn("Conta SIAFI", help="Número da Conta Contábil SIAFI"),
            "Total_Itens": st.column_config.TextColumn("Total de Itens", help="Quantidade de bens nesta conta SIAFI"),
            "Valor Total Analisado (R$)": st.column_config.TextColumn("Valor Total Analisado (R$)", help="Soma do valor de aquisição dos bens nesta conta"),
            "Valor Contábil Analisado (R$)": st.column_config.TextColumn("Valor Contábil Analisado (R$)", help="Soma do valor contábil dos bens nesta conta"),
        },
        height=450,
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("### Resumo Geral das Contas SIAFI")

    total_contas_siafi_distintas = df_resumo_siafi["Conta SIAFI"].nunique()
    total_geral_itens = df_resumo_siafi["Total_Itens"].sum()
    soma_geral_valor = df_resumo_siafi["_Soma_Valor_Numerico"].sum()
    soma_geral_valor_contabil = df_resumo_siafi["_Soma_Valor_Contabil_Numerico"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Contas SIAFI Distintas", f"{total_contas_siafi_distintas}")
    col2.metric("Total Geral de Itens", f"{total_geral_itens:,}".replace(",", "."))
    col3.metric("Soma Total Geral de Aquisição (R$)", format_currency(soma_geral_valor))
    col4.metric("Soma Total Geral Contábil (R$)", format_currency(soma_geral_valor_contabil))

# ============================
# FUNÇÃO PRINCIPAL
# ============================
def main():
    load_custom_css()
    st.markdown("""<div class="custom-header"><h1>🏛️ UFF - Comissão de Processamento de Inventário</h1></div>""", unsafe_allow_html=True)

    # Reordenação: Aba "Bens" movida para o final
    tabs_names = [
        "Apresentação", "Carga Patrimonial", "Bens de Alto Valor", 
        "Top 10 Institucional", "Valor Discrepante", "Data Discrepante",
        "Conta Siafi 18 - Livros", "Centavos", "Conta SIAFI", "Bens"
    ]
    tab_functions = [
        exibir_apresentacao, exibir_carga_patrimonial, exibir_bens_alto_valor,
        exibir_top_10, exibir_valor_discrepante, exibir_data_discrepante,
        exibir_conta_siafi_18, exibir_aba_centavos, exibir_aba_siafi, exibir_aba_bens
    ]
    
    tabs = st.tabs(tabs_names)
    for i, tab in enumerate(tabs):
        with tab:
            tab_functions[i]()

if __name__ == "__main__":
    main()