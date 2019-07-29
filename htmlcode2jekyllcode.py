#!/usr/bin/env python

import logging.config
import os, re

# Logging config
logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'logging.conf'))
# logger = logging.getLogger("logger_console_info")
logger = logging.getLogger("logger_console_debug")



# Global var
files_dir = "/Users/sgendrot/PycharmProjects/extract-to-jekyll"
# dict of html tag and number of repetition
tag_dic = {}


def analyze_jekyll_file(name):
    '''
    Analyze a jekyll file (read the file, change all html tags to jekyll tag)
    Used to find and count the html tags

    :param name: the name of the file
    :type name: basestring
    :return: xxxx
    '''
    jekyll_file = files_dir+"/"+name
    logger.info("Let process: %s" % jekyll_file)

    file_data = open(jekyll_file, "r").read()

    tags_extracted = re.findall("(<((/)?[a-z0-9]*)[^>]*>)", file_data)
    for atag in tags_extracted:
        # logger.debug("tags extracted: %s"% atag[1])
        if atag[1] is "":
            logger.debug("empty tag ???")
        if atag[1] in tag_dic:
            tag_dic[atag[1]] += 1
        else:
            tag_dic[atag[1]] = 1


def process_jekyll_file(name):
    '''
    Process a jekyll file (read the file, change all html tags to jekyll tag)
    Used to find and clean the html tags

    :param name: the name of the file
    :type name: basestring
    :return: xxxx
    '''
    jekyll_file = files_dir+"/"+name
    logger.info("Let process: %s" % jekyll_file)

    file_data = open(jekyll_file, "r").read()

    file_data_clean = re.sub("<(/)?(p|di|center|strong|span)[^>]*>","", file_data)
    logger.debug("data cleaned: %s"% file_data_clean)



###########    MAIN    ###########

if __name__ == "__main__":
    # the dir contains only jekyll-post files
    for afile in os.listdir(files_dir):
        logger.debug ("call process_jekyll_file for %s" % afile)
        analyze_jekyll_file(afile)
        # process_jekyll_file(afile)
    logger.info(tag_dic)



