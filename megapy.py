#!/usr/bin/python
'''
MegaPy - MegaCLI wrapper
'''
import os
import subprocess
import argparse

__version__ = 'MegaPy v.1'
__author__ = 'Riley - riley@fasterdevops.com'

MEGACLI_INSTALLATION_PATH = "/opt/MegaRAID/"


class MegaCLI(object):
    '''
    MegaCLI wrapper
    Example Usage:
    >>> from megapy import MegaCLI
    >>> mega = MegaCLI()
    >>> mega.check_install()
    >>> mega.view_enclosures()
    >>>
    '''
    # pylint: disable=too-many-instance-attributes
    megadir = os.path.dirname(MEGACLI_INSTALLATION_PATH)

    def check_install(self):
        '''
        Checks if MegaCLI is installed.
        '''
        # RedHat Command to install imh-megapkg
        install_megacli = ['/usr/bin/yum',
                           'install',
                           'megacli',
                           '-y']
        # If MegaCLI is not installed, prompt user
        # to see if they would like to install
        if not os.path.exists(self.megadir):
            valid_input = False
            while not valid_input:
                install = raw_input('MegaCLI does not exist on this' +
                                    'server!\n' +
                                    ' Would you like' +
                                    'to install it now?(yes/no): ').lower()
                if install in ('yes', 'y'):
                    subprocess.Popen(install_megacli)
                    valid_input = True
                if install in ('no', 'n'):
                    print('Closing....')
                    valid_input = True

    def __init__(self, megacli_dir=''):
        '''
        define program installation directory and commands
        :param megacli_dir - The installation directory of MegaCLI
        '''
        # If user supplies different installation path,
        # use the installation path
        if megacli_dir is not '':
            self.megadir = os.path.dirname(megacli_dir)
        self.megaenc_command = ['MegaCli64',
                                '-EncInfo',
                                '-aALL']
        self.megaphys_command = ['MegaCli64',
                                 '-Pdlist',
                                 '-aALL']
        self.vdrive_command = ['MegaCli64',
                               '-LDInfo',
                               '-Lall',
                               '-aLL']
        self.battery_command = ['MegaCli64',
                                '-AdpBbuCmd',
                                '-aALL']
        self.start_rebuild_drive_command = ['MegaCli64',
                                            '-PDRbld',
                                            '-Start',
                                            '-PhysDrv',
                                            '[E:S]',
                                            '-aN']
        self.stop_rebuild_drive_command = ['MegaCli64',
                                           '-PDRbld',
                                           '-Stop',
                                           '-PhysDrv',
                                           '[E:S]',
                                           '-aN']
        self.showprog_rebuild_drive_command = ['MegaCli64',
                                               '-PDRbld',
                                               '-ShowProg',
                                               '-PhysDrv',
                                               '[E:S]',
                                               '-aN']
        self.disable_alarm_command = ['MegaCli64',
                                      '-AdpSetProp',
                                      'AlarmDsbl',
                                      '-aALL']
        self.enable_alarm_command = ['MegaCli64',
                                     '-AdpSetProp',
                                     'AlarmEnbl',
                                     '-aALL']

    def view_enclosures(self):
        '''
        View the servers enclosure information
        '''
        subprocess.Popen(self.megadir, self.megaenc_command)

    def view_physical_drives(self):
        '''
        View the servers physical drive information
        '''
        subprocess.Popen(self.megadir, self.megaphys_command)

    def view_vdrive(self):
        '''
        View the servers virtual drive information
        '''
        subprocess.Popen(self.megadir, self.vdrive_command)

    def battery_info(self):
        '''
        View battery information
        '''
        subprocess.Popen(self.megadir, self.battery_command)

    def start_rebuild_drive(self, enclosure, slot):
        '''
        Start rebuilding drive
        :param enclosure - physical enclosure from view_enclosures()
        :param slot - slot of the enclosure
        '''
        command = self.start_rebuild_drive_command
        command[4] = '[' + enclosure + ',' + slot + ']'
        subprocess.Popen(self.megadir, command)

    def stop_rebuild_drive(self, enclosure, slot):
        '''
        Stop drive rebuild
        :param enclosure - physical enclosure from view_enclosures()
        :param slot - slot of the enclosure
        '''
        command = self.start_rebuild_drive_command
        command[4] = '[' + enclosure + ',' + slot + ']'
        subprocess.Popen(self.megadir, command)

    def show_rebuild_drive(self, enclosure, slot):
        '''
        Show drive rebuild information
        :param enclosure - physical enclosure from view_enclosures()
        :param slot - slot of the enclosure
        '''
        command = self.start_rebuild_drive_command
        command[4] = '[' + enclosure + ',' + slot + ']'
        subprocess.Popen(self.megadir, command)

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
        self.megadir = os.path.dirname(megacli_dir)

    def alarm_disable(self):
        '''
        Disable the alarm
        '''
        subprocess.Popen(self.megadir, self.disable_alarm_command)

    def alarm_enable(self):
        '''
        Enable the alarm
        '''
        subprocess.Popen(self.megadir, self.enable_alarm_command)


def parse_arguments():
    '''
    Parsing user arguments. Use -h to see available commands.
    Had to add 'action='store_true' to arguments not expecting any input.
    '''
    parser = argparse.ArgumentParser(description='A wrapper to make ' +
                                     'MegaCLI commands more' +
                                     'user friendly and easier' +
                                     'to remember')
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
    print __version__
    # initialize MegaCLI object
    mega = MegaCLI()
    mega.check_install()
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
