from langchain.utilities import SQLDatabase
from langchain.chat_models import AzureChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.memory import ConversationBufferMemory
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hrproject.settings")
from django.conf import settings 

 
# Set up the SQL database connection
db = SQLDatabase.from_uri(settings.DATABASE_URL)    
 
# Set up the LLM (Azure OpenAI)
llm = AzureChatOpenAI(
    deployment_name=settings.DEPLOYMENT_NAME,
    openai_api_version=settings.OPENAI_API_VERSION,
    model_name=settings.MODEL_NAME,
    temperature=0,
    openai_api_key = settings.OPENAI_API_KEY,
    openai_api_base = settings.OPENAI_API_BASE,
    openai_api_type = "azure",
    
    
)
 
memory = ConversationBufferMemory(memory_key="chat_history")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
 
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    memory=memory,
    agent_type="openai-tools"
)
 
def ask_agent(query):
    try:
        return agent_executor.run(query)
    except Exception as e:
        return f"Error: {str(e)}"
 
 