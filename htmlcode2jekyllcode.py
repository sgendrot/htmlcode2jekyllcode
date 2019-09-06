#!/usr/bin/env python

import logging.config
import os, re

# Logging config
logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'logging.conf'))
# logger = logging.getLogger("logger_console_info")
logger = logging.getLogger("logger_console_debug")



# Global var
# files_dir = "/Users/sylvain/jekyll/velocipaide/_posts"
files_dir = "/Users/sgendrot/jekyll/velocipaide/_posts"
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

    file_data = open(jekyll_file, "r", encoding="latin-1").read()

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

    file_data = open(jekyll_file, "r", encoding="latin-1").read()
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


        # cleaning img src (bad url)
        if "/wp-" in img_info['src']:  # a local image
            img_src = img_info['src'].split("/")
            logger.debug(img_src)
            logger.debug("local img name= /assets/%s" % img_src[len(img_src)-1])
            img_info['src'] = "/assets/" + img_src[len(img_src)-1]
        else: # external image (I have to remove ../../../ added by the web copier)
            img_src = re.sub("(../)*",'',img_info['src'])
            logger.debug("extrenal img name= %s" % img_src)
            img_info['src'] = img_src


        # markdown img: ![Alt text](/path/to/img.jpg "Optional title"){:height="50%" width="50%"}
        img_jekyll_tag = "![%s](%s" % (img_info['alt'], img_info['src'])
        if img_info['title']:
            img_jekyll_tag = img_jekyll_tag + ' "' + img_info['title'] + '"'
        img_jekyll_tag = img_jekyll_tag + ')'
        if img_info['height'] and img_info['width']:
            img_jekyll_tag = img_jekyll_tag + '{:height="%s" width="%s"}' % (img_info['height'], img_info['width'])
        elif img_info['height']:
            img_jekyll_tag = img_jekyll_tag + '{:height="%s"}' % img_info['height']
        elif img_info['width']:
            img_jekyll_tag = img_jekyll_tag + '{:width="%s"}' % img_info['width']

        logger.debug("img jekyll: %s" % img_jekyll_tag)

        # replace old img tag by the new one
        file_data = file_data.replace("<img" + img_tag + "/>", img_jekyll_tag)

    logger.debug(file_data)
    jekyll_file_stream = open(jekyll_file, "w", encoding="latin-1")
    jekyll_file_stream.write(file_data)
    jekyll_file_stream.close()



def clean_a_href_tags(name):
    '''
    Many a tag are ugly (like ../../../../../wp-content/upLoads/...)
    Clean the bad urls and put the jekyll's urls

    Jekyll tag A:
    [an example](http://example.com/ "Title")
    <a href="http://example.com/" title="Title">an example</a>

    :param name: the name of the file
    :type name: basestring
    :return: xxxx
    '''
    jekyll_file = files_dir+"/"+name
    logger.info("Let process: %s" % jekyll_file)

    file_data = open(jekyll_file, "r", encoding="latin-1").read()
    # logger.debug("data : %s"% file_data)

    # capture all img tag to process them
    all_ahref_tags = re.findall("<a([^>]*)>([^<]*)</a>", file_data)
    for ahref_tag in all_ahref_tags:
        # a dict of the param of the img tag
        ahref_info = {}

        #if the tag isn't present, I will user this empty array
        nonexistent_tag = ['','']
        logger.debug("a a_href tag -----> %s" % ahref_tag[0])
        # logger.debug("a a_href text -----> %s" % ahref_tag[1])
        # not the most effective but more human readable
        ahref_info['href'] = (re.search("href=\"([^\"]*)\"", ahref_tag[0]) or nonexistent_tag)[1]
        # ahref_info['target'] = (re.search("target=\"([^\"]*)\"", ahref_tag[0]) or nonexistent_tag)[1] #not sure of the target support
        ahref_info['title'] = (re.search("title=\"([^\"]*)\"", ahref_tag[0])or nonexistent_tag)[1]
        for key in ahref_info:
            logger.debug("%s = %s"% (key, ahref_info[key]))


        # cleaning img url
        if "/wp-content/upLoads" in ahref_info['href'] and not any ( x in ahref_info['href'] for x in [".html","php"]):  # a local img, not a link
            img_name = ahref_info['href'].split("/")
            logger.debug(img_name)
            logger.debug("local ahref name= /assets/%s" % img_name[len(img_name)-1])
            ahref_info['href'] = "/assets/" + img_name[len(img_name)-1]
        else: # external ahref (I have to remove ../../../ added by the web copier)
            ahref_url = re.sub("(\.\./)*",'',ahref_info['href'])
            logger.debug("extrenal ahref name= %s" % ahref_url)
            ahref_info['href'] = ahref_url


        # markdown ahref: [text](http://example.com/ "Title")
        ahref_jekyll_tag = "[%s](%s" % (ahref_tag[1], ahref_info['href'])
        if ahref_info['title']:
            ahref_jekyll_tag = ahref_jekyll_tag + ' "' + ahref_info['title'] + '"'
        ahref_jekyll_tag = ahref_jekyll_tag + ')'

        logger.debug("ahref jekyll: %s" % ahref_jekyll_tag)

        # replace old ahref tag by the new one
        file_data = file_data.replace("<a"+ahref_tag[0]+">"+ahref_tag[1]+"</a>",ahref_jekyll_tag)

    logger.debug(file_data)
    jekyll_file_stream = open(jekyll_file, "w", encoding="latin-1")
    jekyll_file_stream.write(file_data)
    jekyll_file_stream.close()


def add_markdown_flag(name):
    '''
    To use markdown inside html tag, I have to add a flag to them
    flag to add: markdown="1"

    :param name: the name of the file
    :type name: basestring
    :return: xxxx
    '''
    jekyll_file = files_dir+"/"+name
    logger.info("Let analyze: %s" % jekyll_file)

    file_data = open(jekyll_file, "r", encoding="latin-1").read()

    tags_extracted = re.findall("(<[^/][^>]*>)", file_data)
    for atag in tags_extracted:
        logger.debug("tags extracted: %s"% atag)

        # replace old tag by the new one
        if any(x in atag for x in ['<a','<p','<li']):
            file_data = re.sub(atag,atag[:-1]+' markdown="1">', file_data)
        logger.debug("new file: %s" % file_data)

    # rewrite the file
    jekyll_file_stream = open(jekyll_file, "w", encoding="latin-1")
    jekyll_file_stream.write(file_data)
    jekyll_file_stream.close()



###########    MAIN    ###########

if __name__ == "__main__":
    # the dir contains only jekyll-post files
    for afile in os.listdir(files_dir):
        logger.debug ("call process_jekyll_file for %s" % afile)
        # process_jekyll_file(afile)
        # analyze_jekyll_file(afile)
        # clean_img_jekyll_file(afile)
        # add_markdown_flag(afile)
    logger.info(tag_dic)



