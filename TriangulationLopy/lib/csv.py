from   machine import SD
import os
import conf
import pycom

class CSV:
    #################################################################
    ###
    ### STATIC ATTRIBUTES
    ###

    EXTENTION   = ".txt"
    DELIMITER   = ","

    #################################################################
    ###
    ### STATIC PUBLIC METHODS
    ###

    @staticmethod
    def mount(path):
        """
            Mount the SD card.
        """
        if path not in os.listdir("/"):
            try:
                os.mount(SD(), "/" + path)
            except:
                return False
        return True

    @staticmethod
    def toString (var):
        """
            Convert a variable to be print into a CSV file.
        """
        if var is None:
            return ""
        elif isinstance(var, int) or isinstance(var, float):
            return str(var)
        elif isinstance(var, str):
            return "\"" + var + "\""
        elif isinstance(var, bool):
            return "1" if var else "0"

    @staticmethod
    def write(content, mount = conf.MOUNT, file = conf.DATA_FILE + EXTENTION, mode = "w", delimiter = DELIMITER):
        """
            Write the content into the csv file.
        """
        # Check if header is not empty
        if len(content) is 0:
            return
        # Write data
        with open("/" + mount + "/" + file, mode) as file:
            for data in content:
                file.write(CSV.toString(data) + delimiter)
            file.write('\n')

    @staticmethod
    def writeFromDictionnary(content, mount = conf.MOUNT, file = conf.DATA_FILE + EXTENTION, mode = "a", head = conf.HEADER, delimiter = DELIMITER):
        """
            Write content of the dictionnary into the csv file.
        """
        # Check if header is not empty
        if len(content) is 0:
            return
        # Write data
        with open("/" + mount + "/" + file, mode) as file:
            for title in head:
                file.write(CSV.toString(content[title]) + delimiter)
            file.write('\n')

    def writeData(data):
        """Write data in the SD card"""
        if mount(conf.MOUNT):
            if not conf.DATA_FILE + CSV.EXTENTION in os.listdir("/" + conf.MOUNT):
                write(conf.HEADER)
            if isinstance(data, list):
                write(data, mode = "a")
            elif isinstance(data, dict):
                writeFromDictionnary(data)

    @staticmethod
    def writeData2(mount = conf.MOUNT, file = conf.DATA_FILE, head = conf.HEADER, data = None):
        """Write data in the SD card"""
        if CSV.mount(mount):
            if head != None and not file in os.listdir("/" + mount):
                CSV.write(head)
            if isinstance(data, list):
                CSV.write(data, mount, file, mode = "a")
            elif isinstance(data, dict):
                CSV.writeFromDictionnary(data, mount, file)
