from tabulate import tabulate
from datetime import datetime
from dnmasq_leases import DnsmasqLeases
from charging_stations_status import ChargingStationsStatus
from io import StringIO


class SiteStatus:
    """
    Represents the status of a site including charging stations, electric vehicles, and offline chargers.
    """

    def __init__(self, charging_stations: list, datetime: str, evs: list, offline_chargers: list) -> None:
        """
        Initialize SiteStatus object.

        Args:
            charging_stations (list): List of charging stations.
            datetime (str): Datetime of the status.
            evs (list): List of electric vehicles.
            offline_chargers (list): List of offline chargers.
        """
        self.action = "response"
        self.charging_stations = charging_stations
        self.datetime = datetime
        self.evs = evs
        self.offline_chargers = offline_chargers

    @classmethod
    def from_json(cls, json_data: dict) -> 'SiteStatus':
        """
        Create a SiteStatus object from JSON data.

        Args:
            json_data (dict): JSON data representing the site status.

        Returns:
            SiteStatus: The created SiteStatus object.
        """
        if json_data is None:
            # Return an empty SiteStatus if json_data is None
            return cls([], '', [], [])
        
        charging_stations = json_data.get('charging_stations', [])
        datetime = json_data.get('datetime', '')
        evs = json_data.get('evs', [])
        offline_chargers = json_data.get('offline_chargers', [])
        return cls(charging_stations, datetime, evs, offline_chargers)


    def display(self, dnsmasq_leases: DnsmasqLeases, charging_stations_status: ChargingStationsStatus) -> str:
        """
        Display the site status including chargers, connections, and electric vehicles.

        Args:
            dnsmasq_leases (DnsmasqLeases): Instance of DnsmasqLeases containing lease information.
            charging_stations_status (ChargingStationsStatus): Instance of ChargingStationsStatus containing charging station status.

        Returns:
            str: The formatted text displaying site status.
        """
        output = StringIO()

        print("Site Status:", file=output)
        print(f"Action: {self.action}", file=output)
        print(f"DateTime: {self.datetime}", file=output)

        online_chargers = {charger['id']: 'Online' for charger in self.charging_stations}
        offline_chargers = {charger['id']: 'OFFLINE' for charger in self.offline_chargers}

        # Update status for online chargers if they exist in offline chargers
        for charger_id in online_chargers.keys() & offline_chargers.keys():
            online_chargers[charger_id] = 'OFFLINE'

        all_chargers = sorted({**online_chargers, **offline_chargers}.items())

        if all_chargers:
            chargers_with_ip = []
            for charger_id, status in all_chargers:
                ip_address = charging_stations_status.get_ip_from_charger_id(charger_id)
                mac_address = dnsmasq_leases.get_mac_from_ip(ip_address)
                lease = dnsmasq_leases.get_lease_time_from_ip(ip_address)
                chargers_with_ip.append((charger_id, status, ip_address, mac_address, lease))

            print("\nChargers:", file=output)
            headers = ["ID", "Status", "IP", "MAC", "Leased until"]
            print(tabulate(chargers_with_ip, headers=headers, tablefmt="psql"), file=output)

        print("\nConnections:", file=output)
        print(charging_stations_status.display(), file=output)

        if self.evs:
            print("\nElectric Vehicles:", file=output)
            headers = ["ID", "Chg-ID", "Status", "Chg-Current", "Chg-Offer", "Chg-Fw.", "Sess.E", "Start Chg."]
            data = []
            for ev in self.evs:
                start_charging_time = ev.get('start_charging_time')
                formatted_time = "UNKNOWN"
                if start_charging_time is not None:
                    formatted_time = datetime.strptime(start_charging_time, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%y%m%d_%H%M")
                data.append([
                    ev.get('id'),
                    ev.get('charger_id'),
                    ev.get('status'),
                    ev.get('charge_current'),
                    ev.get('charge_offer'),
                    ev.get('charger_firmware'),
                    ev.get('session_energy_consumed'),
                    formatted_time
                ])
            print(tabulate(data, headers=headers, tablefmt="psql", stralign="left"), file=output)

        return output.getvalue()


class EV:
    """
    Represents an electric vehicle (EV) with its attributes and status.
    """

    def __init__(self, action, apd_state, charge_capability, charge_current, charge_offer,
                 charge_power, charger_firmware, charger_id, connector_id, discharge_capability,
                 discharge_current, discharge_offer, discharge_power, ev_suspended, ev_id,
                 meter_values_timestamp, plugin_time, rfid, session_energy_consumed,
                 session_energy_produced, soc, start_charging_time, status, total_energy_consumed,
                 total_energy_produced, transaction_ongoing) -> None:
        """
        Initialize EV object.

        Args:
            # Add type hints and descriptions here...
        """
        self.action = action
        self.apd_state = apd_state
        self.charge_capability = charge_capability
        self.charge_current = charge_current
        self.charge_offer = charge_offer
        self.charge_power = charge_power
        self.charger_firmware = charger_firmware
        self.charger_id = charger_id
        self.connector_id = connector_id
        self.discharge_capability = discharge_capability
        self.discharge_current = discharge_current
        self.discharge_offer = discharge_offer
        self.discharge_power = discharge_power
        self.ev_suspended = ev_suspended
        self.ev_id = ev_id
        self.meter_values_timestamp = meter_values_timestamp
        self.plugin_time = plugin_time
        self.rfid = rfid
        self.session_energy_consumed = session_energy_consumed
        self.session_energy_produced = session_energy_produced
        self.soc = soc
        self.start_charging_time = start_charging_time
        self.status = status
        self.total_energy_consumed = total_energy_consumed
        self.total_energy_produced = total_energy_produced
        self.transaction_ongoing = transaction_ongoing

    @classmethod
    def from_json(cls, json_data: dict) -> 'EV':
        """
        Create an EV object from JSON data.

        Args:
            json_data (dict): JSON data representing the electric vehicle.

        Returns:
            EV: The created EV object.
        """
        # Implement logic to create EV object from JSON data here...
        pass
