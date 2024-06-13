# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

# Import necessary modules
from autogen import AssistantAgent, UserProxyAgent
from autogen.agentchat.contrib.capabilities.teachability import Teachability
import os

# Define the configuration list with environment variables
config_list = [
    {
        "model": os.environ.get("AZURE_OPENAI_MODEL", ""),
        "api_key": os.environ.get("AZURE_OPENAI_KEY", ""),
        "api_type": "azure",
        "base_url": os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
        "api_version": os.environ.get("AZURE_OPENAI_API_VERSION", "")
    }
]

# Create an instance of AssistantAgent for a comedian
comedian = AssistantAgent(
    name="comedian",
    system_message="You are a professional comedian. You can tell jokes and entertain people.",
    description="This agent is a great comedian telling interesting and funny jokes.",
    llm_config={"config_list": config_list}
)

# Create an instance of Teachability for the comedian, this will allow the comedian to learn from interactions
teachability = Teachability(
    reset_db=False,
    path_to_db_dir="./comedian_assistant_experience",
    llm_config={"config_list": config_list}
)

# Add the Teachability capability to the comedian agent
teachability.add_to_agent(comedian)

# Create an instance of UserProxyAgent
user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution_config={"work_dir": "coding", "use_docker": False}
)

# Initiate a chat between the user_proxy and the comedian agent
user_proxy.initiate_chat(
    comedian,
    message="Tell me a joke about cats and ninjas."
)