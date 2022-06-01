# convert xml to map for gi tools

import xml.etree.cElementTree as ET
from uart import *
from f_mfc import *
from data_mfc import *

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

from statistics import mean
from statistics import stdev

# data of MFC tool
NN = 24
MM = 32

Field = []
SField = []
Dev = []
SDev = []
N = []
SN = []
fi = 0


# Root window
root = tk.Tk()
root.title('Emulator MFC based to XML')



nameMAP = 0
nameXML = 0

# Log
text = tk.Text(root, height=12)
text.grid(column=0, row=0, sticky='nsew', columnspan=4)


# for mane map
seriesEntry = tk.Entry(root)
seriesEntry.grid(column=0, row=1, sticky='nsew')
seriesEntry.insert('end', 'HM')
numberEntry = tk.Entry(root)
numberEntry.grid(column=1, row=1, sticky='nsew')
numberEntry.insert('end', '4930')
viselEntry = tk.Entry(root)
viselEntry.grid(column=2, row=1, sticky='nsew')
viselEntry.insert('end', 'W')
cellEntry = tk.Entry(root)
cellEntry.grid(column=3, row=1, sticky='nsew')
cellEntry.insert('end', 'A')

def open_xml_file():
    global nameXML, SField, SDev, SN, Field, Dev, N
    # file type
    filetypes = (
        ('xml files', '*.xml'),
        ('All files', '*.*')
    )
    # show the open file dialog
    f = fd.askopenfile(filetypes=filetypes, initialdir='./@xml/')
    nameXML = f.name
    text.insert('end', '--> Read : ')
    text.insert('end', f.name)
    text.insert('end', '\n')
    tree = ET.parse(nameXML)

    freqS = tree.findall("body/dataset/measurements/measurement/freq")
    for freqI in freqS:
        Field.append(freqI.text.split())
    print("Field [MHz] = ")
    text.insert('end', '--> Field [MHz]\n')
    for m in Field:
        for n in m:
            print(n, end=', ')
        print()

    devS = tree.findall("body/dataset/measurements/measurement/stdDev")
    for devI in devS:
        Dev.append(devI.text.split())
    text.insert('end', '--> Deviation\n')
    print("Deviation [] = ")
    for m in Dev:
        for n in m:
            print(n, end=', ')
        print()

    nvS = tree.findall("body/dataset/measurements/measurement/nbValid")
    for nvI in nvS:
        N.append(nvI.text.split())
    text.insert('end', '--> Number\n')
    print("Number [] = ")
    i = 0
    for m in N:
        print(i, end=' [')
        for n in m:
            print(n, end=', ')
        print(']')
        i = i + 1

    write_MAP_button['state'] = tk.NORMAL
    text.insert('end', '--> Can write\n')

    # statistick
    fField =[]
    for i in range(len(Field)):
        for j in range(len(Field[i])):
            if Field[i][j] == 'nan':
                if Field[i][j] == Field[i][0]:  # if first
                    fff = float("{0:.12f}".format(float(Field[i][1]) * 1)) * 2 - float(
                        "{0:.12f}".format(float(Field[i][2]) * 1))
                elif Field[i][j] == Field[i][-1]:  # if lasst
                    fff = float("{0:.12f}".format(float(Field[i][-2]) * 1)) * 2 - float(
                        "{0:.12f}".format(float(Field[i][-3]) * 1))
                else:  # midle
                    fff = (float("{0:.12f}".format(float(Field[i][j - 1]) * 1)) + float(
                        "{0:.12f}".format(float(Field[i][j + 1]) * 1))) / 2
            else:
                fff = float("{0:.12f}".format(float(Field[i][j]) * 1))
            fField.append(fff)


    avgField = mean(fField)
    text.insert('end', '--> Avg Field = ' + str(avgField) + '\n')

    avgG = 30003.04056926
    k = avgG/avgField
    text.insert('end', '--> Avg Gaus = ' + str(avgG) + ': k = ' + str(k) + ': calc = ' + str(k*avgField) + '\n')
    text.insert('end', '--> Avg Field [G] = ' + str(avgField*k) + ' [30003.04056926 Gauss]\n')
    text.insert('end', '--> Min Field [G] = ' + str(min(fField)*k) + ' [29829.08171055 Gauss]\n')
    text.insert('end', '--> Max Field [G] = ' + str(max(fField) * k) + ' [30011.58498117 Gauss]\n')
    text.insert('end', '--> Standard Deviation [G] = ' + str((stdev(fField)) * k) + ' [37.46503267 Gauss]\n')
    print("Standard Deviation of the sample is % s " % (stdev(fField)))

    val, idx = min((val, idx) for (idx, val) in enumerate(fField))
    text.insert('end', '--> Min = ' + str(val * k) + '  on ' + str(idx) + '\n')
    valMax, idxMax = max((valMax, idxMax) for (idxMax, valMax) in enumerate(fField))
    text.insert('end', '--> Max = ' + str(valMax * k) + '  on ' + str(idxMax) + '\n')
    text.insert('end', '--> Max[636] = ' + str(fField[636] * k) + '  Max[' + str(idxMax) + '] = '+ str(fField[idxMax]*k) + '\n')

    for i in range(NN):
        SF = ''
        SD = ''
        SNn = ''
        for j in range(MM):

            if Field[i][j] == 'nan':
                ifff='1270000000'
            else:
                fff = float("{0:.12f}".format(float(Field[i][j]) * 10000000))
                ifff = int(fff)

            SF = SF + str(ifff) + '\r\n'

            if Dev[i][j] == 'nan':
                iddd='0.1'
            else:
                iddd = float("{0:.12f}".format(float(Dev[i][j])))

            SD = SD + str(iddd) + '\r\n'


            if N[i][j] == 'nan':
                inn='5'
            else:
                nn = float("{0:.12f}".format(float(N[i][j])))
                inn = int(nn)
            SNn = SNn + str(inn) + '\r\n'

        SF = SF + '\x17'
        print(SF.encode('ascii'))
        SField.append(SF)

        SD = SD + '\x17'
        print(SD.encode('ascii'))
        SDev.append(SD)

        SNn = SNn + '\x17'
        print(SNn.encode('ascii'))
        SN.append(SNn)

    print('####################')
    print(SField)

    print('####################')
    for ff in range(NN):

        print(str(SDev[ff]).encode('ascii'))




# open XML file button
open_XML = ttk.Button(
    root,
    text='Open XML File',
    command=open_xml_file
)
open_XML.grid(column=0, row=2, sticky='w', padx=10, pady=10)


def emu_mfc():
    global mda, mcf, mlf, mhf, mre, mdp, nsr, nsp, dbr, ncy, npc, npt, rso, rsg, tvp
    global p_run, p_src, blk, i_blk1
    global bfv, bsd, bnc, bin, dfc, bfl, bfh, bfd
    global st1, st2, st3, st4, st5, st6, sma, npr, pcf, plf, phf, rfh, nst, ver, sn, led, adv
    global fi, NN, MM, SField, Dev, N, SN, SDev



    ####
    # name of serial port
    uart = 'COM4'

    #
    f_run = False
    f_src = False
    f_brk = False
    f_led = False
    f_auto_st1 = False;
    f_auto_st4 = False;
    m_st1 = 0  # auoreg
    m_st2 = 0
    MMM = 10

    k = 0

    ser = initialise_uart(uart)
    time.sleep(0.2)
    print(ser)


    while 1:
        # uart
        uart_str = read_uart(ser)
        # print('====>> ' + str(uart_str))
        cmd, f_data, data = parser_cmd(uart_str)
        # print('~ ' + str(cmd) + ' : ' + str(data))

        # daemon cmd
        if cmd == 'NOP':
            pass

        elif cmd == 'EDP':
            print('\t<--- ERROR DATA = [' + str(data) + ']')

        # general parameters
        elif cmd == 'MDA':  # modulation amplitude
            if f_data == True:
                mda = int(data)
                print('\t<-- mda = [' + str(mda) + ']')
            else:
                push_param(mda, ser)
                print('\t--> mda = {' + str(mda) + '}')

        elif cmd == 'MCF':  # modulation central frequency
            if f_data == True:
                mcf = int(data)
                print('\t<-- mcf = [' + str(mcf) + ']')
            else:
                push_param(mcf, ser)
                print('\t--> mcf = {' + str(mcf) + '}')

        elif cmd == 'MLF':  # modulation lowest frequency
            if f_data == True:
                mlf = int(data)
                print('\t<-- mlf = [' + str(mlf) + ']')
            else:
                push_param(mlf, ser)
                print('\t--> mlf = {' + str(mlf) + '}')

        elif cmd == 'MHF':  # modulation highest frequency
            if f_data == True:
                mhf = int(data)
                print('\t<-- mhf = [' + str(mhf) + ']')
            else:
                push_param(mhf, ser)
                print('\t--> mhf = {' + str(mhf) + '}')

        elif cmd == 'MRE':  # modulation reference
            if f_data == True:
                mre = int(data)
                print('\t<-- mre = [' + str(mre) + ']')
            else:
                push_param(mre, ser)
                print('\t--> mre = {' + str(mre) + '}')

        elif cmd == 'MDP':  # modulation period
            if f_data == True:
                mdp = int(data)
                print('\t<-- mdp = [' + str(mdp) + ']')
            else:
                push_param(mdp, ser)
                print('\t--> mdp = {' + str(mdp) + '}')

        ### advansed level ----------------------------------------------------------------------------- ###
        elif cmd == 'NSR' and adv == 1:  # number of steps for ramp modification
            print('\t-----> ADV NSR ????')
        elif cmd == 'NSP' and adv == 1:  # # number of steps for plateau modification
            print('\t-----> ADV NSP ????')
        elif cmd == 'DBR' and adv == 1:  # DDS Bit
            print('\t-----> ADV DBR ????')
        ### -------------------------------------------------------------------------------------------- ###

        # measurement parameters
        elif cmd == 'NCY':  # numbers of measurement cycles
            if f_data == True:
                ncy = int(data)
                print('\t<-- ncy = [' + str(ncy) + ']')
            else:
                push_param(ncy, ser)
                print('\t--> ncy = {' + str(ncy) + '}')

        elif cmd == 'NPC':  # numbers of preliminary cycles
            if f_data == True:
                npc = int(data)
                print('\t<-- npc = [' + str(npc) + ']')
            else:
                push_param(npc, ser)
                print('\t--> npc = {' + str(npc) + '}')

        elif cmd == 'NPT':  # time duration
            if f_data == True:
                npt = int(data)
                print('\t<-- npt = [' + str(npt) + ']')
            else:
                push_param(npt, ser)
                print('\t--> npt = {' + str(npt) + '}')

        elif cmd == 'RSO':  # rejection signal offset
            if f_data == True:
                rso = int(data)
                print('\t<-- rso = [' + str(rso) + ']')
            else:
                push_param(rso, ser)
                print('\t--> rso = {' + str(rso) + '}')

        elif cmd == 'RSG':  # rejection signal gap
            if f_data == True:
                rsg = int(data)
                print('\t<-- rsg = [' + str(rsg) + ']')
            else:
                push_param(rsg, ser)
                print('\t--> rsg = {' + str(rsg) + '}')

        elif cmd == 'TVP':  # time versus precision
            if f_data == True:
                tvp = int(data)
                print('\t<-- tvp = [' + str(tvp) + ']')
            else:
                push_param(tvp, ser)
                print('\t--> tvp = {' + str(tvp) + '}')

        # data acquisition
        elif cmd == 'RUN':  # start measurement
            f_run = True
            if f_data == False:
                p_run = 100
                print('\t<--- RUN all')
                st1 = '00000000'
                st3 = '00000010'
                st4 = '00010000'
            else:
                p_run = int(data)
                print('\t--> RUN {' + str(p_run) + '}')

        elif cmd == 'SRC':  # start measurement
            f_src = True
            if f_data == False:
                p_src = 100
                print('\t<--- SRC all')
            else:
                p_src = int(data)
                print('\t--> SRC {' + str(p_src) + '}')

        elif cmd == 'CTN':  # continue measurement
            f_brk = False

        elif cmd == 'BRK':  # break measurement
            f_brk = True

        # data reading
        elif cmd == 'BLK':  # data transfer block mode
            if f_data == True:
                blk = int(data)
                print('\t<-- blk = [' + str(blk) + ']')
                if blk == 0:
                    i_blk1 = 0
            else:
                push_param(blk, ser)
                print('\t--> blk = {' + str(blk) + '}')

        elif cmd == 'BFV':  # magnetic field value
            if f_data == True:
                # ???????
                i = int(data)
                push_param(638863559, ser)
                print('\t<-- bfv[' + str(i) + '] = ' + str(638863559))
                # ???????
            else:
                if blk == 0:
                    # ????????
                    push_param(638863559, ser)
                    print('\t<-- bfv[' + str(i_blk1) + '] = ' + str(638863559))
                    i_blk1 = i_blk1 + 1
                    # ????????
                elif blk == 1:

                    ser.write(str(SField[fi]).encode('ascii'))
                    print('\t--> bfv = {', end='')
                    print(str(SField[fi]).encode('ascii'), end='')
                    print('}')


                elif blk == 2:
                    # ?????
                    pass
                    # ?????

        elif cmd == 'BSD':  # standart deviation
            if f_data == True:
                # ???????
                i = int(data)
                push_param(8, ser)
                print('\t<-- bsd[' + str(i) + '] = ' + str(8))
                # ???????
            else:
                if blk == 0:
                    # ????????
                    push_param(9, ser)
                    print('\t<-- bsd[' + str(i_blk1) + '] = ' + str(9))
                    i_blk1 = i_blk1 + 1
                    # ????????
                elif blk == 1:
                    ser.write(str(SDev[fi]).encode('ascii'))
                    print('\t--> bsd = {', end='')
                    print(str(SDev[fi]).encode('ascii'), end='')
                    print('}')
                elif blk == 2:
                    # ?????
                    pass
                    # ?????

        elif cmd == 'BNC':  # numbers of cycles
            if f_data == True:
                # ???????
                i = int(data)
                push_param(70, ser)
                print('\t<-- bnc[' + str(i) + '] = ' + str(70))
                # ???????
            else:
                if blk == 0:
                    # ????????
                    push_param(70, ser)
                    print('\t<-- bnc[' + str(i_blk1) + '] = ' + str(70))
                    i_blk1 = i_blk1 + 1
                    # ????????
                elif blk == 1:
                    ser.write(str(SN[fi]).encode('ascii'))
                    print('\t--> bnc = {', end='')
                    print(str(SN[fi]).encode('ascii'), end='')
                    print('}')

                    if fi < len(SField):
                        fi = fi + 1
                    else:
                        fi = 0
                        
                elif blk == 2:
                    # ?????
                    pass
                    # ?????

        elif cmd == 'BIN':  # individual nmr ???
            push_param(bin, ser)
            print('\t--> bin = {' + str(bin) + '}')

        elif cmd == 'BFC':  # central nmr ???
            push_param(bfc, ser)
            print('\t--> bfc = {' + str(bfc) + '}')

        elif cmd == 'BFL':  # lover nmr ???
            push_param(bfl, ser)
            print('\t--> bfl = {' + str(bfl) + '}')

        elif cmd == 'BFH':  # highest nmr ???
            push_param(bfh, ser)
            print('\t--> bfh = {' + str(bfh) + '}')

        elif cmd == 'BFL':  # diff nmr ???
            push_param(bfd, ser)
            print('\t--> bfd = {' + str(bfd) + '}')

        # status
        elif cmd == 'ST1':
            # daemon auto
            if f_auto_st1 == True:
                if m_st1 < MM:
                    m_st1 = m_st1 + 1
                else:
                    st1 = '00010000'
                    f_auto_st1 = False
                    m_st1 = 0
                    print('\t\t\t\t=st1=> :')
            else:
                st1 = '00000000'

            re = st1 + '\r\n'
            ser.write(re.encode('ascii'))
            print('\t\t\t\t=st1=> ' + str(st1))

        elif cmd == 'ST2':
            re = st2 + '\r\n'
            ser.write(re.encode('ascii'))
            # print('\t\t' + str(st2))
        elif cmd == 'ST3':
            re = st3 + '\r\n'
            ser.write(re.encode('ascii'))
            # print('\t\t' + str(st3))

        elif cmd == 'ST4':
            # daemon auto
            if f_auto_st4 == True:
                if m_st4 < MM:
                    m_st4 = m_st4 + 1
                else:
                    st4 = '00010000'
                    f_auto_st4 = False
                    m_st4 = 0
                    print('\t\t\t\t=st4=> :')
            else:
                st4 = '00000000'

            re = st4 + '\r\n'
            ser.write(re.encode('ascii'))
            print('\t\t\t\t=st4=> ' + str(st4))

        elif cmd == 'ST5':
            re = st5 + '\r\n'
            ser.write(re.encode('ascii'))

        elif cmd == 'ST6':
            re = st6 + '\r\n'
            ser.write(re.encode('ascii'))
        elif cmd == 'ERR':
            print('\n\t<-- ERR ?????\n')
        elif cmd == 'SMA':
            if f_data == True:
                tmp = int(data)
                tmp1 = '{0:b}'.format(tmp)
                sma = tmp1.rjust(8, '0')
                print('\t<-- sma = [' + str(tmp) + ']  b[' + sma + ']')
                if sma[7] == '1':
                    print("\t\t\t\t>> indicate Data Ready")
                if sma[6] == '1':
                    print("\t\t\t\t>> indicate Command Error")
                if sma[5] == '1':
                    print("\t\t\t\t>> indicate Modulation Error")
                if sma[4] == '1':
                    print("\t\t\t\t>> indicate Communication Error")
                if sma[3] == '1':
                    print("\t\t\t\t>> indicate EEPROM Error")
                if sma[2] == '1':
                    print("\t\t\t\t>> indicate Remote Button Depressed")
                if sma[1] == '1':
                    print("\t\t\t\t>> indicate Remote Button Released")
                if sma[0] == '1':
                    print("\t\t\t\t>> indicate Probe Array Not Connected")



            else:
                push_param(sma, ser)
                print('\t--> sma = {' + str(sma) + '}')

        # probe array
        elif cmd == 'NPR':
            if f_data == True:
                npr = int(data)
                print('\t<-- npr = [' + str(npr) + ']')
            else:
                push_param(npr, ser)
                print('\t--> npr = {' + str(npr) + '}')

        elif cmd == 'PCF':
            if f_data == True:
                pcf = int(data)
                print('\t<-- pcf = [' + str(pcf) + ']')
            else:
                push_param(pcf, ser)
                print('\t--> pcf = {' + str(pcf) + '}')

        elif cmd == 'PLF':
            if f_data == True:
                plf = int(data)
                print('\t<-- plf = [' + str(plf) + ']')
            else:
                push_param(plf, ser)
                print('\t--> plf = {' + str(plf) + '}')

        elif cmd == 'PHF':
            if f_data == True:
                phf = int(data)
                print('\t<-- phf = [' + str(phf) + ']')
            else:
                push_param(phf, ser)
                print('\t--> phf = {' + str(phf) + '}')

        elif cmd == 'PRF':
            if f_data == True:
                prf = int(data)
                print('\t<-- prf = [' + str(prf) + ']')
            else:
                push_param(prf, ser)
                print('\t--> prf = {' + str(prf) + '}')

        elif cmd == 'RFH':
            if f_data == True:
                rfh = int(data)
                print('\t<-- rfh = [' + str(rfh) + ']')
            else:
                push_param(rfh, ser)
                print('\t--> rfh = {' + str(rfh) + '}')

        elif cmd == 'NST':
            if f_data == True:
                nst = int(data)
                print('\t<-- nst = [' + str(nst) + ']')
            else:
                push_param(nst, ser)
                print('\t--> nst = {' + str(nst) + '}')

        # general
        elif cmd == 'RSP':  # RS232
            # ????????????????????????????????????????????????????????????????????????????
            print('\t<-- setting uart ????????')
            # ????????????????????????????????????????????????????????????????????????????

        elif cmd == 'ADV':  # ?????????????????????????????????????????????????????????????????
            if f_data == True:
                adv = int(data)
                print('\t<-- adv = [' + str(adv) + ']')
            else:
                push_param(adv, ser)
                print('\t--> adv = {' + str(adv) + '}')

        elif cmd == 'RST':  # reset of the sustem
            print('\t<-- rst uart')
            st1 = '00000000'
            st2 = '00000000'
            st3 = '00000000'
            st4 = '00000000'
            st5 = '00000010'
            st6 = '00000000'
            f_run = False
            f_brk = False
            f_led = False
            led = 0

        elif cmd == 'VER':
            push_param(ver, ser)
            print('\t--> ver = {' + str(ver) + '}')

        elif cmd == 'S/N':
            push_param(sn, ser)
            print('\t--> sn = {' + str(sn) + '}')

        elif cmd == 'LED':
            if f_data == True:
                led = int(data)
                f_led = True
                print('\t<-- led = [' + str(led) + ']')
            # else:
            # push_param(led, ser)
            # print('\t--> led = {' + str(led) + '}')

        # else:
        # print('\t<-- unknov cmd ????')
        # print('\t\t\t\t >>> ' + str(uart_str))
        # print('\t\t\t\t >>>' + str(cmd) + ' : ' + str(data))

        # daemon LED
        if f_led == True:
            if led == 0:
                print('\t\t<led OFF>')
            elif led == 1:
                print('\t\t<led auto R1>')
            elif led == 2:
                print('\t\t<led auto R2>')
            elif led == 3:
                print('\t\t<led ON>')
            elif led == 4:
                print('\t\t<led blink slow>')
                f_auto_st1 = True
                m_st1 = 0
                f_auto_st4 = True
                m_st4 = 0
            elif led == 5:
                print('\t\t<led blink fast>')
                f_auto_st1 = True
                m_st1 = 0
                f_auto_st4 = True
                m_st4 = 0
            else:
                pass
            f_led = False

        # daemon run
        if f_run == True:
            if k < 3:
                print(k)
                k = k + 1
            else:
                st1 = '00000001'
                st3 = '00000001'
                print('<-- data available')
                re = 'DR\r\n'
                ser.write(re.encode('ascii'))
                print('<-- DR')
                f_run = False
                k = 0

        # daemon search
        if f_src == True:
            if k < 3:
                print(k)
                k = k + 1
            else:
                st1 = '00000001'
                st3 = '00000001'
                print('<-- src data available')
                re = 'DR\r\n'
                ser.write(re.encode('ascii'))
                print('<-- DR')
                f_src = False
                k = 0



    ####


def tmp_vsp():

    for i in range(NN):
        SF = ''
        for j in range(MM):

            SF = SF + str(float("{0:.12f}".format(float(Field[i][j]) / 10))) + 'e+007'
            if j < 31:
                SF = SF + ', '
        print(SF)



    # standart deviation

    for i in range(NN):
        SD = ''
        for j in range(MM):
            SD = SD + str(float("{0:.12f}".format(float(Dev[i][j]))))
            if j < 31:
                SD = SD + ', '
        print(SD)



    # point
    print('\n')

    for i in range(NN):
        SP = ''
        for j in range(MM):
            SP = SP + str(int(N[i][j]))
            if j < 31:
                SP = SP + ', '
        print(SP)


    # Timestamp

    for j in range(24):
        ST = ''
        for i in range(32):
            ST = ST + '09:' + str(11 + j) + ':09_03/26/2021'
            if i < 31:
                ST = ST + ', '
        print(ST)




    text.insert('end', '<<- Finish write to MAP \n')


# open file button
write_MAP_button = ttk.Button(
    root,
    text='Emulate MFC',
    command=emu_mfc,
    state=tk.DISABLED
)


write_MAP_button.grid(column=1, row=2, sticky='w', padx=10, pady=10)


root.mainloop()

