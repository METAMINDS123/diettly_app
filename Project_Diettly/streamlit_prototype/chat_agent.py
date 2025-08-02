'''
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Initialize your LLM
def get_chat_agent():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
    memory = ConversationBufferMemory()
    conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
    return conversation
    '''
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

def get_chat_agent():
    template = """
    You are Diettly, an AI-powered meal planner.
    Step-by-step, help the user by asking for:
    1. Age, height, weight → calculate BMI
    2. Allergies or health conditions
    3. Diet/cuisine preferences
    4. Pantry items (if needed)
    Then confirm data and recommend meals.

    Always confirm before giving a meal plan.

    Current conversation:
    {history}
    Human: {input}
    AI:"""

    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=template
    )

    llm = ChatOpenAI(temperature=0.5)
    memory = ConversationBufferMemory()
    conversation = ConversationChain(
        prompt=prompt,
        llm=llm,
        memory=memory,
        verbose=False
    )
    return conversation
