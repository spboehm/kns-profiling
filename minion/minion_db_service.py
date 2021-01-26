#!/usr/bin/env python

import argparse
import sys
import time
import uuid

import db
from entity import Simulation, Host, Event, EventType


def insert_sim(sim):
    return db.insert_sim(sim)


def insert_host(host):
    return db.insert_host(host)


def insert_event(event):
    return db.insert_event(event)


def get_event_oids_by_simulation_id_and_event_type(sim_id, event_type):
    return db.get_event_oids_by_simulation_id_and_event_type(sim_id, event_type)


def write_id_to_stdout(_str):
    sys.stdout.write(str(_str))
    sys.stdout.flush()
    sys.exit(0)


def write_uuid_to_stdout():
    write_id_to_stdout(uuid.uuid4())


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_simulation = subparsers.add_parser('simulation')
    parser_simulation.add_argument('--sim_id')
    parser_simulation.add_argument('--platform')
    parser_simulation.set_defaults(which='simulation')

    parser_host = subparsers.add_parser('host')
    parser_host.add_argument('--simulation_id')
    parser_host.add_argument('--hostname')
    parser_host.add_argument('--role')
    parser_host.set_defaults(which='host')

    parser_event = subparsers.add_parser('event')
    parser_event.add_argument('--host_id')
    parser_event.add_argument('--correlation_id')
    parser_event.add_argument('--event_type')
    parser_event.add_argument('--body')
    parser_event.set_defaults(which='event')

    parser_event_oids = subparsers.add_parser('simulation-event')
    parser_event_oids.add_argument('--sim_id')
    parser_event_oids.add_argument('--event_type')
    parser_event_oids.set_defaults(which='simulation-event')

    parser_uuid = subparsers.add_parser('uuid')
    parser_uuid.set_defaults(which='uuid')

    args = parser.parse_args()

    if args.which == "simulation":
        sim_oid = insert_sim(Simulation(args.sim_id, args.platform).to_dict())
        write_id_to_stdout(sim_oid)
    elif args.which == "host":
        host_oid = insert_host(Host(args.simulation_id, args.hostname, args.role).to_dict())
        write_id_to_stdout(host_oid)
    elif args.which == "event":
        event_oid = insert_event(Event(args.host_id, args.correlation_id, str(EventType(int(args.event_type))), args.body, time.time()).to_dict())
        write_id_to_stdout(event_oid)
    elif args.which == "simulation-event":
        event_oids = get_event_oids_by_simulation_id_and_event_type(args.sim_id, str(EventType(int(args.event_type))))
        write_id_to_stdout(str(event_oids))
    elif args.which == "uuid":
        write_uuid_to_stdout()
    else:
        raise ValueError("Command {} not found!".format(args.which))
