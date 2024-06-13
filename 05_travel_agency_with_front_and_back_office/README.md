# Travel Agency front and back office

This example is based on a Travel Agency scenario.

The code [main.py](main.py) sets up a conversation between a customer and the fron office agents: a `Customer Assistant` agent and a `Trip Specialist` agent. 
The front office agents work with back office (`Accommodation Booking Assistant`, `Activities Booking Assistant`, and `Flight Booking Assistant`) to create the pacakge for the customer.
Front office and back office can use the terminal to perform various operations:
 * find flights
 * book flights
 * find accomodations
 * book accomodations
 * find tickets for activites
 * book tickets
 * retrieve current bookings for the customer
 * email the final bookings back to the customer

Let's break down the code step by step:

1. Import Statements: 
    - The script begins by importing necessary modules and classes from various packages. These include tools for creating conversational agents, handling group chats, registering functions, and integrating with Azure OpenAI services.

2. Setup Azure OpenAI Models: 
    - It initializes two Azure OpenAI models - one for generating responses (llm) and another for embeddings (embed_model). The models are configured with parameters such as deployment name, temperature, API key, endpoint, and version, fetched from environment variables.

3. Configuration for Conversational Agents: 
    - A configuration list (config_list) is defined with details required to interact with the Azure OpenAI API, including model, API key, base URL, and API version.

4. Creation of Conversational Agents: 
    - Several ConversableAgent instances are created for different roles within the travel agency system, such as:
        - `customer proxy`
        - Front office :
            - `customer assistant`
            - `trip specialist assistant`
        - Back office    
            - `flight booking assistant`
            - `accommodation booking assistant`
            - `activities booking assistant`
        - `terminal for executing tools`

5. Teachability Feature: 
    - The Teachability capability is added to the `customer assistant` and `trip specialist assistant agents`, allowing them to learn from interactions and improve over time.

6. Tool Registration: 
    - Functions for :finding and booking flights, accommodations, and attraction tickets are registered with the appropriate agents using register_function. This step links the conversational agents with the actual functionalities they are supposed to handle.

7. Group Chat Setup: 
    - A `GroupChat` instance is created, including all the agents involved in the system. This setup defines how agents can communicate within the system, specifying allowed speaker transitions to control the flow of conversation.

8. Group Chat Manager: 
    - A `GroupChatManager` is instantiated to manage the group chat, equipped with the configuration for interacting with the Azure OpenAI API.

9. Initiating a Chat: 
    - Finally, the script initiates a chat session through the `customer proxy agent`, simulating a customer's request to book a travel package. The conversation is managed by the group chat manager.
