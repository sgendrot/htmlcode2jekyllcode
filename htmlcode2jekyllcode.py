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
    logger.info("Let analyze: %s" % jekyll_file)

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

    # clean the useless tags
    file_data_clean = re.sub("<(/)?(p|div|center|span|style)[^>]*>","", file_data)
    # logger.debug("data : %s"% file_data)
    # logger.debug("data cleaned: %s"% file_data_clean)
    file_data_clean = re.sub("<(/)?(em)[^>]*>","*", file_data_clean)
    file_data_clean = re.sub("<(/)?(strong)[^>]*>","**", file_data_clean)


    jekyll_file_stream = open(jekyll_file, "w")
    jekyll_file_stream.write(file_data_clean)
    jekyll_file_stream.close()


def clean_img_jekyll_file(name):
    '''
    clean and update the img tag (correct link and change tag )

    :param name: the name of the file
    :type name: basestring
    :return: xxxx
    '''
    jekyll_file = files_dir+"/"+name
    logger.info("Let process: %s" % jekyll_file)

    file_data = open(jekyll_file, "r").read()
    # logger.debug("data : %s"% file_data)

    # capture all img tag to process them
    all_img_tags = re.findall("<img([^>]*)/>", file_data)
    for img_tag in all_img_tags:
        # a dict of the param of the img tag
        img_info = {}

        #if the tag isn't present, I will user this empty array
        nonexistent_tag = ['','']
        logger.debug("a img tag -----> %s" % img_tag)
        # not the most effective but more human readable
        img_info['alt'] = (re.search("alt=\"([^\"]*)\"", img_tag) or nonexistent_tag)[1]
        img_info['title'] = (re.search("title=\"([^\"]*)\"", img_tag) or nonexistent_tag)[1]
        img_info['src'] = (re.search("src=\"([^\"]*)\"", img_tag)or nonexistent_tag)[1]
        img_info['height'] = (re.search("height=\"([^\"]*)\"", img_tag) or nonexistent_tag)[1]
        img_info['width'] = (re.search("width=\"([^\"]*)\"", img_tag)or nonexistent_tag)[1]
        for key in img_info:
            logger.debug("%s = %s"% (key, img_info[key]))


    # replace old img tag by the new one
    # file_data_clean = re.sub("<img([^>])*/>","", file_data)


    # jekyll_file_stream = open(jekyll_file, "w")
    # jekyll_file_stream.write(file_data_clean)
    # jekyll_file_stream.close()


###########    MAIN    ###########

if __name__ == "__main__":
    # the dir contains only jekyll-post files
    for afile in os.listdir(files_dir):
        logger.debug ("call process_jekyll_file for %s" % afile)
        # process_jekyll_file(afile)
        # analyze_jekyll_file(afile)
        clean_img_jekyll_file(afile)
    logger.info(tag_dic)



