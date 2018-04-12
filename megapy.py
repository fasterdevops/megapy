#!/usr/bin/python
'''
MegaPy - MegaCLI wrapper
A wrapper to make MegaCLI commands more user friendly and easier to remember
'''
import os
import subprocess
import argparse

__version__ = '0.1.1'
__author__ = 'Riley, Kolby'
__author_email__ = 'riley@fasterdevops.com, kolby@fasterdevops.com'

MEGACLI_INSTALLATION_PATH = "/opt/MegaRAID/"


class MegaCLI(object):
    '''
    MegaCLI wrapper
    Example Usage:
    >>> from megapy import MegaCLI
    >>> mega = MegaCLI()
    >>> mega.view_enclosures()
    >>>
    '''

    def check_install(self):
        '''Checks if MegaCLI is installed'''
       
        # If MegaCLI is not installed, prompt user to install
        if not os.path.exists(self.megadir):
            valid_input = False
            while not valid_input:
                install = raw_input(
                    'MegaCLI does not exist on this server.\n' +
                    'Would you like to install it now? (yes/no)\n' +
                    '> ').lower()
                if 'y' in install:
                    # RedHat command to install megapkg
                    install_megacli = '/usr/bin/yum install megacli -y'
                    subprocess.Popen(install_megacli.split(' '))
                    valid_input = True
                elif 'n' in install:
                    print('Closing....')
                    valid_input = True

    def __init__(self, megacli_dir=''):
        '''
        define program installation directory and commands
        :param megacli_dir - The installation directory of MegaCLI
        '''
        
        # set megacli_dir if provided
        if megacli_dir:
            # add trailing slash if not provided
            if megacli_dir[-1:] ! = '/':
                megacli_dir += '/'
            self.megadir = os.path.dirname(megacli_dir)
        else:
            self.megadir = os.path.dirname(MEGACLI_INSTALLATION_PATH)

        self.check_install()
        
        self.command = {
            'megaenc': 'MegaCli64 -EncInfo -aALL',
            'megaphys': 'MegaCli64 -Pdlist -aALL',
            'vdrive': 'MegaCli64 -LDInfo -Lall -aLL',
            'battery': 'MegaCli64 -AdpBbuCmd -aALL',
            'start_rebuild_drive': 'MegaCli64 -PDRbld -Start -PhysDrv [E:S] -aN',
            'stop_rebuild_drive': 'MegaCli64 -PDRbld -Stop -PhysDrv [E:S] -aN',
            'showprog_rebuild_drive': 'MegaCli64 -PDRbld -ShowProg -PhysDrv [E:S] -aN',
            'disable_alarm': 'MegaCli64 -AdpSetProp AlarmDsbl -aALL',
            'enable_alarm': 'MegaCli64 -AdpSetProp AlarmEnbl -aALL'}
        
        # add filepath to command
        for key, value, in self.command.items():
            self.command['key'] = (self.megadir + value).split(' ')

        def __repr__(self):
            return '<MegaPy MegaCLI object __repr__>'

    def view_enclosures(self):
        '''View the servers enclosure information'''
        subprocess.Popen(self.command['megaenc'])

    def view_physical_drives(self):
        '''View the servers physical drive information'''
        subprocess.Popen(self.command['megaphys'])

    def view_vdrive(self):
        '''View the servers virtual drive information'''
        subprocess.Popen(self.command['vdrive'])

    def battery_info(self):
        '''View battery information'''
        subprocess.Popen(self.command['battery'])

    def start_rebuild_drive(self, enclosure, slot):
        '''
        Start rebuilding drive
        :param enclosure - physical enclosure from view_enclosures()
        :param slot - slot of the enclosure
        '''
        command = self.command['start_rebuild_drive']
        command[4] = '[' + enclosure + ':' + slot + ']'
        subprocess.Popen(command)

    def stop_rebuild_drive(self, enclosure, slot):
        '''
        Stop drive rebuild
        :param enclosure - physical enclosure from view_enclosures()
        :param slot - slot of the enclosure
        '''
        command = self.command['stop_rebuild_drive']
        command[4] = '[' + enclosure + ',' + slot + ']'
        subprocess.Popen(command)

    def show_rebuild_drive(self, enclosure, slot):
        '''
        Show drive rebuild information
        :param enclosure - physical enclosure from view_enclosures()
        :param slot - slot of the enclosure
        '''
        command = self.command['showprog_rebuild_drive']
        command[4] = '[' + enclosure + ',' + slot + ']'
        subprocess.Popen(command)

    def rebuild_drive(self, enclosure, slot):
        '''
        Rebuild the drive
        :param enclosure - physical enclosure from view_enclosures()
        :param slot - slot of the enclosure
        '''
        self.start_rebuild_drive(enclosure, slot)
        self.stop_rebuild_drive(enclosure, slot)
        self.show_rebuild_drive(enclosure, slot)

    def set_basedir(self, megacli_dir):
        '''
        Set the base directory for MegaCLI
        :param megacli_dir - The installation directory of MegaCLI
        '''
        self.__init__(megadir = os.path.dirname(megacli_dir))

    def alarm_disable(self):
        '''Disable the alarm'''
        subprocess.Popen(self.command['disable_alarm_command'])

    def alarm_enable(self):
        '''Enable the alarm'''
        subprocess.Popen(self.command['self.enable_alarm_command'])


def parse_arguments():
    '''
    Parsing user arguments. Use -h to see available commands.
    Had to add 'action='store_true' to arguments not expecting any input.
    '''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-enclosure',
                        help='View the servers enclosure information',
                        dest='encl',
                        action='store_true')
    parser.add_argument('-physical',
                        help='View the servers physical drive information',
                        action='store_true',
                        dest='phys')
    parser.add_argument('-vdrive',
                        help='View the servers virtual drive information',
                        action='store_true',
                        dest='vdrive')
    parser.add_argument('-controller',
                        help='View the servers controller information',
                        action='store_true',
                        dest='control')
    parser.add_argument('-alarmoff',
                        help='Turn the alarm off',
                        action='store_true',
                        dest='off')
    parser.add_argument('-alarmon',
                        help='Turn the alarm off',
                        action='store_true',
                        dest='on')
    parser.add_argument('-basedir',
                        help='Specify the base directory where ' +
                        'MegaCLI is installed.',
                        dest='basedir')
    args = parser.parse_args()
    return args


def main():
    '''
    main function.
    Initilizing MegaCLI object,parsing arguments, and calling functions.
    '''

    # display version and parse arguments
    print('MegaPy ' + __version__)
    
    # initialize MegaCLI object
    mega = MegaCLI()
    args = parse_arguments()
    if args.basedir:
        mega.set_basedir(args.basedir)

    if args.phys:
        mega.view_physical_drives()

    if args.vdrive:
        mega.view_vdrive()

    if args.control:
        mega.view_physical_drives()

    if args.off:
        mega.alarm_disable()

    if args.on:
        mega.alarm_enable()

if __name__ == '__main__':
    main()
