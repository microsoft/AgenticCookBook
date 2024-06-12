# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from autogen import AssistantAgent, UserProxyAgent
from autogen.agentchat.contrib.capabilities.teachability import Teachability
import os

config_list = [
    {
        "model": os.environ.get("AZURE_OPENAI_MODEL", ""),
        "api_key": os.environ.get("AZURE_OPENAI_KEY", ""),
        "api_type": "azure",
        "base_url": os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
        "api_version": os.environ.get("AZURE_OPENAI_API_VERSION", "")
    }
]

comedian = AssistantAgent(
    name= "comedian", 
    system_message= "You are a professional comedian. You can tell jokes and entertain people.", 
    description="This agent is a great comedian telling interesting and funny jokes." ,
    llm_config={"config_list": config_list})

teachability = Teachability(
    reset_db=False, 
    path_to_db_dir="./comedian_assistant_experience",
    llm_config={"config_list": config_list})

teachability.add_to_agent(comedian)

user_proxy = UserProxyAgent(
    name= "user_proxy",
    code_execution_config={"work_dir": "coding", "use_docker": False}) 

user_proxy.initiate_chat(
    comedian, 
    message="Tell me a joke about cats and ninjas."
    )