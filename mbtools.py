#the following external command are being used: 
# sudo apt install espeak xdotool xclip xsel ffmpeg wmctrl zenity mpv
# pip install pyperclip google_speech pyautogui

import subprocess
import sys
import os


class mbwin():

    def __init__(self):
        pass

    def speak(ptext):
        gtext = '"' + str(ptext).replace('"', " ") + '"'
        #res = subprocess.call(["espeak", gtext])
        # defult speed is -s 175     
        res = subprocess.call(["espeak", "-s", "144", "-v", "english-us", gtext])        
        return res

    def speak_by_google(ptext, plang="en"):
        #gtext = '"' + str(ptext).replace('"', " ") + '"'
        from google_speech import Speech
        speech = Speech(ptext, plang)
        speech.play()

            
        
    def alert(ptitle, ptext, ptimeout=0):
        args = ["zenity", "--width", "400", "--info", "--title", ptitle, "--text", ptext ]
        if (ptimeout>0):
            args.extend(["--timeout", str(ptimeout)])

        res = subprocess.call(args)
        return res
       

    def get_active_win_process_id():
        byteOutput = subprocess.check_output(["xdotool", "getwindowfocus", "getwindowpid"], timeout=2)
        return byteOutput.decode('UTF-8').strip()

    def get_active_win_title():
        byteOutput = subprocess.check_output(["xdotool", "getwindowfocus", "getwindowname"], timeout=2)
        return byteOutput.decode('UTF-8').strip()
        #process = subprocess.Popen(["xdotool", "getwindowfocus", "getwindowname"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #out, err = process.communicate()    
        #return out

    def get_active_process_name():        
        pid = mbwin.get_active_win_process_id()
        #cat /proc/pid/comm
        fpath = f"/proc/{pid}/comm"        
        with open(fpath, "r+", encoding='utf-8') as myfile:
            content = myfile.readline()
        return content


    def get_win_by_name(prgxname="test.*mpv"):
        byteOutput = subprocess.check_output(["xdotool", "search", "--limit", "1", "--name", prgxname], timeout=2)
        return byteOutput.decode('UTF-8').strip()

    def send_key_to_win(pwid, *pkeys):
        args = ["xdotool", "key", "--clearmodifiers", "--delay", "44", "--window", pwid]
        for key in pkeys:
            args.append(key)

        byteOutput = subprocess.check_output(args, timeout=2)
        return byteOutput.decode('UTF-8').strip()
        
    def send_key(*pkeys, prepeat=1):
        args = ["xdotool", "key", "--clearmodifiers", "--delay", "44", "--repeat", str(prepeat)]
        for key in pkeys:
            args.append(key)

        byteOutput = subprocess.check_output(args, timeout=2)
        return byteOutput.decode('UTF-8').strip()

    def copy_to_clipboard(ptext):
        #works...
        cmd=f"""echo -n '''{ptext.strip()}''' | xclip -selection clipboard"""
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # output = ps.communicate()[0]
        # print(output)

        #import pyperclip
        #pyperclip.copy(ptext)
        #spam = pyperclip.paste()

    
    def clipboard_get(from_primary_clipboard = False):
        cmd="xclip -o -selection clipboard"
        if (from_primary_clipboard):
            cmd="xclip -o -selection primary"

        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ps.communicate()[0]
        #print(output)
        return output.decode("utf-8")

    def snap_window(right_pane=True):
        import pyautogui
        #print(pyautogui.size())
        width= pyautogui.size().width
        #wmctrl -e <G>,<X>,<Y>,<W>,<H>
        if right_pane:
            prm_e = f"0,{width//2},0,{width//2},0"
        else:
            prm_e = f"0,0,0,{width//2},0"

        cmd = f'''wmctrl -r :ACTIVE: -b remove,maximized_vert,maximized_horz; wmctrl -r :ACTIVE:  -e {prm_e}; wmctrl -r :ACTIVE: -b add,maximized_vert;'''
        mbwin.run_cmd(cmd)


    def run_bash_cmd(pcmd):
        #cmd = "ps -A | grep 'process_name'"
        byteOutput = subprocess.check_output(["bash", "-c", pcmd])
        return byteOutput.decode('UTF-8').strip()
        
    
    def run_cmd(pcmd):
        #works...
        #cmd="echo '" + ptext + "' | xclip -selection clipboard"
        ps = subprocess.Popen(pcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


    def config_get(pkey, pdefault=""):
        import json
        path_config = os.path.join(os.path.expanduser("~"), ".config", "mbpy.json")
        if os.path.exists(path_config) == False:
            return pdefault

        try:
            with open(path_config, 'r') as f: 
                config = json.load(f)
                #fp = os.path.realpath(f.name)
                if(len(pkey)>0):
                    return config.get(pkey, pdefault)
            # if pkey not in config:
                #    return pdefault
                return config
        except Exception as ex:
            print (ex)
            return pdefault


        
    def config_set(pkey, pval):
        import json
        path_config = os.path.join(os.path.expanduser("~"), ".config", "mbpy.json")
        config = {}
        if os.path.exists(path_config) == True:
            with open(path_config, 'r') as f: 
                try:
                    config = json.load(f)
                except Exception as ex:
                    print (ex)

        config[pkey] = pval
        #write it back to the file
        with open(path_config, 'w') as f:
            json.dump(config, f)




class mbtools():

    PATH_MPV_SOCKET="/tmp/mpvsocket_m1"

    def __init__(self):
        pass
    
    
    def get_audio_duration_as_ms(purl) -> int:
        from pymediainfo import MediaInfo
        media_info = MediaInfo.parse(purl)
        # Tracks can be accessed via the 'tracks' attribute or through shortcuts such as 'image_tracks', 'audio_tracks', 'video_tracks', etc.
        general_track = media_info.general_tracks[0]            
        return int(general_track.duration)
        
        # # takes time... :(
        # #song = pydub.AudioSegment.from_ogg(purl)
        # song = AudioSegment.from_file(purl) 
        # trimmed_song = song[1000:2000] #get reange of audio
        # return song.duration_seconds

        # import mutagen
        # au = mutagen.File(purl, easy=True)
        # if (au == None):
        #     return
        # return int(au.info.length)


    def log(ptext):
        with open("/tmp/mb.log", "a", encoding='utf-8') as myfile:
            myfile.writelines(ptext + "\n")   


    def mpv_play(ppath, pstart=-1, pend = -1, *pstart_args):        
        #"--force-window=no", "-no-video", -vo=null #don't show window and play audio only
        #mpv --really-quiet=yes --volume=99 --no-config --no-load-scripts "$1";
        #prms = [ "mpv", "--really-quiet=yes", "--no-config", "--no-load-scripts" ] #ok
        prms = [ "mpv", "--really-quiet=yes", "--load-scripts=no", "--config=no" ]

        if (pstart > 0):
            prms.append("--start=" + str(pstart))
        if (pend > 0):
            prms.append("--end=" + str(pend))

        for arg in pstart_args:
            prms.append(arg)

        prms.append(f''' "{ppath}" ''')
        cmd = ' '.join(prms)
        #cmd += " &"
        #print(cmd)
        mbwin.run_bash_cmd(cmd)


    def mpv_socket_play(pstart, pstop):
        cmd = 'echo \'{ "command": ["set_property", "start", "' + str(pstart) + '"] }\' | socat - "' + mbtools.PATH_MPV_SOCKET + '"'
        mbwin.run_bash_cmd(cmd)
        cmd = 'echo \'{ "command": ["set_property", "end", "' + str(pstop) + '"] }\' | socat - "' + mbtools.PATH_MPV_SOCKET + '"'
        mbwin.run_bash_cmd(cmd)
        cmd = 'echo \'{ "command": ["seek", ' + str(pstart) + ', "absolute"] }\' | socat - "' + mbtools.PATH_MPV_SOCKET + '"'
        mbwin.run_bash_cmd(cmd) 
        cmd = '''echo '{ "command": ["set_property", "pause", false] }' | socat - "''' + mbtools.PATH_MPV_SOCKET + '"'
        mbwin.run_bash_cmd(cmd)
        #mbwin.run_cmd(cmd) #works

    def mpv_socket_get_current_pos():
        cmd = '''echo '{ "command": ["get_property", "playback-time"] }' | socat - "''' + mbtools.PATH_MPV_SOCKET + '"'
        jsnret = mbwin.run_bash_cmd(cmd)
    
        import json
        pos = json.loads(jsnret)["data"]
        return pos


    def mpv_socket_get_current_path():
        cmd = '''echo '{ "command": ["get_property", "path"] }' | socat - "''' + mbtools.PATH_MPV_SOCKET + '"'
        jsnret = mbwin.run_bash_cmd(cmd)
        
        import json
        gpath = json.loads(jsnret)["data"]
        return gpath

        
    def ffmpeg_cut(pinput, poutput, pstart=0, pstop=0, *args ):
        prms = ["ffmpeg", "-y", "-vn"]
        if pstart>0:
            prms.append("-ss " + str(pstart))

        prms.append(f'''-i "{pinput}" ''')
        prms.append(" -c copy ")
        
        if pstop>0:
            dur = pstop - pstart
            prms.append(" -t " + str(dur))

        for arg in args:
            prms.append(f''' {arg} ''') #extra params

        prms.append(f''' "{poutput}" ''')

        cmd = ' '.join(prms)
        mbwin.run_bash_cmd(cmd)
        #mbwin.run_cmd(cmd) #works

        
    def ffmpeg_flac(pinput, poutput, pstart=0, pdur=0, pnormalize=True, pmono=True, psr=48000, *args ):
        prms = ["ffmpeg", "-y", "-vn"]
        if pstart>0:
            prms.append("-ss " + str(pstart))

        prms.append(f'''-i "{pinput}" ''')
        prms.append(f" -vn -ar {psr} -sample_fmt s16 ")

        nch = 2
        if(pmono):
            nch = 1
        prms.append(f" -ac {nch} ")

        if (pnormalize):
            prms.append(" -af 'loudnorm=i=-16:tp=-1' ")
        
        if pdur>0:
            prms.append(" -t " + str(pdur))

        for arg in args:
            prms.append(f''' {arg} ''') #extra params

        prms.append(f''' "{poutput}" ''')

        cmd = ' '.join(prms)
        mbwin.run_bash_cmd(cmd)

        #cmd = f'''ffmpeg -i '{path_media}' -y -ss {pos_start} -to {pos_end} -vn -c:a mp3  '{path_out}' '''        
        #cmd = f'''ffmpeg  -y -ss {pos_start} -i '{path_media}' -t {dur} -vn -c:a mp3  '{path_out}' '''    
        #cmd = f'''ffmpeg  -y -ss {pos_start} -i "{path_media}" -t {dur} -vn -af 'loudnorm=i=-16:tp=-1' -ac 2 -ar 44100 -sample_fmt s16 '{path_out}' '''    
        #mbwin.run_bash_cmd(cmd) #works
        #mbwin.run_cmd(cmd) #works
       

    def ffmpeg_convert_au(pinput, poutput, pstart=0, pduration=0, pnormalize=False, pmono=False, pbitrate="128k", psr=48000, *args ):
        prms = ["ffmpeg", "-y", "-vn"]
        if pstart>0:
            prms.append("-ss " + str(pstart))

        prms.append(f'''-i "{pinput}" ''')
        prms.append(f" -vn -ar {psr} -ab {pbitrate} ")
       # prms.append(f" -vn -ar {psr} -sample_fmt s16 ")

        nch = 2
        if(pmono):
            nch = 1
        prms.append(f" -ac {nch} ")

        if (pnormalize):
            prms.append(" -af 'loudnorm=i=-16:tp=-1' ")
        
        if pduration > 0:
            prms.append(" -t " + str(pduration))

        for arg in args:
            prms.append(f''' {arg} ''') #extra params

        prms.append(f''' "{poutput}" ''')

        cmd = ' '.join(prms)
        mbwin.run_bash_cmd(cmd)


    def ffmpeg_merge_media_files(poutput, pinfiles=[], preencode=True, pmono=True, psr=48000):
        '''    merges multiple audio/video files.
            if [preencode] is True, the audio format will be FLAC.
            [pmono] and [psr] parameters will be considered if [preencode] is True.
        '''

        path_cuts = "/tmp/cuts.txt"
        with open(path_cuts, 'w') as f:
            #f.writelines(pinfiles)
            for it in pinfiles:
                f.write(f'''file '{it}'\n''')

        prms = [f'''ffmpeg -y -protocol_whitelist concat,file,http,https,tcp,tls,crypto -safe 0 -f concat -i "{path_cuts}" ''']
        #prms = [f'''ffmpeg -safe 0 -f concat -i "{path_cuts}" ''']
        #prms = ['''ffmpeg -safe 0 -f concat -i <(printf "file '%s'\n" ''']
        #prms.append(' '.join(pinfiles))
        #prms.append('"' + '"  "'.join(pinfiles) + '"')
        #prms.append(") ")

        if(preencode==False):
            prms.append(" -c copy ")
        else:
            nch = 2
            if (pmono):
                nch = 1
            prms.append(f" -vn -ac {nch} -ar {psr} -sample_fmt s16 ")
            #prms.append(" -vn -ac 1 -ar 44100 -sample_fmt s16 ")


        prms.append(f''' "{poutput}" ''')

        cmd = ' '.join(prms)
        print (cmd)
        mbwin.run_bash_cmd(cmd)
        #ffmpeg -safe 0  -f concat -i cuts.txt -c copy  eb146-raw.flac
        #ffmpeg -safe 0 -f concat -i <(printf "file '$PWD/%s'\n" 1.WAV 2.WAV 3.WAV)  -c copy eb151_raw.wav


    def audacious_playing_media_path():
        import subprocess
        byteOutput = subprocess.check_output(["audtool", "current-song-filename"], timeout=2)
        return byteOutput.decode('UTF-8').strip()


    def speak_by_android_device(ptext, ip="192.168.56.102", port=12345): 
        #speak using Android x86 on Virtualbox
        import socket
        import urllib.parse
        txt = urllib.parse.unquote(ptext)
        txt = txt.replace("\r\n", ". ----").replace("\n", ". ----") #2022-07
        #print(txt)

        sck = socket.socket()
        #sck.connect(('127.0.0.1',12345))
        #sck.connect(('192.168.56.102',12345))
        sck.connect((ip, port))
        txt += "\n"
        sck.send(txt.encode())
        #ret = s.recv(1024).decode()
        mp3 = "/tmp/t2s.wav"
        f = open(mp3,'wb')
        ret = sck.recv(1024)
        while (ret):
            #print("Receiving...")
            f.write(ret)
            ret = sck.recv(1024)
        f.close()
        sck.close()

        print(mp3)
        mbtools.mpv_play(mp3)
        


    #saves the audio to temp folder and play it for the repeated requests. so no need to connect to google every time
    def google_speak_save(ptext, plang="en", pplay=True):
        #gtext = '"' + str(ptext).replace('"', " ") + '"'

        dir_tmp = "/tmp/cl"
        if(os.path.exists(dir_tmp)==False):
            os.mkdir(dir_tmp)

        import hashlib
        fn = hashlib.sha1(ptext.encode('utf-8')).hexdigest()
        fn = "t2s_" + str(fn) + ".mp3"            
        fpath=os.path.join(dir_tmp, fn)

        if os.path.exists(fpath):
            if (pplay):
                import pydub, pydub.playback
                au = pydub.AudioSegment.from_mp3(fpath)
                pydub.playback.play(au)

        else:
            from google_speech import Speech
            speech = Speech(ptext, plang)
            speech.save(fpath)
            if (pplay):
                speech.play()

        return fpath


    def speak_clipboard_google(plang="en", from_primary_clipboard = False):
        #gtext = '"' + str(ptext).replace('"', " ") + '"'
        gtext = mbwin.clipboard_get(from_primary_clipboard)
        gtext = gtext.strip()
        if (len(gtext)>4000):
            gtext = gtext[0: 4000] + " (...)"

        mbtools.google_speak_save(gtext)
        

    def speak_clipboard_android(plang="en", from_primary_clipboard = False):
        #gtext = '"' + str(ptext).replace('"', " ") + '"'
        gtext = mbwin.clipboard_get()
        gtext = gtext.strip()
        if (len(gtext)>50000):
            gtext = gtext[0: 50000] + " (...)"
        mbtools.speak_by_android_device(gtext)        


    def download(purl, plocalpath, pheaders = None, pdata = None):
        
        if os.path.exists(plocalpath):
            print("File is already exists:", plocalpath)
            return os.stat(plocalpath).st_size

        if (pheaders == None):
            pheaders = {
                'User-agent': 'Mozilla/4.0 (compatible; MRR API Python client; ' +
                str(sys.platform) + '; ' + str(sys.version).replace('\n', '') + ')',
                }

        import requests, shutil

        try:
            with requests.get(purl, data=pdata, headers=pheaders, stream=True) as req:
                with open(plocalpath, 'wb') as f:
                    shutil.copyfileobj(req.raw, f)
            #urllib.request.urlretrieve(purl, plocalpath)
            #req = urllib.request.Request(url, myparams, header)
            #req.headers = header
        except Exception as ex:
            print("ERROR downloading: ", purl, ex)
            return 0

        return os.stat(plocalpath).st_size



    def grab_url(purl, pheaders = None, pdata = None):

        if (pheaders == None):
            pheaders = {
                'User-agent': 'Mozilla/4.0 (compatible; MRR API Python client; ' +
                str(sys.platform) + '; ' + str(sys.version).replace('\n', '') + ')',
                }

        import requests

        try:
            res = requests.post(purl, data=pdata, headers=pheaders)   
            #res = requests.get(purl, headers=pheaders)
            
            return res.content
            #return res.raw
            #req = urllib.request.Request(url, myparams, header)
            #req.headers = header
        except Exception as ex:
            print("ERROR downloading: ", purl, ex)
            return ""

        return ""


#mymbwin = mbwin()

#mbwin.copy_to_clipboard("hello everyonsss sdf 322 3")
#mbwin.run_cmd("hellllloooooo")

#val1 = mbwin.config_get("test1")
#mbwin.config_set("test1", "value1")

#mbwin.google_speak_save("will only return the same value within a given script run:")

#mbwin.speak_clipboard_text()

if __name__ == '__main__':

    try:    
        arg=None
        if len(sys.argv)>1:
            arg = sys.argv[1]

        if arg == "-wintitle":
            wtitle = mbwin.get_active_win_title()
            print(wtitle)
            mbwin.speak(wtitle)  

        elif arg == "-winprocess":
            pname = mbwin.get_active_process_name()
            print(pname)
            mbwin.speak(pname)            

        elif arg == "-speak_clipboard_android":
            mbtools.speak_clipboard_android()

        elif arg == "-speak_clipboard_google":
            mbtools.speak_clipboard_google()

        elif arg == "-speak_clipboard_primary_google":
            mbtools.speak_clipboard_google(from_primary_clipboard=True)

        elif arg == "-help": #mb
            print("-wintitle".ljust(22, " "), "gets and speak active window title")       
            print("-winprocess".ljust(22, " "), "gets and speak active window process")       
            print("-speak_clipboard_android".ljust(22, " "), "speaks text copied to clipboard by android vbox.")       
            print("-speak_clipboard_google".ljust(22, " "), "speaks text copied to clipboard by google service.")       
            print("-speak_clipboard_primary_google".ljust(22, " "), "speaks text in primary clipboard (selection) by google service.")       
            print("-help".ljust(22, " "),"show this message")
        # else:
        #     print("try -help to see command line parameters")
        
    except Exception as ex:
        print (ex)


