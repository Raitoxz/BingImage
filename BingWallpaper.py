# coding: utf-8
# author: Xiang
import urllib
import re
import os
import Image
import win32api
import win32con
import win32gui
import time
import _winreg
from os.path import getsize


def get_html(my_url):
    """
    获得网页的html
    :param my_url: 网页链接
    :return:
    """
    page = urllib.urlopen(my_url)
    my_html = page.read()
    return my_html


def set_wallpaper_from_bmp(bmp_path):
    """
    在注册表中设置新的背景图片
    :param bmp_path:图片的地址
    :return:
    """
    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                    "Control Panel\Desktop", 0,
                                    win32con.KEY_SET_VALUE)
    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 刷新桌面
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmp_path, win32con.SPIF_SENDWININICHANGE)
    # 保存注册表
    win32api.RegSetValueEx(reg_key, "Wallpaper", 0, win32con.REG_SZ, bmp_path)
    # 关闭注册表
    win32api.RegCloseKey(reg_key)


def set_wallpaper(img_path_, date_):
    """
    将图片的格式修改成bmp，
    :param img_path_:图片的地址
    :param date_:当天的时间
    :return:
    """
    # 把图片格式统一转换成bmp格式,并放在源图片的同一目录
    img_dir = os.path.dirname(img_path_)
    bmp_image = Image.open(img_path_)
    new_bmp_path = os.path.join(img_dir, '%s.bmp') % date_
    bmp_image.save(new_bmp_path, "BMP")
    set_wallpaper_from_bmp(new_bmp_path)


if __name__ == "__main__":
    html = get_html("http://cn.bing.com/")
    pattern = re.compile(r"http://s\.cn\.bing\.net(\w|/|\-|\d|_|\.)*\.jpg")
    match = re.search(pattern, html)
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    img_name = '%s.jpg' % date
    img_path = 'F:\\bing_image\\' + '%s' % img_name
    urllib.urlretrieve(match.group(), img_path)
    set_wallpaper(img_path, date)
    print "Succeed!"
