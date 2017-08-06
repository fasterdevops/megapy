#!/usr/bin/python
'''
MegaPy - MegaCLI wrapper
'''
import sh
import os
import subprocess
import argparse

__version__ = 'MegaPy v.1'
__author__ = 'Riley - riley@fasterdevops.com'

MEGACLI_INSTALLATION_PATH = "/opt/MegaCli/"


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

    megadir = os.path.dirname(MEGACLI_INSTALLATION_PATH)

    def check_install(self):
        '''
        Checks if MegaCLI is installed.
        '''
        # RedHat Command to install imh-megapkg
        install_megacli = ['/usr/bin/yum',
                           'install',
                           'imh-megapkg',
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

    # Using subprocess to to run megadir with command
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
        View battery information
        :param enclosure - physical enclosure from view_enclosures()
        :param slot - slot of the enclosure
        '''
        command = self.start_rebuild_drive_command
        command[4] = '[' + enclosure + ',' + slot + ']'
        subprocess.Popen(self.megadir, command)

    def show_rebuild_drive(self, enclosure, slot):
        '''
        View battery information
        :param enclosure - physical enclosure from view_enclosures()
        :param slot - slot of the enclosure
        '''
        command = self.start_rebuild_drive_command
        command[4] = '[' + enclosure + ',' + slot + ']'
        subprocess.Popen(self.megadir, command)

    def rebuild_drive(self, enclosure, slot):
        '''
        View battery information
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


def parse_arguments():
    '''
    Parsing user arguments. Use -h to see available commands.
    '''
    parser = argparse.ArgumentParser(description=('A wrapper to make '
                                                  'MegaCLI commands more '
                                                  'user friendly and easier '
                                                  'to remember')
                                    )
    parser.add_argument('--enclosure',
                        help='View the servers enclosure information',
                        dest='encl'
                       )
    parser.add_argument('--physical',
                        help='View the servers physical drive information',
                        dest='phys'
                       )
    parser.add_argument('--vdrive',
                        help='View the servers virtual drive information',
                        dest='vdrive'
                       )
    parser.add_argument('--controller',
                        help='View the servers controller information',
                        dest='control'
                       )
    parser.add_argument('--basedir',
                        help='Specify the base directory where' +
                        'MegaCLI is installed.',
                        dest='basedir'
                       )
    return parser.parse_args()


def main():
    '''
    main function.
    Initilizing MegaCLI object,parsing arguments, and calling functions.
    '''

    # display version and parse arguments
    print __version__
    args = parse_arguments()

    # initialize MegaCLI object
    mega = MegaCLI()
    mega.check_install()

    if args.basedir:
        mega.set_basedir(args.basedir)

    if args.encl:
        mega.view_enclosures()
    if args.vdrive:
        mega.view_vdrive()

    if args.phys:
        mega.view_physical_drives()


if __name__ == '__main__':
    main()