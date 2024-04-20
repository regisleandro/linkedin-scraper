import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate

class Openai:
  def __init__(self) -> None:
    load_dotenv()

  def default_message_template(self):
    return  """
      Você é um assistante de rh online, que irá avaliar um curriculo a partir de um perfil do linkedin, se possivel, adicione o tempo de experiência em cada cargo.
      Adicione uma classificação conforme o nível de senioridade (tempo de experiência) de cada cargo, classificando em perfil iniciante, perfil intermediário e perfil sênior.
      Considere como:
        - perfil sênior aqueles com mais de 5 anos de experiência, 
        - perfil intermediário aqueles entre 2 a 5 anos de experiência
        - perfil iniciante aqueles com menos de 2 anos de experiência.
      Não invente respostas, apenas resuma o que está no perfil.
      Agrupe em sessões nome, sobre e experiência.
      Retorne o texto em markdown, use heading level 3 para os títulos e heading level 4 para os subtítulos.
      Ao final do texto, adicione um resumo do perfil (somente considere a experiência para criar o resumo).
      Adicione uma seção  com a classificação de senioridade e a indicação de:
      - 👀 para perfil iniciante, 
      - 📆 para perfil pleno e 
      - 📅 💰 para perfil sênior, use heading level 4 para o título
      Todo o texto deve ser traduzido para o português.
      Esse é o perfil do linkedin:
    """

  def summarize_profile(self, profile, template_text=None):
    message_template = self.default_message_template()
    if template_text:
      message_template = template_text
    
    chat_template = ChatPromptTemplate.from_messages([
      ('system', message_template),
      ('user', "{profile}")
    ])

    messages = chat_template.format_messages(profile=profile)

    model_name = 'gpt-3.5-turbo'
    llm = ChatOpenAI(model_name=model_name, temperature=0, max_tokens=3000)
    summarize = llm(messages)

    return re.sub(r"\.", r". \n", summarize.content)