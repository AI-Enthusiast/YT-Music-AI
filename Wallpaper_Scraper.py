# Wallpaper scraper taken from Grypse https://github.com/Grypse/DownImg
# updated to python 3.6 by Cormac Dacker

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 10:25:34 2015
@author: Gryps
"""

import http.client as httplib
import os
import socket
import urllib.request as urllib2
from Lib import queue as Queue
from pathlib import Path
from threading import Thread
from time import ctime, time

from urllib.request import HTTPError, URLError


def down(down_dir, link):
    """
    Download the images from the given link and store it to the designated directory
    Args:
        down_dir:the images storage folder
        link:the download link
    Raises:
        HTTPError:An error occured accessing the website
        URLError:An error occured when os no connection
        socket.error:An error occured during TCP/IP connection
    """
    req = urllib2.Request(link)
    req.add_header("User-Agent", "Mozilla 5.0")
    conn = urllib2.urlopen(req)
    directory = down_dir / os.path.basename(link)
    f = directory.open('wb')
    f.write(conn.read())
    f.close()


def setup_dir():
    """
    Set the download directory of images downloaded
    Return:
        download_dir:the setting directory of images to be stored
    """
    download_dir = Path("H:\\pic")
    return download_dir


def get_link(start, stop):
    """
    Acquire all downloading links and set to links array
    Args:
        start:the image initialed index value
        stop:the image terminated index value
    Return:
        links:the all link array for downloading
    """
    links = []
    for x in range(start, stop):
        url = 'https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-' + str(x) + '.jpg'
        links.append(url)
    return links


class DownloadWorker(Thread):
    """
    The class of image downloading thread
    Function:
        __init__():initialization of threading
        run:the running of threading
    """

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            down_dir, link = self.queue.get()
            print
            os.path.basename(link) + "\n"
            try:
                down(down_dir, link)
            except HTTPError as e:
                print(os.path.basename(link) + ': ' + e.reason)
            except URLError as e:
                print(e.__weakref__)
            except socket.error as e:
                print(e.__weakref__)
            # when the BadStatueLine exception occurs pass it and start the next task
            except httplib.BadStatusLine:
                pass
            self.queue.task_done()


def main():
    ts = time()
    start = input("Please input the start value: ")
    stop = input("Please input the stop value: ")
    # set the number of threads
    threads = input("Please input the download numbers every piece: ")
    k = stop - start
    # acquire the download links
    links = [l for l in get_link(start, stop)]
    # set the download storage directory
    down_dir = setup_dir()
    queue = Queue()
    # judge download numbers if greater than threads or not
    # if K< = threads ,set the k for threads,else set the threads for the number of thread
    if k <= threads:
        for x in range(k - 1):
            queue.qsize()
            worker = DownloadWorker(queue)
            worker.setDaemon(True)
            worker.start()
    else:
        for x in range(threads):
            worker = DownloadWorker(queue)
            worker.setDaemon(True)
            worker.start()
    # traverse the links and put the link to queue
    for link in links:
        queue.put((down_dir, link))
    # the new queue joining
    queue.join()
    print
    'Took {}'.format(time() - ts)
    print
    "The finished time:" + ctime()


if __name__ == '__main__':
    main()
