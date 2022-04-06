#the following external command are being used: 
# sudo apt install espeak xdotool xclip xsel
# pip install pyperclip 

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


    def speak_clipboard_text(plang="en"):
        #gtext = '"' + str(ptext).replace('"', " ") + '"'
        gtext = mbwin.clipboard_get()
        gtext = gtext.strip()
        if (len(gtext)>4000):
            gtext = gtext[0: 4000] + " (...)"

        mbwin.google_speak_save(gtext)


            
        
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
        cmd="echo '" + ptext + "' | xclip -selection clipboard"
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # output = ps.communicate()[0]
        # print(output)

        #import pyperclip
        #pyperclip.copy(ptext)
        #spam = pyperclip.paste()

    
    def clipboard_get():
        cmd="xclip -o -selection clipboard"
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ps.communicate()[0]
        #print(output)
        return output.decode("utf-8")

    
        

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

#mymbwin = mbwin()

#mbwin.copy_to_clipboard("hello everyonsss sdf 322 3")
#mbwin.run_cmd("hellllloooooo")

#val1 = mbwin.config_get("test1")
#mbwin.config_set("test1", "value1")

#mbwin.google_speak_save("will only return the same value within a given script run:")

#mbwin.speak_clipboard_text()

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

    elif arg == "-speak_clipboard":
        mbwin.speak_clipboard_text()

    elif arg == "-help": #mb
        print("-wintitle".ljust(22, " "), "gets and speak active window title")       
        print("-winprocess".ljust(22, " "), "gets and speak active window process")       
        print("-speak_clipboard".ljust(22, " "), "speaks text copied to clipboard.")       
        print("-help".ljust(22, " "),"show this message")
    # else:
    #     print("try -help to see command line parameters")
       
except Exception as ex:
    print (ex)


