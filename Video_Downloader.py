# The purpose of this is to download and downscale videos for uploading elsewhere

import subprocess as sp
from multiprocessing import Process
import os
import contextlib
from moviepy.editor import VideoFileClip

class Video_Handler:
    

    def youtube_downloader(url=None):
        fpin = "Downloaded-Videos"
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
            formats = str(sp.run("yt-dlp "+url+ " -F",capture_output=True)).replace("\\n","\n").split("\n")
            formatter = []
            for s in formats:
                if not "only" in s and not "images" in s and not "EXT" in s and not "-" in s and not "[youtube]" in s and not "[info]" in s and not "stderr" in s:
                    formatter.append(s.replace("    ","  ").replace("  "," ").replace("  "," ").replace("  "," "))
            formatter = formatter[0].split(" ")
            format = ""
            
            if "mp4" in formatter[1] or "webm" in formatter[1]:
                format = str(formatter[0])
#            print(format+"\n")

            result1 = sp.run("yt-dlp "+url+" -f "+str(format)+" -o "+source)
            
            cnt = os.listdir(fpin)
#            print(cnt)
            toss = cnt[0]
            if ".webm" not in toss:
                cnt2 = toss[:-4]+".webm"
            else:
                cnt2 = toss
            filepath1 = os.path.join(fpin,toss)
            filepath2 = os.path.join(fpout,cnt2)



            def getFrameSize(filer=None):
                if filer == None:
                    return None
                else:
                    tclip =VideoFileClip(filer) 
                    clip = tclip.size
                    tclip.close()
                    return clip
            


            frame = getFrameSize(filepath1)
            
            sframe = [0,0]
            if frame[0]>500 or frame[1]>500:
                print("Resizing")
                if frame[0]/frame[1] == 1:
                    sframe[0] = int(max(frame[0]*0.3, 240))
                    sframe[1] = int(max(frame[1]*0.3, 240))
                    print("Square")
                elif frame[0]/frame[1] == 9/16:
                    sframe[0] = int(max(frame[0]*0.3, 300))
                    sframe[1] = int(max(frame[1]*0.3, 480))
                    print("Portait HD")
                else:
                    sframe[0] = int(max(frame[0]*0.3, 480))
                    sframe[1] = int(max(frame[1]*0.3, 300))
                    print("Other")
            else:
                sframe = frame
#            print(sframe)
#            print(cnt2)
            reso = ""+str(sframe[0])+"x"+str(sframe[1])
            if not os.path.exists(filepath2):
                cmd = str("ffmpeg -i \""+filepath1+"\" -s "+reso+" \""+filepath2+"\"")
                result2 = sp.run(cmd)
            os.remove(filepath1)
            return filepath2
        else:
            return "Stream is live, I can not download a livestream in process. Apologies."



    def test(url=None):
        result = str(sp.run("yt-dlp "+url+" --print live_status",capture_output=True))
        print("not_live" in result)


#Video_Handler.test("https://www.youtube.com/watch?v=LU8dH6YmkOE")
Video_Handler.youtube_downloader("https://youtu.be/d5q1_S6lI-0")
Video_Handler.youtube_downloader("https://youtu.be/z4E9lcuz3WU")