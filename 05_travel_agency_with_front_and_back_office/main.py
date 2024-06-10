# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from autogen import ConversableAgent
from autogen import GroupChat
from autogen import GroupChatManager
from autogen import register_function
from autogen.runtime_logging import start, stop
from autogen.agentchat.contrib.capabilities.teachability import Teachability
from llama_index.core import Settings
from llama_index.core.agent import ReActAgent
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.tools.wikipedia import WikipediaToolSpec
from llamaindex_conversable_agent import LLamaIndexConversableAgent
from tools.travel_tools import find_flights, book_flight, find_accomodations, book_accomodation, get_bookings, send_booking_email
import os

start(logger_type="sqlite")

# setup llamaindex
llm = AzureOpenAI(
    deployment_name= os.environ.get("AZURE_OPENAI_MODEL", ""),
    temperature=0.0,
    api_key= os.environ.get("AZURE_OPENAI_KEY", ""),
    azure_endpoint= os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
    api_version= os.environ.get("AZURE_OPENAI_API_VERSION", ""),
    )

embed_model = AzureOpenAIEmbedding(
    deployment_name= os.environ.get("AZURE_OPENAI_EMBEDDING_MODEL", ""),
    temperature=0.0,
    api_key= os.environ.get("AZURE_OPENAI_KEY", ""),
    azure_endpoint= os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
    api_version= os.environ.get("AZURE_OPENAI_API_VERSION", ""),
    )

Settings.llm = llm
Settings.embed_model = embed_model


# setup autogen

config_list = [
    {
        "model": os.environ.get("AZURE_OPENAI_MODEL", ""),
        "api_key": os.environ.get("AZURE_OPENAI_KEY", ""),
        "api_type": "azure",
        "base_url": os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
        "api_version": os.environ.get("AZURE_OPENAI_API_VERSION", "")
    }
]

# create autogent agents
customer_proxy = ConversableAgent(
    "customer", 
    description="This the customer trying to book a trip, flights and accomodations.",
    human_input_mode="ALWAYS",
)

flight_assistant = ConversableAgent(
    "flight_booking_assistant",
    system_message="You help customers finding flights and booking them.  All retrieved information will be sent to the customer service which will present informations to the customer. Use the tool find_flights(origin='London', destination='Tokyo', date=2025-04-15) to find flights and book_flight(flight_name='Flight 01',origin='London', destination='Tokyo',  departure_date=2025-04-15, passengers=1) to book a flight.", 
    description="This agent helps customers find flights and book them. It can use external resources to provide more details.",
    llm_config={"config_list": config_list},
    # human_input_mode="ALWAYS"
    )

terminal = ConversableAgent(
    "computer_terminal",
    description="This computer terminal can be used to execute tools like booking flight and accommodations.",
    )

accomodation_assistant = ConversableAgent(
    "accommodation_assistant",
    system_message="You help customers finding hotels and accomodations and booking them. When looking up accomodations, you can use external resources to provide more details. All retrieved information will be sent to the customer service which will present informations to the customer. use find_accomodations(location='Tokyo', date=2025-04-15) to find accomodations and book_accomodation(accomodation_name='Tokyo', check_in_date=2025-04-15, nights=3, guests=1) to book accomodation.", 
    description="This agent helps customers find accomodations and hotels and book them. It can use external resources to provide more details.",
    llm_config={"config_list": config_list},
    )


customer_assistant = ConversableAgent(
    "customer_service",
    system_message="You handle all the final comunication, sending booking confirmamtions and other details. You can access the current customer bookings details and use them in email and communications. use get_bookings() to get the bookings and send_booking_email(email='customer@domain.com', booking_details = \{\}) to send an email with booking details. As you learn more about the customers and their booking habits, you can use this information to provide better service.", 
    description="This agent handles all the final communication with the customer, sending booking confirmations and other details. To do this, it can access the current customer bookings details and bookings and use them in email and communications.",
    llm_config={"config_list": config_list},
    )

teachability = Teachability(
    reset_db=True, 
    path_to_db_dir="./customer_assistant_experience",
    llm_config={"config_list": config_list})

teachability.add_to_agent(customer_assistant)

# register functions with autogen

register_function(
    find_flights,
    executor=terminal,
    caller=flight_assistant,
    name="find_flights",
    description="A tool for finding flight options between two locations. usage find_flights(origin='London', destination='Tokyo', date=2025-04-15) to find flights.",
    )

register_function(
    book_flight,
    executor=customer_proxy,
    caller=flight_assistant,
    name="book_flight",
    description="A tool for booking flights between two locations. use book_flight(flight_name='Flight 01',origin='London', destination='Tokyo',  departure_date=2025-04-15, passengers=1) to book a flight.",
    )

register_function(
    find_accomodations,
    executor=terminal,
    caller=accomodation_assistant,
    name="find_accomodations",
    description="A tool for finding accomodation options in a location. use find_accomodations(location='Tokyo', date=2025-04-15) to find accomodations.",
    
)

register_function(
    book_accomodation,
    executor=customer_proxy,
    caller=accomodation_assistant,
    name="book_accomodation",
    description="A tool for booking accomodation. use book_accomodation(accomodation_name='Tokyo', check_in_date=2025-04-15, nights=3, guests=1) to book accomodation.",
    )

register_function(
    get_bookings,
    executor=terminal,
    caller=customer_assistant,
    name="get_bookings",
    description="Retrieves the current bookings for the customer. call get_bookings() to get the bookings.",
)

register_function(
    send_booking_email,
    executor=terminal,
    caller = customer_assistant,
    name="send_booking_email",
    description="A tool for sending booking confirmation emails, call send_booking_email(email=dd@cp.com, booking_details = \{\}) to send an email with booking details.",
    )

# create a react agent to use wikipedia tool
wiki_spec = WikipediaToolSpec()
# Get the search wikipedia tool
wikipedia_tool = wiki_spec.to_tool_list()[1]

location_specialist = ReActAgent.from_tools(
    tools=[wikipedia_tool], 
    llm=llm,
    max_iterations=30,
    verbose=True)

# create an autogen agent using the react agent
trip_assistant = LLamaIndexConversableAgent(
    "trip_specialist",
    llama_index_agent=  location_specialist,
    system_message="You help customers finding more about places they would like to visit. You can use external resources to provide mroe details as you engage with the customer.",
    description="This agents helps customers discover locations to visit, things to do, and other details about a location. It can use external resources to provide more details. This agent helps in finding attractions, history and all that there si to know abotu a place",
)

# create a group chat
group_chat = GroupChat(
    agents=[customer_proxy, flight_assistant, accomodation_assistant, trip_assistant, customer_assistant, terminal],
    messages=[],
    max_round=100,
    send_introductions=False,
    speaker_transitions_type="disallowed",
    allowed_or_disallowed_speaker_transitions={
        terminal: [customer_proxy],
        customer_proxy: [terminal],
    },
)

group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": config_list},
    # human_input_mode="ALWAYS"
)

chat_result = customer_proxy.initiate_chat(
    group_chat_manager,
    # message="I would like to visit tokyo on the 15th of April 2025. Can you help me find flights and accomodations? I will be departing from London, just me and Tara. We will need a return flight too. ",
    message="What are the most important thigns to see in tokyo if you like video games?",
    summary_method="reflection_with_llm",
)

stop()