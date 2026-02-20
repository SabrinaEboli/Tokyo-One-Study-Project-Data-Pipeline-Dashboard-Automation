import pandas as pd
import smtplib
from email.message import EmailMessage

# limpeza dos dados
def limpar_dados(df):

    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()
    df = df.dropna(how='all')
    df = df.dropna(subset=['Order ID'])

    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Price'] = df['Price'].fillna(0)

    return df

# relatorio mensal criar nova tabela
def gerar_relatorio_geral(df, arquivo_saida):

    # df_mes = df[df['Month'] == x ]

    tabela = (
        df
        .groupby('Food item')['Price']
        .sum()
        .reset_index()
        .rename(columns={'Price': 'Total Revenue'})
        # ordena do maior para menor
        .sort_values(by='Total Revenue', ascending=False)
    )

    tabela.to_csv(arquivo_saida, index=False)

    print(f"Arquivo {arquivo_saida} salvo com sucesso!")

    return arquivo_saida

# enviar email automatico
def enviar_email(arquivo):

    email_remetente = "xxx@gmail.com"
    senha = "xxxx"
    email_destino = "xxx@gmail.com"

    msg = EmailMessage()
    msg['Subject'] = "Relatório automático - Tokyo One"
    msg['From'] = email_remetente
    msg['To'] = email_destino
    msg.set_content(
        "Segue em anexo o relatório automático de faturamento por item.")

# anexa o arquivo
    with open(arquivo, 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype='application',
            subtype='octet-stream',
            filename=arquivo
        )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_remetente, senha)
        smtp.send_message(msg)

    print("Email enviado com sucesso!")


# le o arquivo limpa ele passa pelo agrupamento pra fzr a nova tabela e envia o email (executa tudo)
df = pd.read_csv("tokyo one.csv")

df = limpar_dados(df)

arquivo = gerar_relatorio_geral(
    df,
    arquivo_saida="relatorio_geral.csv"
)

enviar_email(arquivo)
