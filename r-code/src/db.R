if (!require('mongolite')){
  install.packages('mongolite')
}

library(mongolite)

db.connect <- function(db, collection) {
  return (mongo(db = db,
                collection = collection,
                url = paste("mongodb://", 
                            ifelse(nchar(Sys.getenv("MINION_MONGODB_USER")) > 0, Sys.getenv("MINION_MONGODB_USER"), "guest"), ":",
                            ifelse(nchar(Sys.getenv("MINION_MONGODB_PASSWORD")) > 0, Sys.getenv("MINION_MONGODB_PASSWORD"), "guest"), "@",
                            ifelse(nchar(Sys.getenv("MINION_MONGODB_HOST")) > 0, Sys.getenv("MINION_MONGODB_HOST"), "h11.pi.uni-bamberg.de"), ":",
                            ifelse(nchar(Sys.getenv("MINION_MONGODB_PORT")) > 0, Sys.getenv("MINION_MONGODB_PORT"), "27017"), "/?ssl=",
                            ifelse(nchar(Sys.getenv("MINION_MONGODB_SSL")) > 0, Sys.getenv("MINION_MONGODB_SSL"), "true"), sep=""),
                verbose = FALSE,
                options = ssl_options()))
}

db.disconnect <- function(connect) {
  connect$disconnect()
}

# simulations
simulations_coll <- db.connect("minion", "simulations")
# hosts
hosts_coll <- db.connect("minion", "hosts")
# events
events_coll <- db.connect("minion", "events")
# netdata
netdata_coll <- db.connect("netdata", "netdata_metrics")
# all collections
collections <- c(simulations_coll, hosts_coll, events_coll, netdata_coll)

get.simulation <- function(sim_id) {
  return (simulations_coll$find(query = paste("{\"sim_id\":","\"", sim_id, "\"","}", sep=""), 
                                fields = '{"_id":true, "sim_id":true, "platform":true}'))
}

get.hosts <- function(sim_oid) {
  return (hosts_coll$find(query = paste("{\"simulation_id\":","\"", sim_oid, "\"","}", sep=""), 
                          fields = '{"_id": true, "simulation_id": true, "hostname": true, "role": true}'))
}

get.events.by.hosts.oid <- function(sim_id, hosts_oid) {
  return (events_coll$find(query = paste("{\"host_id\":{\"$in\":", paste0("[",paste0("\"", paste(hosts_oid, collapse='","'), '"'), "]"), "}}", sep="")))
}

# pass timestamp_start and timestamp_end as numeric!
get.netdata.metrics <- function(hostname, chart_type, chart_family, chart_context, timestamp_start, timestamp_end) {
  return (netdata_coll$find(query = paste("{\"hostname\":", "\"", hostname, "\",",
                                          "\"chart_type\":", "\"", chart_type, "\",", 
                                          "\"chart_family\":", "\"", chart_family, "\",", 
                                          "\"chart_context\":", "\"", chart_context , "\",", 
                                          "\"timestamp\":{\"$gt\":", timestamp_start, ",", "\"$lt\":", timestamp_end, "}", "}", sep = ""), 
                            fields = '{"_id": false, "hostname": true, "chart_name": true, "units": true, "id": true, "value": true, "timestamp": true}'))
}

get.system.metrics <- function(sim_id, hosts, timestamp_start, timestamp_end) {
  system_cpu <- Reduce(rbind, lapply(hosts, function(x) {
    system_metrics <- get.netdata.metrics(x, "system", "cpu", "system.cpu", timestamp_start, timestamp_end)
  }))
  system_ram <- Reduce(rbind, lapply(hosts, function(x) {
    system_metrics <- get.netdata.metrics(x, "system", "ram", "system.ram", timestamp_start, timestamp_end)
  }))
  system_disk <- Reduce(rbind, lapply(hosts, function(x) {
    system_metrics <- get.netdata.metrics(x, "system", "disk", "system.io", timestamp_start, timestamp_end)
  }))
  system_disk_util <- Reduce(rbind, lapply(hosts, function(x) {
    system_metrics <- get.netdata.metrics(x, "disk_util", "sda", "disk.util", timestamp_start, timestamp_end)
  }))
  system_net <- Reduce(rbind, lapply(hosts, function(x) {
    system_metrics <- get.netdata.metrics(x, "system", "network", "system.net", timestamp_start, timestamp_end)
  }))
  return (list(system_cpu = system_cpu, system_ram = system_ram, system_disk = system_disk, system_disk_util = system_disk_util, system_net = system_net))
}