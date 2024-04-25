## Command Procedure: show site-status

The show site-status command retrieves and displays the current status of the site and its associated resources.

## Execution Steps

1. **Retrieve site status from Redis (`cgw/SiteStatus` key):**
   - Attempt to fetch the current site status data from the Redis server using the specified key.

2. **Fallback to local file if Redis is unavailable:**
   - If communication with Redis fails, the command attempts to load the site status from the `site_status.json` file locally.

3. **Retrieve charging station status from Redis (`cgw/ChargingStationsStatus` key):**
   - Query the Redis server to obtain the current status of charging stations associated with the site.

4. **Fallback to local file for charging station status if Redis is unavailable:**
   - In case of Redis unavailability, the command loads the charging station status from the `charging_stations_status.json` file.

5. **Read DNS leases information:**
   - Utilize the `DnsmasqLeases` class to read and manage DNS leases information from the `/data/dnsmasq/dnsmasq.leases` file.

6. **Display combined site status:**
   - Combine the retrieved site status (either from Redis or local file) with DNS leases information and charging stations status.

## Error Handling

- **Redis Unavailability:**
  - If Redis is not reachable, the command gracefully handles the situation by falling back to local JSON files for status information retrieval.
  - It attempts to load the site status from the `site_status.json` file and the charging station status from the `charging_stations_status.json` file in such cases.

- **File and JSON Decoding Errors:**
  - Proper error handling is implemented for potential file not found errors (`FileNotFoundError`) or JSON decoding errors (`json.JSONDecodeError`).
  - Appropriate warning or error messages are printed to inform users about these issues and prevent unexpected behavior during execution.



# TerminalScreen Class

The `TerminalScreen` class provides a customizable terminal interface using the `prompt_toolkit` library. It allows for interactive command handling, output display, and running processes in separate threads within a terminal-like environment.

## Features

- **Customizable Layout**: Provides an interactive terminal layout with input and output fields.
- **Command Handling**: Supports setting a command handler function to process user inputs.
- **Thread Management**: Allows starting and stopping processes in separate threads.
- **Directory Command Completion**: Offers nested command completion based on directory structure.

## Installation

To use the `TerminalScreen` class, you need to have the `prompt_toolkit` library installed. You can install it using pip:

```
pip install prompt_toolkit
```
## Usage

```
from TerminalScreen import TerminalScreen

# Initialize TerminalScreen with a directory containing command files
terminal = TerminalScreen(cmds_dir="/path/to/commands")

# Set a command handler function
def handle_command(command):
    # Custom command handling logic here
    return "Command executed: " + command

terminal.set_command_handler(handle_command)

# Start the terminal interface
terminal.run()

```
## Features
- Supports custom command handling functions.
- Provides auto-completion for commands based on available files in the specified directory.
- Enables starting and managing background processes/threading from the terminal interface.

