#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    python 3 script to convert JBoss/Wildfly user properties list to
    hashcat mode 20 by @_EthicalChaos_

    Usage:
        python jbosswidlyfly_to_hashcat.py --userlist mgmt-users.properties > jbosswildfly.hashes
        hashcat -O -m 20 --username --hex-salt jbosswildfly.hashes rockyou.txt
"""

import re
import binascii
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--userlist", help="JBoss/Wilfly user properties file containing hashes")
parser.add_argument("--realm", default="ManagementRealm", nargs='?')
args = parser.parse_args()

hash_format = r'^(.*)=([a-f0-9]{32})\s*$'

users_file = open(args.userlist, 'r')
lines = users_file.readlines()

for line in lines:
    result = re.search(hash_format, line.strip())
    if result is not None:
        print('%s:%s:%s' % (result.group(1),
                            result.group(2),
                            binascii.hexlify(bytes(result.group(1) + ':' + args.realm + ':', 'utf-8')).decode('utf-8')))
