import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Henrique Farmaco Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define um prompt de sistema que descreve as regras e comportamento do assistente de IA
CUSTOM_PROMPT = """
Você é o "Auxiliar do Henrique", um assistente de IA especialista em farmacia, com foco principal em remedios. Sua missão é ajudar farmaceuticos iniciantes com dúvidas sobre remedios de forma clara, precisa e útil.

REGRAS DE OPERAÇÃO:
1.  **Foco em Farmacia**: Responda apenas a perguntas relacionadas a Farmacos, remedios, bulas, quimicas, efeitos colaterais e intercambialidade. Se o usuário perguntar sobre outro assunto, responda educadamente que seu foco é exclusivamente em auxiliar com Farmacia.
2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo de Remedios**: Forneça um ou mais blocos de informacao sobre o assunto em si com outros remedios parecidos. O remedio ou duvida deve ser bem comentado para explicar as partes importantes.
    * **Detalhes do Remedio**: Após o bloco introdutorio, descreva em detalhes o que cada parte do que a quimica faz, explicando a relacao e os efeitos e as funções utilizadas.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante para a documentação oficial de onde tirou a resposta (https://consultas.anvisa.gov.br/#/bulario/sa.com) ou da biblioteca em questão.
3.  **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""


with st.sidebar:
    
    st.title("Assistente de Farmacia")

    st.markdown("Assistente de Farmacia para consulta")
    
    groq_api_key = st.text_input(
        "Insert your api Key", 
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )

    st.markdown("---")
    st.markdown("Me ajude com...")

    st.markdown("---")

st.title("Este assistene te auxilia a obter informação sobre tudo relacionado a Farmacia")

st.title("Ola eu sou o Groqx, como posso te ajudar hoje?")

st.caption("Tire Sua Duvida")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

client = None

if groq_api_key:
    
    try:
        
        client = Groq(api_key = groq_api_key)
    
    except Exception as e:
        
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()


elif st.session_state.messages:
     st.warning("Please insert your Groq key")


if prompt := st.chat_input("insert questions"):
    
    if not client:
        st.warning("Set your Grot API key to Start")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        
        messages_for_api.append(msg)

    with st.chat_message("assistant"):
        
        with st.spinner("analisys"):
            
            try:
                
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-20b", 
                    temperature = 0.7,
                    max_tokens = 2048,
                )
                
                dsa_ai_resposta = chat_completion.choices[0].message.content
                
                st.markdown(dsa_ai_resposta)
                
                st.session_state.messages.append({"role": "assistant", "content": dsa_ai_resposta})

            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")


