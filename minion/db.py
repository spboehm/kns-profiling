#!/usr/bin/python3
import pymongo
import os
import json
import logging
from bson import ObjectId, json_util
from dotenv import load_dotenv

load_dotenv()

db = pymongo.MongoClient("mongodb://%s:%s@%s:27017/" %
                         (os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST")))
minion_db = db[os.getenv("DB_DATABASE")]
simulations = minion_db[os.getenv("DB_COLL_SIMULATION")]
hosts = minion_db[os.getenv('DB_COLL_HOST')]
events = minion_db[os.getenv('DB_COLL_EVENT')]
results = minion_db[os.getenv('DB_COLL_RESULT')]


def insert_sim(sim):
    return str(simulations.insert_one(sim).inserted_id)


def get_sim(sim_id):
    return dump_json(simulations.find_one({"sim_id": sim_id}))


def insert_host(host):
    return str(hosts.insert_one(host).inserted_id)


def get_host(_id):
    return dump_json(hosts.find_one({"_id": ObjectId(str(_id))}))


def get_hosts_by_simulation_id(simulation_id):
    return dump_json(hosts.find({"simulation_id": simulation_id}))


def insert_event(event):
    return str(events.insert_one(event).inserted_id)


def get_event(_id):
    return dump_json(events.find_one({"_id": ObjectId(str(_id))}))


def get_event_by_correlation_id(correlation_id):
    return dump_json(events.find({"correlation_id": correlation_id}))


def get_event_by_event_type(event_type):
    return dump_json(events.find({"event_type": event_type}))


def get_events_by_host_ids_and_event_type(host_ids, event_type):
    return dump_json(events.find({"host_id": {"$in": host_ids}, "event_type": event_type}))


def get_event_oids_by_simulation_id_and_event_type(sim_id, event_type):
    sim_oid = get_sim(sim_id)['_id']['$oid']
    hosts = get_hosts_by_simulation_id(sim_oid)

    host_oids = []
    for h in hosts:
        host_oids.append(h['_id']['$oid'])

    events = get_events_by_host_ids_and_event_type(host_oids, event_type)

    event_oids = []
    for e in events:
        event_oids.append(e['_id']['$oid'])

    return event_oids


def get_all_events():
    return dump_json(events.find({}))


def insert_result(result):
    return str(results.insert_one(result).inserted_id)


def disconnect():
    logging.info('DB connection closed')
    db.close()


def dump_json(data):
    return json.loads(json_util.dumps(data))
