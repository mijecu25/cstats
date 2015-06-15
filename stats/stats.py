import sys as system

__author__ = 'Miguel Velez'


# Main method
def main(args):
    print
    print 'stats provides statistic and information about your directory'

    # Check if the user entered any arguments
    if len(args) == 0:
        pass
    else:
        # Loop through the arguments
        for arg in args:
            print arg

# Start the program
if __name__ == '__main__':
    main(system.argv[1:])
