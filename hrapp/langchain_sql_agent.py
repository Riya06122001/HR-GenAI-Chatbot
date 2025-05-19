from langchain.utilities import SQLDatabase
from langchain.chat_models import AzureChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.memory import ConversationBufferMemory
 
# Set up the SQL database connection
db = SQLDatabase.from_uri(
    "postgresql+psycopg2://hradmin:pass#1234@hr-chatbot-db.postgres.database.azure.com/hr_database"
)
 
# Set up the LLM (Azure OpenAI)
llm = AzureChatOpenAI(
    deployment_name="gpt-4o",
    model_name="gpt-4",
    temperature=0,
    openai_api_version="2024-03-01-preview",
    openai_api_key="DVx5kzwinP9CSaaI9JHY3BLYV3yRVzqsU2aSGJXaXFIJiMqLsqEYJQQJ99AKACYeBjFXJ3w3AAABACOGIk13",
    openai_api_base="https://riya-openai.openai.azure.com/",
    
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
 
 