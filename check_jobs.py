#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep

from captricity.captricity_tools import check_jobs, process_images

def main():
    """
    Adds images to batches and checks job status every half hour
    """
    while True:
        print "Processing Images"
        process_images()
        print "Checking job status"
        check_jobs()
        print "Taking a 30 minute nap"
        sleep(30*60)


if __name__ == '__main__':
    main()
