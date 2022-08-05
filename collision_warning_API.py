
def create_rec(num_detections):
    frame_dict = {}
    for id in range(num_detections):
        frame_dict['frame_details', id] = []
        frame_dict['dng_frame_num', id] = []
    return frame_dict
         
def update_frame_details(dict,w,id,imW):
    time_stamp = time.time()
    dict['frame_details', id].append(((w/imW),time_stamp))
    if len(dict['frame_details' , id]) == 3 :
        del dict['frame_details' , id][0]

def time_to_collision_RTD(dict,id):
    frame_dict = dict
    decided_value = 0.47
    distance_travelled = frame_dict['frame_details' , id][-1][0] - frame_dict['frame_details' , id][-2][0] #distance travelled in a frame
    distance_travelled = round(distance_travelled,3)
    if distance_travelled > 0:
        remaining_distance = decided_value - frame_dict['frame_details' , id][-1][0]
        rat_velocity = distance_travelled/(frame_dict['frame_details' , id][-1][1] - frame_dict['frame_details' , id][-2][1])
        try:
            ttc = remaining_distance/rat_velocity
        except:
            ttc = 0
    else:
        ttc = 0
    return ttc

def time_to_collision_FRD(dict,frame_rate,id):#returns seconds remaining before collision for each detected objects
    frame_dict = dict
    decided_value = 0.47
    distance_travelled = frame_dict['frame_details' , id][-1][0] - frame_dict['frame_details' , id][-2][0] #distance travelled in a frame
    distance_travelled = round(distance_travelled,3)
    if distance_travelled > 0:
        remaining_distance = decided_value - frame_dict['frame_details' , id][-1][0] #remaining distance till collision
        try:
            num_frames_left = remaining_distance/distance_travelled
            ttc = num_frames_left/frame_rate #time to contact in seconds
            ttc = round(ttc,2)
        except:
            ttc = 0
    else:
        ttc = 0
    return ttc

def detect_crash(z,id,dict,beep_list,list):
    dict['dng_frame_num',id].append(z)
    if len(dict['dng_frame_num',id]) > 1:
        if (dict['dng_frame_num',id][-1] - dict['dng_frame_num',id][-2]) < 3:
            # pygame.mixer.init()
            # pygame.mixer.music.load("beep-02.mp3")
            # pygame.mixer.music.stop()
            # pygame.mixer.music.play()
            # while pygame.mixer.music.get_busy() == True:
            print("danger!!")
            beep_list.append(z)
            if len(beep_list) == 1:
                list.append(10)
            else:
                if (beep_list[-1] - beep_list[-2]) > 100:
                    list.append(10)
            return 10
    if len(dict['dng_frame_num',id]) == 5:
        del dict['dng_frame_num',id][:-3]
