#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
Convert nrpe.config.jinja2 to shinken config
'''


import sys
import os


if len(sys.argv) < 2:
    sys.exit('USAGE: {0} nrpe_config'.format(sys.argv[0]))


FILE = sys.argv[1]


with open(FILE, 'rt') as f:
    lines = f.readlines()
    for l in lines:
        if 'command[' in l:
            name, cmd = l.split(']=')
            name = name[name.find('[') + 1:]
            cmd, params = cmd.split(' ',1)
            check_type = os.path.basename(cmd)
            sign = '!'
            description = 'TODO'
            if check_type == 'check_tcp':
                print '{0}:'.format(name)
                program_name = name.split('_')[0].title()
                print '  description: {0} Local Port'.format(program_name)
                print 

                name = 'REMOTE_PORT'
                description = '{0} Remote Port'.format(program_name)
            elif check_type == 'check_ping':
                sign = ''
            elif check_type == 'check_procs':
                description = '{0} Daemon'.format(name.split('_')[0].title())
                check_type = 'check_nrpe'

            print '{0}:'.format(name)
            print '  check: {0}{1}{2}'.format(check_type, sign, name)
            print '  description: {0}'.format(description)
            print '  {0}'.format(params)
