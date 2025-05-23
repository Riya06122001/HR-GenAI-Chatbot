from langchain.utilities import SQLDatabase
from langchain.chat_models import AzureChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.memory import ConversationBufferMemory
import os


 
def ask_agent(query,db_url, deployment_name, openai_api_version, model_name, openai_api_key, openai_api_base):
    try:
        # Set up the SQL database connection
        db = SQLDatabase.from_uri(db_url)

        # Set up the LLM (Azure OpenAI)
        llm = AzureChatOpenAI(
            deployment_name=deployment_name,
            openai_api_version=openai_api_version,
            model_name=model_name,
            temperature=0,
            openai_api_key=openai_api_key,
            openai_api_base=openai_api_base,
            openai_api_type="azure",

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
        return agent_executor.run(query)
    except Exception as e:
        return f"Error: {str(e)}"
 
 