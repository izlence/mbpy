from mbwin import mbwin


class mbtools():

    PATH_MPV_SOCKET="/tmp/mpvsocket_m1"

    def __init__(self):
        pass


    def send_welcome_message(self):
        pass

    def log(ptext):
        with open("/tmp/mb.log", "a", encoding='utf-8') as myfile:
            myfile.writelines(ptext + "\n")   


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

        
    def ffmpeg_flac(pinput, poutput, pstart=0, pdur=0, pnormalize=True, pmono=True ):
        prms = ["ffmpeg", "-y", "-vn"]
        if pstart>0:
            prms.append("-ss " + str(pstart))

        prms.append(f'''-i "{pinput}" ''')
        prms.append(" -vn -ar 44100 -sample_fmt s16 ")

        if(pmono):
            prms.append(" -ac 1 ")
        else:
            prms.append(" -ac 2 ")

        if (pnormalize):
            prms.append(" -af 'loudnorm=i=-16:tp=-1' ")
        
        if pdur>0:
            prms.append(" -t " + str(pdur))

        prms.append(f''' "{poutput}" ''')

        cmd = ' '.join(prms)
        mbwin.run_bash_cmd(cmd)

        #cmd = f'''ffmpeg -i '{path_media}' -y -ss {pos_start} -to {pos_end} -vn -c:a mp3  '{path_out}' '''        
        #cmd = f'''ffmpeg  -y -ss {pos_start} -i '{path_media}' -t {dur} -vn -c:a mp3  '{path_out}' '''    
        #cmd = f'''ffmpeg  -y -ss {pos_start} -i "{path_media}" -t {dur} -vn -af 'loudnorm=i=-16:tp=-1' -ac 2 -ar 44100 -sample_fmt s16 '{path_out}' '''    
        #mbwin.run_bash_cmd(cmd) #works
        #mbwin.run_cmd(cmd) #works
       


    def ffmpeg_merge_media_files(poutput, pinfiles=[], preencode=True):
        '''    merges multiple audio/video files.    '''
        path_cuts = "/tmp/cuts.txt"
        with open(path_cuts, 'w') as f:
            #f.writelines(pinfiles)
            for it in pinfiles:
                f.write(f'''file '{it}'\n''')

        prms = [f'''ffmpeg -safe 0 -f concat -i "{path_cuts}" ''']
        #prms = ['''ffmpeg -safe 0 -f concat -i <(printf "file '%s'\n" ''']
        #prms.append(' '.join(pinfiles))
        #prms.append('"' + '"  "'.join(pinfiles) + '"')
        #prms.append(") ")

        if(preencode==False):
            prms.append(" -c copy ")
        else:
            prms.append(" -vn -ac 1 -ar 44100 -sample_fmt s16 ")

        prms.append(f''' "{poutput}" ''')

        cmd = ' '.join(prms)
        print (cmd)
        mbwin.run_bash_cmd(cmd)
        #ffmpeg -safe 0  -f concat -i cuts.txt -c copy  eb146-raw.flac
        #ffmpeg -safe 0 -f concat -i <(printf "file '$PWD/%s'\n" 1.WAV 2.WAV 3.WAV)  -c copy eb151_raw.wav



