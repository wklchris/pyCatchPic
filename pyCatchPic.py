# coding utf-8
# Python version: 3.4
import os
import re
import urllib.request as urllib2
# For filtering pixel size of pics
import io
from PIL import Image   # Requiring Lib: pillow


def download_from_url(originurl, input_srclst, pixel_size=(100, 100)):
    """
    download_from_url(originurl, input_srclst [, pixel_size]):
        The main function of downloading pics from <str: originurl>.

        Pics found by searching <list: input_srclst> will be downloaded.
        Pics smaller than <tuple: pixel_size = (100,100)> won't be download.
    """
    browser = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
    browser += ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    req = urllib2.Request(originurl)
    req.add_header('User-Agent', browser)
    print("Now reading url...(Please restart if there's no response for a long time)")
    byte_f = urllib2.urlopen(req).read()
    try:
        utf8_f = byte_f.decode('utf-8', 'ignore')
    except UnicodeDecodeError as e:
        print(e)
        exit()
    else:
        print('Successfully decode.\n=====')
        get_pics_url = image_url(utf8_f, input_srclst)
        print('Estimated {} pics without filtering.\n'.format(len(get_pics_url)))
        download_pics(get_pics_url, pixel_size)


def image_url(pics, srclst):
    """
    image_url(pics, srclst):
        Get urls of pics filtered by <list: srclst> from <str: pics>.

        Return <list: all_pics>: urls of all pics on webpage.
    """
    all_pics = []
    while bool(srclst):
        all_pics.extend(re.compile(srclst.pop()).findall(pics))
    return all_pics


def download_pics(pic_url, pixel_filter):
    """
    download_pics(pic_url):
        Download pics to c:\test from <list: pic_url>.

        Pics smaller than <tuple: pixel_filter> won't be downloaded.
        Names and total num of pics will be printed on screen.
    """
    folder = 'test'
    os.chdir('c:\\')
    try:
        if not os.path.exists(folder):
            os.mkdir(folder)
    except:
        print('Fail to create a folder for downloading. ')
        exit()
    total_num = 0
    for single_pic_url in pic_url:
        data = urllib2.urlopen(single_pic_url).read()
        im = Image.open(io.BytesIO(data))
        if im.width > pixel_filter[0] and im.height > pixel_filter[1]:
            total_num += 1
            pic_name = re.split('/', single_pic_url)[-1]
            print('[{:0>4d}/{}]'.format(total_num, len(pic_url)), pic_name, '{0}x{1}'.format(im.width, im.height))
            path = folder + '/' + pic_name
            with open(path, 'wb') as f:
                f.write(data)
    print('=====\nAll pics match width>{0} px and height>{1} px.'.format(pixel_filter[0], pixel_filter[1]))
    print('Total download: {0} pics. Filtered: {1}'.format(total_num, len(pic_url)-total_num))
    print(r'Saving path: c:\test')


# ================
# ===== Main =====
# ================

# Version & Author
version_of_this = 'ver 0.1\n\tin Python 3.4 --July 14, 2016'
author_of_this = "wklchris (github.com/wklchris)"
print('Pics Downloader {0} \nby {1}\n'.format(version_of_this, author_of_this))

# Main
pixel_height, pixel_width = 100, 100
pixel_no_smaller_than_this = (pixel_width, pixel_height)
downUrl = 'http://tieba.baidu.com/p/4671102626'  # Test Link
srcList = [r'src="(http://imgsrc.baidu.com/forum/.*?)"',
           r'src="(http://hiphotos.baidu.com/.*?)"']

download_from_url(downUrl, srcList, pixel_no_smaller_than_this)
