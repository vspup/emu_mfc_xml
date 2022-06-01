# general parameters
mda = 1000 # amplitude
mcf = 638599999 # modulation central frequency
mlf = 638280969 # modulation lowest frequency
mhf = 638919292 # modulation highest frequency
mre = 0 # modulation reference 0-MDA  1-MFC  2-MLC  3-MHF
mdp = 60 # modulation period
nsr = 0
nsp = 0
dbr = 0

# measurement parameters
ncy = 70 # cycles
npc = 12 # number of preliminary cycles
npt = 600 # time duration
rso = 0 # rejection signal offset
rsg = 40 # rejection signal gap
tvp = 0 # time versus precision

# data acquisition
p_run = 100 # run all sensors (if p_run == i only i sensor)
p_src = 100 # search all sensors (if p_srs == i only i sensor)

# data reading
blk = 1 #data tansfer block mode 0-one-by-one   1-decimal  2-hexadecimal
i_blk1 = 0 # index of next blox if mode 0
# magnetic field
bfv = b'638863559\r\n638871378\r\n638880327\r\n638882921\r\n638876412\r\n638866853\r\n638862360\r\n638866792\r\n' \
      b'638874058\r\n638873910\r\n638864364\r\n638856158\r\n638858882\r\n638867511\r\n638868348\r\n638859582\r\n' \
      b'638854234\r\n638859090\r\n638864616\r\n638862078\r\n638856484\r\n638857393\r\n638864499\r\n638869939\r\n' \
      b'638869607\r\n638867136\r\n638868015\r\n638872982\r\n638878668\r\n638881255\r\n638880579\r\n638879602\r\n\x17'
# standard deviation
#bsd = b'6\r\n12\r\n6\r\n6\r\n6\r\n12\r\n12\r\n6\r\n' \
#      b'6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n12\r\n' \
#      b'6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n' \
#      b'12\r\n6\r\n6\r\n6\r\n12\r\n6\r\n6\r\n6\r\n\x17'
bsd = b'6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n' \
      b'6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n' \
      b'6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n' \
      b'6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n6\r\n\x17'
# number of cycles
bnc = b'70\r\n70\r\n70\r\n70\r\n70\r\n70\r\n70\r\n70\r\n' \
      b'70\r\n70\r\n70\r\n70\r\n70\r\n70\r\n70\r\n70\r\n' \
      b'70\r\n70\r\n70\r\n70\r\n70\r\n70\r\n70\r\n70\r\n' \
      b'70\r\n70\r\n70\r\n70\r\n70\r\n70\r\n70\r\n70\r\n\x17'
bin = 638878888 # individual frequency if point run or point srs
# ??????????????????????
bfc = mcf
bfl = mlf
bfh = mhf
bfd = mhf-mlf
# ??????????????????????

# status
st1 = '00000000'
st2 = '00000000'
st3 = '00000000'
st4 = '00000000'
st5 = '00000010'
st6 = '00000000'
sma = 0

# prove array
npr = 32 # number of array
pcf = 638599999
plf = 625799999
phf = 651399999
rfh = 0 # ????????????????????????????????????????????????????????????????????
nst = 0 # ????????????????????????????????????????????????????????????????????

ver = 'METROLAB SA Geneva, MFC-3045 Version 2.22'
sn = 2
led = 0

# adv
adv = 0





