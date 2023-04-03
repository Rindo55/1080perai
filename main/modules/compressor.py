import asyncio
import aiofiles
import aiohttp
from html_telegraph_poster import TelegraphPoster
from pathlib import Path

from main.modules.utils import get_progress_text 

import os

import re

import math

import subprocess

async def gg():
          cmd = '''ffmpeg -hide_banner -loglevel quiet -progress "progressaa.txt" -i "video.mkv" -filter_complex "[0:v]drawtext=fontfile=font.ttf:text='t.me/animxt':fontsize=25:fontcolor=ffffff:alpha='if(lt(t,0),0,if(lt(t,5),(t-0)/5,if(lt(t,15),1,if(lt(t,20),(5-(t-15))/5,0))))':x=w-text_w-15:y=15" -c:v libx265 -s 192x144 -pix_fmt yuv420p10le -preset medium -r 24000/1001 -crf 24.2 -x265-params profile=main444-10:deblock=-1,-1:no-sao:aq-mode=2:aq-strength=0.75:bframes=6:frame-threads=4 -c:a libopus -b:a 96k "out.mkv" -y''',
          subprocess.Popen(cmd,shell=True)

async def mediainfo(filed):
    try:
        process = await asyncio.create_subprocess_shell(
            f"mediainfo '''{filed}''' --Output=HTML",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        out = stdout.decode()
        client = TelegraphPoster(use_api=True)
        client.create_api_token("Mediainfo")
        page = client.post(
            title="Mediainfo",
            author=("animxt"),
            author_url=f"https://t.me/animxt",
            text=out,
        )
        return page["url"]
    except Exception as error:
        print(error)
        return None

async def compress_video(total_time, videox, name, guessname):

  try:

    video = "video.mkv"

    out = "out.mkv" 

    prog = "progressaa.txt"

    with open(prog, 'w') as f:

      pass

    

    asyncio.create_task(gg())

   

    while True:

      with open(prog, 'r+') as file:

        text = file.read()

        frame = re.findall("frame=(\d+)", text)

        time_in_us=re.findall("out_time_ms=(\d+)", text)

        progress=re.findall("progress=(\w+)", text)

        speed=re.findall("speed=(\d+\.?\d*)", text)

        if len(frame):

          frame = int(frame[-1])

        else:

          frame = 1

        if len(speed):

          speed = speed[-1]

        else:

          speed = 1

        if len(time_in_us):

          time_in_us = time_in_us[-1]

        else:

          time_in_us = 1

        if len(progress):

          if progress[-1] == "end":

            break

        

        time_done = math.floor(int(time_in_us)/1000000)

        

        progress_str = get_progress_text(guessname,"Encoding",time_done,str(speed),total_time,enco=True)

        try:

          await videox.edit_caption(progress_str)

        except:

            pass

      await asyncio.sleep(20)

    if os.path.lexists(out):

        return out

    else:

        return "None"

  except Exception as e:

    print("Encoder Error",e)
