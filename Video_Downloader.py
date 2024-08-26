# The purpose of this is to download and downscale videos for uploading elsewhere


import subprocess as sp
import os
from moviepy.editor import VideoFileClip

class Video_Handler:


    def youtube_downloader(url=None):
        fpin  = "Downloaded-Videos"
        fpout = "Converted-Videos"

        if not os.path.exists(fpin):
            os.makedirs(fpin, exist_ok=True)
        if not os.path.exists(fpout):
            os.makedirs(fpout, exist_ok=True)


        if url is None:
            print("There is nothing here")
            return "There is nothing here"
        
        result = str(sp.run("yt-dlp "+url+" --print live_status",capture_output=True))

        if "not_live" in result :
            source = os.path.join(fpin,"%(title)s.%(ext)s")
            result1 = sp.run("yt-dlp "+url+" -o "+source)
            cnt = os.listdir(fpin)
            print(cnt)
            toss = cnt[0]
            if ".webm" not in toss:
                cnt2 = toss[:-4]+".webm"
            else:
                cnt2 = toss
            filepath1 = os.path.join(fpin,toss)
            filepath2 = os.path.join(fpout,cnt2)

            clip = VideoFileClip(filepath1)
            frame = clip.size
            sframe = [0,0]
            if frame[0]>500 or frame[1]>500:
                if frame[0]/frame[1] == 1:
                    sframe[0] = int(max(frame[0]*0.3, 240))
                    sframe[1] = int(max(frame[1]*0.3, 240))
                elif frame[0]/frame[1] == 9/16:
                    sframe[0] = int(max(frame[0]*0.3, 320))
                    sframe[1] = int(max(frame[1]*0.3, 480))
                else:
                    sframe[0] = int(max(frame[0]*0.3, 480))
                    sframe[1] = int(max(frame[1]*0.3, 300))
            clip.close
#            print(sframe)
#            print(cnt2)
            reso = ""+str(sframe[0])+"x"+str(sframe[1])
            if not os.path.exists(filepath2):
                cmd = str("ffmpeg -i \""+filepath1+"\" -s "+reso+" \""+filepath2+"\"")
                result2 = sp.run(cmd)
            for file in os.listdir(fpin):
                print(file)
                os.remove(os.path.join(fpin,file))
            return filepath2
        else:
            return "Stream is live, I can not download a livestream in process. Apologies."



    def test(url=None):
        result = str(sp.run("yt-dlp "+url+" --print live_status",capture_output=True))
        print("not_live" in result)


#Video_Handler.test("https://www.youtube.com/watch?v=LU8dH6YmkOE")
Video_Handler.youtube_downloader("https://youtu.be/d5q1_S6lI-0")