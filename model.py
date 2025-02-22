# ======================================== Libs =================================
# from langchain_deepseek import ChatDeepSeek
from langgraph.graph import MessagesState, StateGraph
import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import END
from langchain_openai import ChatOpenAI
from script import run_bash_script

# ======================================== Variables ============================
load_dotenv()
# llm = ChatDeepSeek(model='deepseek-chat', temperature=0)
llm = ChatOpenAI(model='gpt-4o-mini', timeout=120)
graph_builder = StateGraph(MessagesState)
script_result = []
commands = []
feedbacks = []
count = 0
# ======================================== Functions ============================
def load_tmpl(file_path):
    """Loading prompts from a template file"""
    with open(file_path, 'r') as file:
        content = file.read()
    return content


GENERATOR_PROMPT = load_tmpl("templates/generator_prompt.tmpl")
VALIDATION_PROMPT = load_tmpl("templates/validation_prompt.tmpl")
SUMMARY_PROMPT = load_tmpl("templates/summary.tmpl")


async def command_generator(state: MessagesState):
    """Generating command for bash script"""
    global feedbacks, commands
    if len(feedbacks) > 0:
        prompt = [SystemMessage(GENERATOR_PROMPT + "\nFeedbacks: " + "\n".join(feedbacks)
                                + "Commands which was used and doesn't work: "
                                + "\n".join(commands))] + state["messages"]
    else:
        prompt = [SystemMessage(GENERATOR_PROMPT)] + state["messages"]
    response = await llm.ainvoke(prompt)
    print(response.content)
    return {"messages": [response]}

async def command_validation(state: MessagesState):
    """Validating command for bash script is the command is right or using necessary libs"""
    prompt = [SystemMessage(VALIDATION_PROMPT)] + state["messages"]
    response = llm.invoke(prompt)
    if response.content != "is_valid":
        global feedbacks
        feedbacks.append(response.content)
    print(response.content)
    return {"messages": [response]}

async def input_output(state: MessagesState):
    """Executing bash script
         Creating bash script file, if it doesn't exist it will be created
         if already exists it will be removed and created new
         Using docker to execute bash script
         if it doesn't response to user request it gives feedback
    """
    global script_result, count, commands
    bash_script = "/app/my_script.sh"
    if os.path.exists(bash_script):
        os.remove(bash_script)
        print("Old bash script removed, in order to create new bash script")
    else:
        print("There is no old bash script")

    commands.append(state["messages"][-2].dict()["content"])
    try:
        with open(bash_script, "w") as file:
            file.write("#!/bin/bash\n")
            file.write(commands[-1] + "\n")
        print(f"Bash-script '{bash_script}' successfully created.")
        script_result.append(await run_bash_script(bash_script))
        prompt = ([SystemMessage("Check executed command: " + script_result[-1]
                                 + "if execution result validate to user"
                                   "intend answer: 'is_aligned'"
                                   "otherwise give an alignment feedback.")]
                  + [state["messages"][0]])
    except Exception as e:
        print(f"Error while creating a script: {e}")
        prompt = ([SystemMessage("Check executed command: " + f"Error while creating a script: {e}"
                                 + "if execution result validate to user"
                                   "intend answer: 'is_aligned'"
                                   "otherwise give an alignment feedback.")]
                  + [state["messages"][0]])

    response = await llm.ainvoke(prompt)
    if count > 0 and response.content != "is_aligned":
        response = HumanMessage("is_aligned")
    if response.content != "is_aligned":
        global feedbacks
        feedbacks.append(response.content)
        count += 1
    print(response.content)
    return {"messages": [response]}


async def output_wrapping(state: MessagesState):
    """If all steps response to users query we generate summary"""
    global script_result, count, commands
    prompt = ([SystemMessage(SUMMARY_PROMPT)]+state["messages"] + ["Bash scripts which used: "] + commands
              + ["Results of running scripts: "] + script_result)
    response = await llm.ainvoke(prompt)
    count = 0
    commands, script_result = [], []
    print(response.content)
    return {"messages": [response]}


graph_builder.add_node("command_generator", command_generator)
graph_builder.add_node("command_validation", command_validation)
graph_builder.add_node("input_output", input_output)
graph_builder.add_node("output_wrapping", output_wrapping)
graph_builder.set_entry_point("command_generator")
graph_builder.add_conditional_edges("command_validation",
                                    lambda state: "input_output" if "is_valid"
                                    in state["messages"][-1].dict()["content"]
                                    else "command_generator",
                                    )
# Checking output of last state if AI respond is_valid it goes to the next step otherwise regenerates with feedback
graph_builder.add_conditional_edges("input_output",
                                    lambda state: "output_wrapping" if "is_aligned"
                                    in state["messages"][-1].dict()["content"]
                                    else "command_generator",
                                    )
# Checking output of last state if AI respond is_aligned it goes to the next step otherwise regenerates with feedback
graph_builder.add_edge("command_generator", "command_validation")
graph_builder.add_edge("output_wrapping", END)
graph = graph_builder.compile()
