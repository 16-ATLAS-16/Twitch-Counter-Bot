import sys

global Args, ValidArgs
Args = sys.argv[1:]
ValidArgs = ['-v',
            '-h',
            '--help',
            '--verbrose',
            '-V',
            '--silent',
            '--no-ui',
            '--new-process']


  