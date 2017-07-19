#ifndef STRUCTURES
#define STRUCTURES
#include <string>
#include <map>

struct Server {
  std::string name; // name of server
  std::string ip_addr;// IPv4 address of server
  std::map<string> keys;// list of key:value pairs containing info about the server
};

struct Battery {
  std::string name; // name of battery
  std::string status; // status of battery (ie, charging, discharging, charged)
  std::string time_left; // time left for the battery to be available
  unsigned char charge; //charge of the battery, from 0 to 100 as a percentile
};

struct Sensor {
  std::string name; // name of sensor
  std::string type; // type of sensor (to aid in proper parsing of object)
  std::string value; // value of sensor
};

struct NetworkNode {
  std::string name; // name of network interface
  long uplink; // upload/uplink utilization
  long downlink; //download/downlink utilization
  short speed; // speed of the interface (ie, 10/100/1G)
  bool sw_centric; // switch centric or machine centric, true if switch centric
};

#endif /* STRUCTURES */
