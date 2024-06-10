# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from autogen import AssistantAgent, UserProxyAgent
import os

config_list = [
    {
        "model": "gpt-4o",
        "api_key": os.environ.get("AZURE_OPENAI_KEY", ""),
        "api_type": "azure",
        "base_url": os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    }
]

commedian = AssistantAgent(
    name= "commedian", 
    system_message= "You are a professional comedian. You can tell jokes and entertain people.", 
    description="This agent is a great comedian telling interesting and funny jokes." ,
    llm_config={"config_list": config_list})

user_proxy = UserProxyAgent(
    name= "user_proxy",
    code_execution_config={"work_dir": "coding", "use_docker": False}) 

user_proxy.initiate_chat(
    commedian, 
    message="Tell me a joke about cats and ninjas."
    )