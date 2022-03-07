# -*- coding: cp1252 -*-
###############################################################################
#                               N-BACK-TIMING TASK                            #
#                                     V.1.5                                   #
#  Author: Ignacio Polti                                                      #
#  Brain Dynamics Group - UNICOG                                              #
###############################################################################

import pygame
from pygame.locals import *
import random

# === Experiment settings =====================================================
# =============================================================================
TRIAL_GENERATOR = 20    # Number of trials per condition
RUNS = 1  # Total number of runs for the entire experiment
STIMULI = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
BACK = [0, 1, 2, 3]  # n-back conditions
# BLOCK = (n-back, TargetTime [in milliseconds])
BLOCK = [(0,30000), (0,60000), (0,90000), (1,30000), (1,60000), (1,90000),
         (2,30000), (2,60000), (2,90000), (3,30000), (3,60000), (3,90000)]
TIME_CONTROL = [30000, 30000, 30000, 30000, 60000, 60000, 60000, 60000,
                90000, 90000, 90000, 90000]
DUR = 600  # maximum stimulus duration
ISI = 500  # Inter-Stimulus_Interval
# RESP_PAUSE = 500
BG, HI = [128, 128, 128], [255, 255, 255]  # BG = background color | HI: text
INFO_COL = [0, 0, 255]
TEXT_SIZE = 200
INSTRUCTION_SIZE = 50
STRING = []
WRONG = [255, 0, 0]
CORRECT = [0, 255, 0]
RD_COL = [255, 0, 0]
RD_RADIUS = 70
W, H = 600, 600
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

# Rearranges the 1st block according to nmbr_subj
def block_generator(nmbr_subj):
    if nmbr_subj <= len(BLOCK):
        n_sub = nmbr_subj
    else:
        x = (nmbr_subj%12)
        if x == 0:
            y = (round(nmbr_subj/12))-1
        else:
            y = round(nmbr_subj/12)
        n_sub = int(nmbr_subj - y * 12)
            
    my_block = BLOCK[:]
    local = my_block.pop(n_sub)
    random.shuffle(my_block)
    my_block = [local] + my_block
    return my_block


# Prepares a sequence of stimuli
def list_stimulus(nback):
    for k in range(TRIAL_GENERATOR):
        # Conditions 1 to 3-back:
        if nback[0] >= 1:                           
            my_stimuli = STIMULI[:]                 # [1] Makes a copy of the original list of stimuli
            chunk = random.sample(my_stimuli, 10)   # [2] Extracts a random sample of 10 elements from the stimuli list
            chunk = zip(chunk, [False]*10)          # [3] Creates a tuple
        
            # Picks a random element (target) from chunk
            target,_ = random.choice(chunk[(nback[0]+1):9])

            # Creates a copy of the target selected, and add it N positions back in chunk
            index = chunk.index((target, False))
            chunk.pop(index)
            chunk.insert(index,(target, True))
            chunk.pop(index-nback[0])
            chunk.insert(index-nback[0],(target, False))

            # Adds each chunk to STRING (list of stimuli) 
            global STRING
            STRING += chunk

        # "Control" condition (0-back):
        else:
            my_stimuli = STIMULI[:]                 # [1] Makes a copy of the original list of stimuli
            my_stimuli.pop(2)                       # [2] Extracts letter "C" from the list of stimuli
            chunk = random.sample(my_stimuli, 10)   # [3] Extracts a random sample of 10 elements from the stimuli list
            chunk = zip(chunk, [False]*10)          # [4] Creates a tuple

            # Picks a random element (target) from chunk
            target,_ = random.choice(chunk)

            # Replaces the target selected with a control stimulus ('C')
            index = chunk.index((target, False))
            chunk.pop(index)
            chunk.insert(index,('C', True))

            # Adds each chunk to STRING (list of stimuli) 
            global STRING
            STRING += chunk

    back = nback[0]
    if back > 0:
        idx = back
        for i,j in STRING[back:]:
            if i == STRING[idx-back][0]:
                STRING.pop(idx)
                STRING.insert(idx,(i, True))
                print(idx, i, file=h)
            else:
                i == i
                print(idx, 'ok', file=h)
            idx = idx + 1
	
    assert len(STRING) == TRIAL_GENERATOR*10, "chunks missing from STRING"     # Checks total amount of chunks in STRING


def key_press():
    key_pressed = False
    while not key_pressed:
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    raise Exception
                else:
                    key_pressed = True


# "Resting point" for the participant between conditions
def pause():
    run_pause1 = "PAUSE"
    run_pause2 = "Pour continuer, appuyez sur Entrée"
    pygame.event.get()
    window.fill(BG)
    font_instr = pygame.font.Font(None, INSTRUCTION_SIZE)
    image1 = font.render(run_pause1, True, HI, BG)
    size1 = image1.get_size()
    image2 = font_instr.render(run_pause2, True, HI, BG)
    size2 = image2.get_size()
    window.blit(image1, [W/2 - size1[0]/2, H/3 - size1[1]/2])
    window.blit(image2, [W/2 - size2[0]/2, H/2 - size2[1]/2])
    pygame.display.flip()
    key_press()


def presentation(nback):    # Condition INFO
    if nback[0] == 0:
        condition = 'Cible = C'
    elif nback[0] == 1:
        condition = 'N-Back = 1'
    elif nback[0] == 2:
        condition = 'N-Back = 2'
    elif nback[0] == 3:
        condition = 'N-Back = 3'
    else:
        print('presentation ERROR')

    pygame.event.get()
    window.fill(BG)
    font_image2 = pygame.font.Font(None, INSTRUCTION_SIZE)
    image = font.render(condition, True, HI, BG)
    image2 = font_image2.render('Pour continuer, appuyez sur la barre espace', True, HI, BG)
    size = image.get_size()
    size2 = image2.get_size()
    window.blit(image, [W/2 - size[0]/2, H/2 - size[1]/2])
    window.blit(image2, [W/2 - size2[0]/2, H/1.2 - size2[1]/2])
    pygame.display.flip()
    key_press()


def red_dot():
    window.fill(BG)
    pygame.draw.circle(window, RD_COL, [W/2, H/2], RD_RADIUS)
    pygame.display.flip()
    pygame.time.delay(1000)


def draw_images(stim, col):     # Prepares and shows on screen list of corresponding stimuli images
    image = font.render(stim, True, col, BG)
    size = image.get_size()
    window.blit(image, [W/2 - size[0]/2, H/2 - size[1]/2])
    pygame.display.flip()


def check_user_input(col, stim, no_time, counter_init):
    events = pygame.event.get()
    for ev in events:
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                if not stim:    # Allows only one key pressing per stimulus shown on screen
                    reaction_time = pygame.time.get_ticks() - counter_init
                    return WRONG, False, reaction_time      # [1] If partipant press space-bar when NO TARGET is on screen, change stimulus color to RED
                reaction_time = pygame.time.get_ticks() - counter_init
                return CORRECT, True, reaction_time         # [2] If partipant press space-bar when TARGET is on screen, change stimulus color to GREEN
            elif ev.key == K_ESCAPE:
                raise Exception
    return col, None, no_time   # [3] If participant doesn't press a key, stimulus shown on screen remains with default values (color, response and RT)


def time_question():
    pygame.init()
    time_estimate = ""
    counter_init = pygame.time.get_ticks()
    while True:
        for ev in pygame.event.get():
            if ev.type == KEYDOWN:
                if ev.unicode.isdigit():
                    time_estimate += ev.unicode
                    if len(time_estimate) == 2:
                        time_estimate += ':'
                elif ev.key == K_BACKSPACE:
                    time_estimate = time_estimate[:-1]
                elif ev.key == K_RETURN or K_KP_ENTER:
                    try:
                        reaction_time = pygame.time.get_ticks() - counter_init
                        t_est_1 = int(time_estimate[:2])
                        t_est_2 = int(time_estimate[3:])
                        if t_est_2 > 59:
                            time_estimate = ""
                        else:
                            time_estimate = (60*t_est_1) + t_est_2
                            print(nmbr_subj, subj, run, indx, nback[0],
                                  nback[1], 'T_ESTIMATE', None, None,
                                  reaction_time, None, time_estimate, file=f)
                            return time_estimate
                    except ValueError:
                        time_estimate = ""
                elif ev.key == K_ESCAPE:
                    raise Exception
                
        window.fill(BG)
        font_instr = pygame.font.Font(None, INSTRUCTION_SIZE)
        instruction1 = font_instr.render("Combien de temps s'est-il écoulé", True, HI)
        instruction2 = font_instr.render("entre les deux ronds rouges?", True, HI)
        instruction3 = font_instr.render("Utilisez les nombres activés par 'MAJ' pour", True, HI)
        instruction4 = font_instr.render("répondre en minutes et en secondes", True, HI)
        instruction5 = font_instr.render("mm    :    ss", True, HI)
        instruction6 = font_instr.render("Une fois que vous avez fini, appuyez sur Entrée", True, HI)
        instr1_size = instruction1.get_size()
        instr2_size = instruction2.get_size()
        instr3_size = instruction3.get_size()
        instr4_size = instruction4.get_size()
        instr5_size = instruction5.get_size()
        instr6_size = instruction6.get_size()
        answer_block = font.render(time_estimate, True, HI)
        rect = answer_block.get_rect()
        rect.center = window.get_rect().center
        window.blit(instruction1, [W/2 - instr1_size[0]/2, H/6 - instr1_size[1]/2])
        window.blit(instruction2, [W/2 - instr2_size[0]/2, H/4.7 - instr2_size[1]/2])
        window.blit(instruction3, [W/2 - instr3_size[0]/2, H/3.5 - instr3_size[1]/2])
        window.blit(instruction4, [W/2 - instr4_size[0]/2, H/3 - instr4_size[1]/2])
        window.blit(instruction5, [W/2 - instr5_size[0]/2, H/2.5 - instr5_size[1]/2])
        window.blit(instruction6, [W/2 - instr6_size[0]/2, H/1.2 - instr6_size[1]/2])
        window.blit(answer_block, rect)
        pygame.display.flip()
                                      

def main_loop(nmbr_subj, subj, nback, counter_general):
    pygame.init()
    
    for trial, stim in enumerate(STRING, start=1):
        if stim[1] == True:
            response = 'Miss'
        else:
            response = None # Default response

        col = HI    # Default color of stimulus
        no_time = None  # Default RT

        counter_init = pygame.time.get_ticks()
        while (pygame.time.get_ticks() - counter_init) < DUR:    # [1] Counts time until maximum stimulus duration is reached (DUR)
            window.fill(BG)
            draw_images(stim[0], col)  # [2] Shows stimulus on screen
            col, resp, reaction_time = check_user_input(col, stim[1], no_time, counter_init)  # [3] Checks participant's response

            if response is None or 'Miss' and resp is not None:   # [4] If there's a response, updates the response value
                response = resp
                if no_time is None and reaction_time is not None:   # [5] If there's a response, updates the RT value
                    no_time = reaction_time

        #Interstimulus Interval (ISI)    
        window.fill(BG)
        pygame.display.flip()
        pygame.time.wait(ISI)

        time_estimate = None
        print(nmbr_subj, subj, run, indx, nback[0], nback[1], trial,
              stim[0], response, no_time,
              (pygame.time.get_ticks() - counter_general), time_estimate,
              file=f)

        if (pygame.time.get_ticks() - counter_general) >= nback[1]:     # Time interval counter
            break   


def control_instruction():
    window.fill(BG)
    ctrl_size = 60
    font_instr = pygame.font.Font(None, ctrl_size)
    instruction1 = font_instr.render("Fixez la croix.", True, HI)
    instruction2 = font_instr.render("Vous allez estimer le temps écoulé", True, HI)
    instruction3 = font_instr.render("entre les deux apparitions du rond rouge.", True, HI)
    instruction4 = font_instr.render("Pour continuer, appuyez sur Entrée", True, HI)
    instr1_size = instruction1.get_size()
    instr2_size = instruction2.get_size()
    instr3_size = instruction3.get_size()
    instr4_size = instruction4.get_size()
    window.blit(instruction1, [W/2 - instr1_size[0]/2, H/3 - instr1_size[1]/2])
    window.blit(instruction2, [W/2 - instr2_size[0]/2, H/2 - instr2_size[1]/2])
    window.blit(instruction3, [W/2 - instr3_size[0]/2, H/1.8 - instr3_size[1]/2])
    window.blit(instruction4, [W/2 - instr4_size[0]/2, H/1.2 - instr4_size[1]/2])
    pygame.display.flip()
    key_press()


def control_interval(intv):
    window.fill(BG)
    fix_cross = font.render("+", True, HI)
    cross_size = fix_cross.get_size()
    window.blit(fix_cross, [W/2 - cross_size[0]/2, H/2 - cross_size[1]/2])
    pygame.display.flip()
    pygame.time.delay(intv)


def control_time_question(trial, intv):
    pygame.init()
    time_estimate = ""
    counter_init = pygame.time.get_ticks()
    while True:
        for ev in pygame.event.get():
            if ev.type == KEYDOWN:
                if ev.unicode.isdigit():
                    time_estimate += ev.unicode
                    if len(time_estimate) == 2:
                        time_estimate += ':'
                elif ev.key == K_BACKSPACE:
                    time_estimate = time_estimate[:-1]
                elif ev.key == K_RETURN or K_KP_ENTER:
                    try:
                        reaction_time = pygame.time.get_ticks() - counter_init
                        t_est_1 = int(time_estimate[:2])
                        t_est_2 = int(time_estimate[3:])
                        if t_est_2 > 59:
                            time_estimate = ""
                        else:
                            time_estimate = (60*t_est_1) + t_est_2
                            print(nmbr_subj, subj, trial, intv,
                                  reaction_time, time_estimate, file=g)
                            return time_estimate
                    except ValueError:
                        time_estimate = ""
                elif ev.key == K_ESCAPE:
                    raise Exception
    
        window.fill(BG)
        font_instr = pygame.font.Font(None, INSTRUCTION_SIZE)
        instruction1 = font_instr.render("Combien de temps s'est-il écoulé", True, HI)
        instruction2 = font_instr.render("entre les deux ronds rouges?", True, HI)
        instruction3 = font_instr.render("Utilisez les nombres activés par 'MAJ' pour", True, HI)
        instruction4 = font_instr.render("répondre en minutes et en secondes", True, HI)
        instruction5 = font_instr.render("mm    :    ss", True, HI)
        instruction6 = font_instr.render("Une fois que vous avez fini, appuyez sur Entrée", True, HI)
        instr1_size = instruction1.get_size()
        instr2_size = instruction2.get_size()
        instr3_size = instruction3.get_size()
        instr4_size = instruction4.get_size()
        instr5_size = instruction5.get_size()
        instr6_size = instruction6.get_size()
        answer_block = font.render(time_estimate, True, HI)
        rect = answer_block.get_rect()
        rect.center = window.get_rect().center
        window.blit(instruction1, [W/2 - instr1_size[0]/2, H/6 - instr1_size[1]/2])
        window.blit(instruction2, [W/2 - instr2_size[0]/2, H/4.7 - instr2_size[1]/2])
        window.blit(instruction3, [W/2 - instr3_size[0]/2, H/3.5 - instr3_size[1]/2])
        window.blit(instruction4, [W/2 - instr4_size[0]/2, H/3 - instr4_size[1]/2])
        window.blit(instruction5, [W/2 - instr5_size[0]/2, H/2.5 - instr5_size[1]/2])
        window.blit(instruction6, [W/2 - instr6_size[0]/2, H/1.2 - instr6_size[1]/2])
        window.blit(answer_block, rect)
        pygame.display.flip()

    
def control():
    t_ctrl = TIME_CONTROL[:]
    random.shuffle(t_ctrl)
    pygame.init()
    for trial, intv in enumerate(t_ctrl, start=1):
        control_instruction()
        red_dot()
        control_interval(intv)
        red_dot()
        control_time_question(trial, intv)


def merci():
    window.fill(BG)
    font_merci = pygame.font.Font(None, INSTRUCTION_SIZE)
    merci_m = font_merci.render("Merci pour votre participation!", True, HI)
    merci_size = merci_m.get_size()
    window.blit(merci_m, [W/2 - merci_size[0]/2, H/2 - merci_size[1]/2])
    pygame.display.flip()
    key_press()

# === MAIN EXPERIMENT STRUCTURE ===============================================
# =============================================================================
try:
    while True:
        try:
            nmbr_subj = int(raw_input('Subject number: '))   # Subject number
            break
        except ValueError:
            print('Invalid character. Please write a number')
    subj = raw_input('subject (no spaces): ')   # Participant's name
    f = open('data_' + subj + '_TIME.txt', 'w')
    print('Nro_SUBJ', 'SUBJ', 'RUN', 'BLOCK', 'BACK', 'TIME', 'TRIAL', 'STIM',
          'ANSWER', 'RT', 'COUNTER', 'RESP_QUESTION', file=f)
    g = open('IntervalCONTROLdata_' + subj + '_TIME.txt', 'w')
    print('Nro_SUBJ', 'SUBJ', 'TRIAL', 'INTERVAL', 'RT', 'ESTIMATE', file=g)
    h = open(subj + 'data_analysis.txt', 'w')
    print('INFO', 'STIM', file=h)
    for run in range(RUNS):
        if run == 0:
            my_block = block_generator(nmbr_subj)
            for indx, nback in enumerate(my_block, start=1):
                list_stimulus(nback)    # Creates stimuli set according to N-BACK condition
                pygame.init() 
                pygame.mouse.set_visible(False)
                
                # Creates full-screen window and font
                #window = pygame.display.set_mode((W,H))
                window = pygame.display.set_mode([0, 0], FULLSCREEN | DOUBLEBUF | HWSURFACE)
                W, H = window.get_size()
                font = pygame.font.Font(None, TEXT_SIZE)
                window.fill(BG)
                pygame.display.flip()

                presentation(nback) # Shows N-BACK condition
                red_dot()
                counter_general = pygame.time.get_ticks()
                main_loop(nmbr_subj, subj, nback, counter_general)
                red_dot()
                time_question()
                STRING = []
        else:
            alt_block = BLOCK[:]
            random.shuffle(alt_block)
            pause()
            for indx, nback in enumerate(alt_block, start=1):
                list_stimulus(nback)    # Creates stimuli set according to N-BACK condition
                pygame.init() 
                pygame.mouse.set_visible(False)
                
                # Creates full-screen window and font
                #window = pygame.display.set_mode((W,H))
                window = pygame.display.set_mode([0, 0], FULLSCREEN | DOUBLEBUF | HWSURFACE)
                W, H = window.get_size()
                font = pygame.font.Font(None, TEXT_SIZE)
                window.fill(BG)
                pygame.display.flip()

                presentation(nback) # Shows N-BACK condition
                red_dot()
                counter_general = pygame.time.get_ticks()
                main_loop(nmbr_subj, subj, nback, counter_general)
                red_dot()
                time_question()
                STRING = []
    pause()
    control()
    merci()
    
finally:
    f.close()
    g.close()
    h.close()
    pygame.quit()
