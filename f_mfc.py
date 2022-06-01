#


def parser_cmd(inpack):
    if len(inpack) >= 3:
        tmp = inpack[0:3]
        tmp = tmp.upper()
        c = tmp.decode(encoding='UTF-8')
        f = False
        d = -1
        if len(inpack) > 3:
            if chr(inpack[3]) == ',':
                tmp = inpack[4:].decode(encoding='UTF-8')
                f = True
                d = tmp
                if tmp.isdigit() != True:
                    c = 'EDT' # wrong data
            else:
                f = False
                d = -1
    else:
        c = 'NOP'
        f = False
        d = -1

    return c, f, d

def push_param(param, port):
    outpack = str(param) + '\r\n'
    port.write(outpack.encode('ascii'))


