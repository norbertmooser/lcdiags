import json
from tabulate import tabulate

class CgwConfig:
    def __init__(self, charging_stations, cpo_backend_url, grid_connection, new_phase_rotation_logic, payload_version, rfids, schema_version, settings, site_id):
        self.charging_stations = charging_stations
        self.cpo_backend_url = cpo_backend_url
        self.grid_connection = grid_connection
        self.new_phase_rotation_logic = new_phase_rotation_logic
        self.payload_version = payload_version
        self.rfids = rfids
        self.schema_version = schema_version
        self.settings = settings
        self.site_id = site_id

    @classmethod
    def from_json(cls, json_data):
        return cls(
            charging_stations=[ChargingStation.from_json(cs) for cs in json_data["charging_stations"]],
            cpo_backend_url=json_data["cpo_backend_url"],
            grid_connection=json_data["grid_connection"],
            new_phase_rotation_logic=json_data["new_phase_rotation_logic"],
            payload_version=json_data["payload_version"],
            rfids=json_data["rfids"],
            schema_version=json_data["schema_version"],
            settings=json_data["settings"],
            site_id=json_data["site_id"]
        )

    def to_json(self):
        return {
            "charging_stations": [cs.to_json() for cs in self.charging_stations],
            "cpo_backend_url": self.cpo_backend_url,
            "grid_connection": self.grid_connection,
            "new_phase_rotation_logic": self.new_phase_rotation_logic,
            "payload_version": self.payload_version,
            "rfids": self.rfids,
            "schema_version": self.schema_version,
            "settings": self.settings,
            "site_id": self.site_id
        }


        
    def display(self):
        sorted_stations = sorted(self.charging_stations, key=lambda x: x.id)
        data = []
        for station in sorted_stations:
            connectors_info = "\n".join([f"{c.capability}" for c in station.connectors])
            connectors_phase_mapping = "\n".join([f"{c.phase_mapping}" for c in station.connectors])
            data.append([station.id, station.type, connectors_info, station.lowest_acceptable_current, station.lowest_acceptable_offer,connectors_phase_mapping])
        
        headers = ["Name", "Type", "Conn. cap", "lac", "lao", "phase map"]
        print(tabulate(data, headers=headers, tablefmt="psql"))

        
    def display_rfids(self):
        data = []
        for rfid in sorted(self.rfids, key=lambda x: x["name"]):
            data.append([rfid["name"], rfid["identifier"]])
        
        headers = ["Name", "Identifier"]
        print(tabulate(data, headers=headers, tablefmt="psql"))

      


class ChargingStation:
    def __init__(self, connectors, current_type, efficiency, firmware_version, id, ip_address, lowest_acceptable_current, lowest_acceptable_offer, manual_phase_rotation, name, ocpp_interface, ocpp_tls, parent_fuse, plug_count, type, uuid):
        self.connectors = connectors
        self.current_type = current_type
        self.efficiency = efficiency
        self.firmware_version = firmware_version
        self.id = id
        self.ip_address = ip_address
        self.lowest_acceptable_current = lowest_acceptable_current
        self.lowest_acceptable_offer = lowest_acceptable_offer
        self.manual_phase_rotation = manual_phase_rotation
        self.name = name
        self.ocpp_interface = ocpp_interface
        self.ocpp_tls = ocpp_tls
        self.parent_fuse = parent_fuse
        self.plug_count = plug_count
        self.type = type
        self.uuid = uuid

    @classmethod
    def from_json(cls, json_data):
        return cls(
            connectors=[Connector.from_json(connector) for connector in json_data["connectors"]],
            current_type=json_data["current_type"],
            efficiency=json_data["efficiency"],
            firmware_version=json_data["firmware_version"],
            id=json_data["id"],
            ip_address=json_data["ip_address"],
            lowest_acceptable_current=json_data["lowest_acceptable_current"],
            lowest_acceptable_offer=json_data["lowest_acceptable_offer"],
            manual_phase_rotation=json_data["manual_phase_rotation"],
            name=json_data["name"],
            ocpp_interface=json_data["ocpp_interface"],
            ocpp_tls=json_data["ocpp_tls"],
            parent_fuse=json_data["parent_fuse"],
            plug_count=json_data["plug_count"],
            type=json_data["type"],
            uuid=json_data["uuid"]
        )

    def to_json(self):
        return {
            "connectors": [connector.to_json() for connector in self.connectors],
            "current_type": self.current_type,
            "efficiency": self.efficiency,
            "firmware_version": self.firmware_version,
            "id": self.id,
            "ip_address": self.ip_address,
            "lowest_acceptable_current": self.lowest_acceptable_current,
            "lowest_acceptable_offer": self.lowest_acceptable_offer,
            "manual_phase_rotation": self.manual_phase_rotation,
            "name": self.name,
            "ocpp_interface": self.ocpp_interface,
            "ocpp_tls": self.ocpp_tls,
            "parent_fuse": self.parent_fuse,
            "plug_count": self.plug_count,
            "type": self.type,
            "uuid": self.uuid
        }


class Connector:
    def __init__(self, capability, charger_id, connector_id, efficiency, fallback_value, id, lowest_acceptable_current, lowest_acceptable_offer, phase_mapping, priority, uuid):
        self.capability = capability
        self.charger_id = charger_id
        self.connector_id = connector_id
        self.efficiency = efficiency
        self.fallback_value = fallback_value
        self.id = id
        self.lowest_acceptable_current = lowest_acceptable_current
        self.lowest_acceptable_offer = lowest_acceptable_offer
        self.phase_mapping = phase_mapping
        self.priority = priority
        self.uuid = uuid

    @classmethod
    def from_json(cls, json_data):
        return cls(
            capability=json_data["capability"],
            charger_id=json_data["charger_id"],
            connector_id=json_data["connector_id"],
            efficiency=json_data["efficiency"],
            fallback_value=json_data["fallback_value"],
            id=json_data["id"],
            lowest_acceptable_current=json_data["lowest_acceptable_current"],
            lowest_acceptable_offer=json_data["lowest_acceptable_offer"],
            phase_mapping=json_data["phase_mapping"],
            priority=json_data["priority"],
            uuid=json_data["uuid"]
        )

    def to_json(self):
        return {
            "capability": self.capability,
            "charger_id": self.charger_id,
            "connector_id": self.connector_id,
            "efficiency": self.efficiency,
            "fallback_value": self.fallback_value,
            "id": self.id,
            "lowest_acceptable_current": self.lowest_acceptable_current,
            "lowest_acceptable_offer": self.lowest_acceptable_offer,
            "phase_mapping": self.phase_mapping,
            "priority": self.priority,
            "uuid": self.uuid
        }



# Load JSON data from file
file_path = 'cgw_config.json'
with open(file_path, 'r') as file:
    json_data = json.load(file)

# Convert JSON data to object
cgw_config = CgwConfig.from_json(json_data)

# Display the data using the display function
cgw_config.display()
cgw_config.display_rfids()
