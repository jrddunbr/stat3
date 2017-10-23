from easysnmp import snmp_get, snmp_set, snmp_walk

# Perform an SNMP walk
system_items =  snmp_walk(u'.1.3.6.1.2.1', hostname='128.153.145.20', community='cacti', version=1)



# Each returned item can be used normally as its related type (str or int)
# but also has several extended attributes with SNMP-specific information
for item in system_items:
    print ('{oid}.{oid_index} {snmp_type} = {value}'.format(
        oid=item.oid,
        oid_index=item.oid_index,
        snmp_type=item.snmp_type,
        value=item.value
    ))
