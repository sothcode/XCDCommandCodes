#! /usr/bin/python3

import os
import sys
import time
from quickReport import readback
from changeAxisDogleg import changeAxis
from gotoDogleg import gotoDogleg
from clearDogleg import clearDogleg

# SET DEFAULT GLOBAL VARIABLES
lb = -2.9   # low bound to travel to
hb = 2.9    # high bound to travel to
ss = 0.1    # step size to take in search
ns = 10     # numsteps to take

# set reset command - just run shell script
curl_pref = 'curl -o ./scopeTraces/st'
curl_suff = ' http://10.20.35.4:81/image.png'

def gridSearch( test_axis ):

    # label axes to move from input axis
    DL0_A0 = test_axis + 'DL0_A0'
    DL0_A1 = test_axis + 'DL0_A1'
    DL1_A0 = test_axis + 'DL1_A0'
    DL1_A1 = test_axis + 'DL1_A1'


    # start by moving chosen dogleg to (-2.9, 2.9)
    init_A0 = changeAxis(DL0_A0)
    goto_A0, pos0 = gotoDogleg(lb)
    init_A1 = changeAxis(DL0_A1)
    goto_A1, pos1 = gotoDogleg(lb)
    if not (init_A0 and goto_A0 and init_A1 and goto_A1):
        return

    # define initial moves
    move_A0 = hb
    move_A1 = lb + ss

    # 
    for i in range(ns):

        # change to DL0
        didChange_A0 = changeAxis(DL0_A0)
        if not didChange_A0:
            print("findDiode change to A0 failed on step ", i)
            return

        # move A0 from to either lb or hb
        didGoto_A0, pos0 = gotoDogleg(move_A0)
        if not didGoto_A0:
            if pos0 == 0:
                print("findDiode A0 move step ", i, " to ", pos0, " failed.")
                return
            else:
                x = input("gotoDogleg failed with above status. Press enter to clear or any other key then enter to abort.")
                if x != "":
                    return
                else:
                    clearDogleg()


        # change to DL1
        didChange_A1 = changeAxis(DL0_A1)
        if not didChange_A1:
            print("findDiode change to A1 failed on step ", i)
            return

        # move A1 up by step size ss
        didGoto_A1, pos1 = gotoDogleg(move_A1)
        if not didGoto_A1:
            if pos1 == 0:
                print("findDiode A1 move step ", i, " to ", pos1, " failed.")
                return
            else:
                x = input("gotoDogleg failed with above status. Press enter to clear or any other key then enter to abort.")
                if x != "":
                    return
                else:
                    clearDogleg()


        x = input("Press enter to perform next move.  Press any key then enter to abort.")
        if x != "":
            return
        else:
            move_A0 = -1*move_A0
            move_A1 = move_A1 + ss

    print("findDiode:gridSearch finished.")

    return


def wrapGoto(position, dummy=True):
    if dummy:
        print("gotoDogleg " + str(position))
        return True, position
    else:
        didGoto, pos = gotoDogleg(position)
        return didGoto, pos
    
def wrapChangeAxis(axis, dummy=True):
    if dummy:
        print("changeAxis " + str(axis))
        return True
    else:
        didChange = changeAxis(axis)
        return didChange




def spiralSearch(test_axis, x_DL00:float=0.0, x_DL01:float=0.0, x_DL10:float=0.0, x_DL11:float=0.0, ns0:int=ns, \
                 ns1:int=ns, step_size:int=ss, autorun:bool=True, img_bool:bool=True):

    # label axes to move from input axis
    DL0_A0 = test_axis + 'DL0_A0'
    DL0_A1 = test_axis + 'DL0_A1'
    DL1_A0 = test_axis + 'DL1_A0'
    DL1_A1 = test_axis + 'DL1_A1'

    # start by moving first dogleg to (x_DL00,x_DL01), default (0,0)
    init_DL00 = wrapChangeAxis(DL0_A0)
    goto_DL00, pos00 = wrapGoto(x_DL00)
    init_DL01 = wrapChangeAxis(DL0_A1)
    goto_DL01, pos01 = wrapGoto(x_DL01)
    if not (init_DL00 and goto_DL00 and init_DL01 and goto_DL01):
        return
    
    # start by moving chosen dogleg to (x_DL10,x_DL11), default (0,0)
    init_DL10 = wrapChangeAxis(DL1_A0)
    goto_DL10, pos10 = wrapGoto(x_DL10)
    init_DL11 = wrapChangeAxis(DL1_A1)
    goto_DL11, pos11 = wrapGoto(x_DL11)
    if not (init_DL10 and goto_DL10 and init_DL11 and goto_DL11):
        return

    # save first image
    count:int = 0
    filename = str(count) + '_' + "{:.4f}".format(x_DL00) + '_' + "{:.4f}".format(x_DL01) + \
                '_' + "{:.4f}".format(x_DL10) + '_' + "{:.4f}".format(x_DL11) + '.png'
    img_save = curl_pref + filename + curl_suff
    os.system(img_save)
    count += 1

    # calculate initial moves
    innerstep = -1*step_size
    outerstep = -1*step_size
    mv_DL00 = x_DL00
    mv_DL01 = x_DL01
    mv_DL10 = x_DL10
    mv_DL11 = x_DL11

    # spiral for upstream dogleg DL0
    for i in range(ns0):

        # change to DL0_A0, return if failed
        didChange_DL00 = wrapChangeAxis(DL0_A0)
        if not didChange_DL00:
            print("findDiode:spiralSearch change to DL0_A0 failed on step ", i)
            return
        for ii in range(i+1):
            # increase (or decrease) move by one step
            mv_DL00 = mv_DL00 + outerstep
            # move DL0_A0 from spiral center to first step
            didGoto_DL00, pos00 = wrapGoto(mv_DL00)
            if not didGoto_DL00:
                if pos00 == 0:
                    print("findDiode:spiralSearch DL0_A0 move step ", i, " to ", pos00, " failed.")
                    return
                else:
                    x = input("gotoDogleg failed with above status. Press enter to clear or any other key then enter to abort.")
                    if x != "":
                        return
                    else:
                        clearDogleg()
            # take picture if we want pics
            if img_bool:
                filename = str(count) + '_' + str(f"{mv_DL00:.4f}") + '_' + str(f"{mv_DL01:.4f}") + \
                            '_' + str(f"{mv_DL10:.4f}") + '_' + str(f"{mv_DL11:.4f}") + '.png'
                img_save = curl_pref + filename + curl_suff
                os.system(img_save)
                count += 1
            # stop in between each move if autorun not turned on
            if not autorun:
                x = input("Press enter to perform next move.  Press any key then enter to abort.")
                if x != "":
                    return

            # spiral for downstream dogleg DL1
            for j in range(ns1):

                # change to DL1_A0
                didChange_DL10 = wrapChangeAxis(DL1_A0)
                if not didChange_DL10:
                    print("findDiode:spiralSearch change to DL1_A0 failed on step ", i)
                    return
                for jj in range(j+1):
                    # increase (or decrease) move by one step
                    mv_DL10 = mv_DL10 + innerstep
                    # move DL1_A0 to new move
                    didGoto_DL10, pos10 = wrapGoto(mv_DL10)
                    if not didGoto_DL10:
                        if pos10 == 0:
                            print("findDiode:spiralSearch failed in DL1_A0 move step ", j, " to ", pos10, ".")
                            return
                        else:
                            x = input("gotoDogleg failed with above status. Press enter to clear or any other key then enter to abort.")
                            if x != "":
                                return
                            else:
                                clearDogleg()
                    # take picture if we want pics
                    if img_bool:
                        filename = str(count) + '_' + str(f"{mv_DL00:.4f}") + '_' + str(f"{mv_DL01:.4f}") + \
                                    '_' + str(f"{mv_DL10:.4f}") + '_' + str(f"{mv_DL11:.4f}") + '.png'
                        img_save = curl_pref + filename + curl_suff
                        os.system(img_save)
                        count += 1
                    # stop in between each move if autorun not turned on
                    if not autorun:
                        x = input("Press enter to perform next move.  Press any key then enter to abort.")
                        if x != "":
                            return

                # change to DL1_A1
                didChange_DL11 = wrapChangeAxis(DL1_A1)
                if not didChange_DL11:
                    print("findDiode change to DL1_A1 failed on step ", j)
                    return
                for jj in range(j+1):
                    # increase (or decrease) move by one step
                    mv_DL11 = mv_DL11 + innerstep
                    # move A1 up by step size ss
                    didGoto_DL11, pos11 = wrapGoto(mv_DL11)
                    if not didGoto_DL11:
                        if pos11 == 0:
                            print("findDiode DL1_A1 failed in move step ", i, " to ", pos11, ".")
                            return
                        else:
                            x = input("gotoDogleg failed with above status. Press enter to clear or any other key then enter to abort.")
                            if x != "":
                                return
                            else:
                                clearDogleg()
                    # take picture if we want pics
                    if img_bool:
                        filename = str(count) + '_' + str(f"{mv_DL00:.4f}") + '_' + str(f"{mv_DL01:.4f}") + \
                                    '_' + str(f"{mv_DL10:.4f}") + '_' + str(f"{mv_DL11:.4f}") + '.png'
                        img_save = curl_pref + filename + curl_suff
                        os.system(img_save)
                        count += 1
                    # stop in between each move if autorun not turned on
                    if not autorun:
                        x = input("Press enter to perform next move.  Press any key then enter to abort.")
                        if x != "":
                            return

                innerstep = -1*innerstep

        # change to DL0_A1, return if failed
        didChange_DL01 = wrapChangeAxis(DL0_A1)
        if not didChange_DL01:
            print("findDiode change to DL0_A1 failed on step ", i)
            return
        for ii in range(i+1):
            # increase (or decrease) move by one step
            mv_DL01 = mv_DL01 + outerstep
            # move A1 up by step size ss
            didGoto_DL01, pos01 = wrapGoto(mv_DL01)
            if not didGoto_DL01:
                if pos01 == 0:
                    print("findDiode DL1_A1 failed in move step ", i, " to ", pos01, ".")
                    return
                else:
                    x = input("gotoDogleg failed with above status. Press enter to clear or any other key then enter to abort.")
                    if x != "":
                        return
                    else:
                        clearDogleg()
            # take picture if we want pics
            if img_bool:
                filename = str(count) + '_' + str(f"{mv_DL00:.4f}") + '_' + str(f"{mv_DL01:.4f}") + \
                            '_' + str(f"{mv_DL10:.4f}") + '_' + str(f"{mv_DL11:.4f}") + '.png'
                img_save = curl_pref + filename + curl_suff
                os.system(img_save)
                count += 1
            # stop in between each move if autorun not turned on
            if not autorun:
                x = input("Press enter to perform next move.  Press any key then enter to abort.")
                if x != "":
                    return

            # spiral for downstream dogleg DL1
            for j in range(ns1):

                # change to DL1_A0
                didChange_DL10 = wrapChangeAxis(DL1_A0)
                if not didChange_DL10:
                    print("findDiode:spiralSearch change to DL1_A0 failed on step ", i)
                    return
                for jj in range(j+1):
                    # increase (or decrease) move by one step
                    mv_DL10 = mv_DL10 + innerstep
                    # move DL1_A0 to 
                    didGoto_DL10, pos10 = wrapGoto(mv_DL10)
                    if not didGoto_DL10:
                        if pos10 == 0:
                            print("findDiode:spiralSearch failed in DL1_A0 move step ", j, " to ", pos10, ".")
                            return
                        else:
                            x = input("gotoDogleg failed with above status. Press enter to clear or any other key then enter to abort.")
                            if x != "":
                                return
                            else:
                                clearDogleg()
                    # take picture if we want pics
                    if img_bool:
                        filename = str(count) + '_' + str(f"{mv_DL00:.4f}") + '_' + str(f"{mv_DL01:.4f}") + \
                                    '_' + str(f"{mv_DL10:.4f}") + '_' + str(f"{mv_DL11:.4f}") + '.png'
                        img_save = curl_pref + filename + curl_suff
                        os.system(img_save)
                        count += 1
                    # stop in between each move if autorun not turned on
                    if not autorun:
                        x = input("Press enter to perform next move.  Press any key then enter to abort.")
                        if x != "":
                            return
                    

                # change to DL1_A1
                didChange_DL11 = wrapChangeAxis(DL1_A1)
                if not didChange_DL11:
                    print("findDiode change to DL1_A1 failed on step ", j)
                    return
                for jj in range(j+1):
                    # increase (or decrease) move by one step
                    mv_DL11 = mv_DL11 + innerstep
                    # move A1 up by step size ss
                    didGoto_DL11, pos11 = wrapGoto(mv_DL11)
                    if not didGoto_DL11:
                        if pos11 == 0:
                            print("findDiode DL1_A1 failed in move step ", i, " to ", pos11, ".")
                            return
                        else:
                            x = input("gotoDogleg failed with above status. Press enter to clear or any other key then enter to abort.")
                            if x != "":
                                return
                            else:
                                clearDogleg()
                    # take picture if we want pics
                    if img_bool:
                        filename = str(count) + '_' + str(f"{mv_DL00:.4f}") + '_' + str(f"{mv_DL01:.4f}") + \
                                    '_' + str(f"{mv_DL10:.4f}") + '_' + str(f"{mv_DL11:.4f}") + '.png'
                        img_save = curl_pref + filename + curl_suff
                        os.system(img_save)
                        count += 1
                    # stop in between each move if autorun not turned on
                    if not autorun:
                        x = input("Press enter to perform next move.  Press any key then enter to abort.")
                        if x != "":
                            return

                innerstep = -1*innerstep

        outerstep = -1*outerstep

    print('findDiode:spiralSearch completed.')

    return



if __name__ == "__main__":
    #check args
    if len(sys.argv) == 2:
        axis = sys.argv[1]
        spiralSearch(axis)
    elif len(sys.argv) == 11:
        axis, x_DL00, x_DL01, x_DL10, x_DL11, ns0, ns1, step_size, autorun, img_bool = sys.argv[1:11]
        spiralSearch(axis, x_DL00, x_DL01, x_DL10, x_DL11, ns0, ns1, step_size, autorun, img_bool)
    else:
        print("findDiode.py WRONG ARGS")
        sys.exit()
