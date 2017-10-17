# stat3

Stat3 is a new edition of manage2\* and a complete rewrite of the original Management v1.0

# Things to do:

## In the net folder:

* Create a program which can fetch data from COSI's Juniper EX4500 and TP link switches, and dump it into a CSV.
* Create multiple granularities of files from those CSV's: every 15 seconds for the day, every hour for the week, and quarterly for the year. Beyond that, we're not sure, but keeping that data should be small enough that it's not problematic.
* Render graphs based on these levels of data in MatPlotLib for nice looking graph images (rather this than Javascript/CSS based versions.

## In the server folder:

* Create a server to nab real-time data from servers
* Display the data collected on a webpage
* Collect data from battery backups
* Display this data, and use it to tell computers that they should shut down cleanly in the event of an outage longer than a set time.
* Send emails to service maintainers for when systemd scripts or other events occur, as configured

## In the web folder:

* visualization code for the server data as well as the network data. Perhaps we can also make some JS based graphs for the battery backups and servers, and make some cool metrics

## Other files hanging around:

### protocol.md:

Defines the network protocol used for the stat3 packets. They are basic yet extendable.


