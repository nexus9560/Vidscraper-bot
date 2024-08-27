# The purpose of this is to download and downscale videos for uploading elsewhere

import subprocess as sp
from multiprocessing import Process
import os
import contextlib
from moviepy.editor import VideoFileClip

class Video_Handler:
    



    #Method for downloading youtube videos
    def youtube_downloader(url=None, guild=None):
        #Download folder, file input
        fpin = "Downloaded-Videos"
        #Output location
        fpout = "Converted-Videos"

        servLoc = None

        # For the future, each server will have its own place for the videos
        if guild != None:
            servLoc = str(guild)

        # Makes sure the folders exist
        # Future proofing with the idea that every server will have their own folder for the sake of housekeeping.
        if servLoc!= None:
            if not os.path.exists(fpin):
                os.makedirs(servLoc, fpin, exist_ok=True)
            if not os.path.exists(fpout):
                os.makedirs(servLoc, fpout, exist_ok=True)
        else:
            if not os.path.exists(fpin):
                os.makedirs(fpin, exist_ok=True)
            if not os.path.exists(fpout):
                os.makedirs(fpout, exist_ok=True)

        # Makes sure there is a URL (Probably should be in front of the folder check, but whatever)
        if url is None:
            print("There is nothing here")
            return "There is nothing here"
        
        #This checks to see if it's a livestream, if it is a livestream, bail.
        result = str(sp.run("yt-dlp "+url+" --print live_status",capture_output=True))


        # This is where the check occurs, if it is not live, bail.        
        if "not_live" in result :

            # Source File
            source = os.path.join(fpin,"%(title)s.%(ext)s")

            # Format acquisition, looks for the format with both video and audio in one, usually the smallest is listed first
            formats = str(sp.run("yt-dlp "+url+ " -F",capture_output=True)).replace("\\n","\n").split("\n")
            formatter = []
            # Strips white space out
            for s in formats:
                if not "only" in s and not "images" in s and not "EXT" in s and not "-" in s and not "[youtube]" in s and not "[info]" in s and not "stderr" in s:
                    formatter.append(s.replace("    ","  ").replace("  "," ").replace("  "," ").replace("  "," "))
            formatter = formatter[0].split(" ")
            format = ""
            

            # Looks for the *.mp4 or *.webm format download
            if "mp4" in formatter[1] or "webm" in formatter[1]:
                format = str(formatter[0])
#            print(format+"\n")

            # Actually downloads the video with the prescribed format and output filename, at some point I should check and make sure that yt-dlp is actually downloaded
            result1 = sp.run("yt-dlp "+url+" -f "+str(format)+" -o "+source)
            

            # Looks in the fpin folder for the downloader video
            cnt = os.listdir(fpin)
#            print(cnt)

            # This block here gets the filename and makes a string with the new filename as a .webm
            toss = cnt[0]
            if ".webm" not in toss:
                cnt2 = toss[:-4]+".webm"
            else:
                cnt2 = toss
            filepath1 = os.path.join(fpin,toss)
            filepath2 = os.path.join(fpout,cnt2)


            # This definition gets the frame, as I intend on resizing videos to be 360p at a minimum, and even at 360p they may be too big or something
            def getFrameSize(filer=None):
                if filer == None:
                    return None
                else:
                    tclip =VideoFileClip(filer) 
                    clip = tclip.size
                    tclip.close()
                    return clip
            


            frame = getFrameSize(filepath1)
            

            # Checks to see if the frame is above 500px to a side and resizes to a third of that size while attempting to preserve aspect ratio, otherwise continues
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

            # Checks to see if the converted file exists and if it does skip this section, otherwise convert it to webm
            if not os.path.exists(filepath2):
                cmd = str("ffmpeg -i \""+filepath1+"\" -s "+reso+" \""+filepath2+"\"")
                result2 = sp.run(cmd)
            os.remove(filepath1)
            return filepath2
        else:
            return "Stream is live, I can not download a livestream in process. Apologies."


    # Definition for testing things
    def test(url=None):
        result = str(sp.run("yt-dlp "+url+" --print live_status",capture_output=True))
        print("not_live" in result)



# Testing section
#   Video_Handler.test("https://www.youtube.com/watch?v=LU8dH6YmkOE")
#   Video_Handler.youtube_downloader("https://youtu.be/d5q1_S6lI-0")
#   Video_Handler.youtube_downloader("https://youtu.be/z4E9lcuz3WU")