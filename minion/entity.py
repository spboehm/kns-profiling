import json
from enum import Enum


class Simulation:
    def __init__(self, sim_id, platform):
        self.sim_id = sim_id
        self.platform = platform

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict())


class Host:
    def __init__(self, simulation_id, hostname, role):
        self.simulation_id = simulation_id
        self.hostname = hostname
        self.role = role

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict())


class Event:
    def __init__(self, host_id, correlation_id, event_type, body, timestamp):
        self.host_id = host_id
        self.correlation_id = correlation_id
        self.event_type = event_type
        self.body = body
        self.timestamp = timestamp

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict())


class EventResponse:
    def __init__(self, correlation_id, event_type, payload):
        self.correlation_id = correlation_id
        self.event_type = event_type
        self.payload = payload

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict())


class EventType(Enum):
    # worker agent
    WORKER_AGENT_STARTED = 0
    START_SIMULATION_CPU = 1
    FINISHED_SIMULATION_CPU = 2
    START_SIMULATION_MEM = 3
    FINISHED_SIMULATION_MEM = 4
    START_SIMULATION_IO = 5
    FINISHED_SIMULATION_IO = 6
    WORKER_AGENT_STOPPED = 7
    # controller agent
    START_SIMULATION = 8
    STOP_SIMULATION = 9
    START_CONTAINER_PLATFORM = 10
    STOP_CONTAINER_PLATFORM = 11
    START_KNS_PLATFORM = 20
    FINISHED_START_KNS_PLATFORM = 21
    START_KNS_JOIN_NODES = 22
    FINISHED_START_KNS_JOIN_NODES = 23
    START_KNS_DEPLOYMENT = 24
    FINISHED_START_KNS_DEPLOYMENT = 25
    STOP_KNS_DEPLOYMENT = 26
    FINISHED_STOP_KNS_DEPLOYMENT = 27
    START_KNS_UNJOIN_NODES = 28
    FINISHED_KNS_UNJOIN_NODES = 29
    STOP_KNS_PLATFORM = 30
    FINISHED_STOP_KNS_PLATFORM = 31




