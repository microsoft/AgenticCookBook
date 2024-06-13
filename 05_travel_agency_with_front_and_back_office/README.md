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

1. Importing Modules:
   - The code begins by importing the necessary modules: `AssistantAgent`, `UserProxyAgent`, and `Teachability` from the `autogen.agentchat.contrib.capabilities` package.
   - It also imports the `os` module.

2. Configuration:
   - The code defines a list called `config_list` which contains a dictionary with configuration details for the agents.
   - The dictionary includes information such as the model, API key, API type, base URL, and API version. These values are retrieved from environment variables using the `os.environ.get()` function.
   - The code also configures the `Settings` for `
