# -*- coding: utf-8 -*-
# @Time : 2020/12/25 15:10
# @Author : Jiangzhesheng
# @File : main.py
# @Software: PyCharm
import sys
import argparse
import os
import logging
import subprocess
import shutil

def get_audio_from_video(video_path:str, outdir:str, logger):
    file_name=os.path.splitext(os.path.basename(video_path))[0]
    outfilepath=os.path.join(outdir,file_name+'.m4a')
    cmd=['ffmpeg','-i',video_path,'-vn','-codec','copy',outfilepath]
    a = subprocess.Popen(cmd)
    a.wait()
    if a.returncode == 0:
        logger.info('finishing converting')
    else:
        logger.error('failed converting')
    return outfilepath

def video_getter(url:str,outdir:str,logger):
    if url[0] != '\'':
        url=url
    else:
        url = url
    cmd=['you-get','-o',outdir,url]
    a=subprocess.Popen(cmd)
    a.wait()
    if a.returncode==0:
        logger.info('finishing download')
    else:
        logger.info('finishing download')

def video_rename(video_path:str)->str:
    file_name=os.path.abspath(video_path)
    new_name=file_name.replace(' ','-')
    os.rename(file_name,new_name)
    return new_name

def rm_all(dirpath):
    del_list = os.listdir(dirpath)
    for f in del_list:
        file_path = os.path.join(dirpath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)

def all(input_url:str, out_video_dir:str, out_audio_dir:str, logger):
    cur_dir=os.getcwd()
    tmp_dir=os.path.join(cur_dir, 'tmp')
    try:
        os.mkdir(tmp_dir)
    except FileExistsError:
        rm_all(tmp_dir)
    video_getter(url=input_url,outdir=tmp_dir,logger=logger)
    video_path=os.path.join(tmp_dir,os.listdir(tmp_dir)[0])
    video_path=video_rename(video_path)
    audio_path=get_audio_from_video(video_path=video_path, outdir=tmp_dir, logger=logger)
    shutil.copy(video_path,out_video_dir)
    shutil.copy(audio_path, out_audio_dir)
    rm_all(tmp_dir)

def main(argv):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input_url',default='https://v.qq.com/x/page/x0373a1yfhv.html')
    parser.add_argument('-ov', '--out_video_dir', default='C:\\Users\\jiangzhesheng\\Videos')
    parser.add_argument('-oa', '--out_audio_dir', default='C:\\Users\\jiangzhesheng\\Music')
    args = parser.parse_args(argv[1:])
    input_url = args.input_url
    out_audio_dir = args.out_audio_dir
    out_video_dir=args.out_video_dir

    try:
        os.mkdir(out_audio_dir)
    except FileExistsError as e:
        print(out_audio_dir, ' is exist, files in it may be overwritten')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    sh = logging.StreamHandler()
    shfmt = logging.Formatter('%(asctime)s-%(message)s')
    sh.setFormatter(fmt=shfmt)
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)

    # local_video_path='C:\\Users\\jiangzhesheng\\Videos\\河-台大合唱团.mp4'
    # get_audio_from_video(video_path=local_video_path,
    #                      outdir=out_audio_dir,
    #                      logger=logger)

    all(input_url=input_url,
        out_audio_dir=out_audio_dir,
        out_video_dir=out_video_dir,
        logger=logger)

if __name__ == '__main__':
    main(sys.argv)