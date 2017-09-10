# stat3 Network Protocol

## Table of Contents

1. Reserved Characters
2. Protocol Formatting
   * Port Numers
   * Server Packets
   * Battery Packets
   * Sensor Packets
   * Network Packets
3. Future Notes

## 1. Reserved Characters

The following list of characters is not to be used:

```
| ` , (space character)
```

The reason they are not to be used is because of formatting characters used in the program.

Also worth noting, all ```_``` characters are replaced with spaces in the server application automatically

## 2. Protocol Formatting

### Port Numbers

* Server Port: ```2204```
* Battery Port: ```2205```
* Sensor Port: ```2206```
* Network Port: ```2207```


#### Server Packets

Servers give data which only has key, value pairs. The server name is determined from the IP address in this case

```
(key) | (data)
```

#### Battery Packets

Batteries only give data which has name, percent, and time left tupples.

```
(name) | (percent) | (timeleft)
```

* ```name``` - string of battery name
* ```percent``` - float number (from 0 to 100) of battery percentage
* ```timeleft``` - string of battery time left string

#### Sensor Packets

Sensors give data which has name, value, and optionally type pairs

If no type is specified, ```RAW``` is defaulted

```
(name) | (data) | [type]
```

* ```name``` - string of sensor name
* ```data``` - data of any type
* ```type``` - **Optional** string of sensor type (to be parsed per **Sensor Types**)

##### Sensor Types

* ```RAW``` - integer
* ```THERMAL``` - Degrees F
* ```BOOLEAN``` - True or False
* ```IBOOLEAN``` - True or False (to be inverted in server application)

#### Network Packets

Network Packets give data which has a name, upload, and download tupple

```
(name) | (upload) | (downlaod)
```

* ```name``` - string of sensor name
* ```upload``` - float number from 0 to 100
* ```download``` - float number from 0 to 100

## 3. Future Notes

TCP operation is used mostly for connections with servers that cannot be contacted over UDP

UDP is the main port to be used for most traffic.

Encrypted traffic is planned for the future. Multiple packets may be handled in a single stream? Unsure how to handle this, but may be more efficient to not do single short RSA conneciton due to computational expenses.
