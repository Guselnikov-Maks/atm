import easyocr

def plata(file):
    reader = easyocr.Reader(["en"])
    full_str = reader.readtext(file, detail=0)
    
    ret_str = []
    
    for slovo in full_str:
        if len(slovo) > 10:
            ret_str.append(slovo)
            
    number = len(ret_str) - 1
    return ret_str[number]

def test(file):
    reader = easyocr.Reader(["en"])
    full_str = reader.readtext(file, detail=0)
    
    kol = 0
    
    for i in full_str:
        kol += 1
        split_str = i.split()
        if len(split_str) == 1:
            if (split_str[0] == 'SNN:' or split_str[0] == 'SJN:' or split_str[0] == 'SIN:' or split_str[0] == 'SN:' or split_str[0] == 'SNN' or split_str[0] == 'SN:' or split_str[0] == 'SN' or split_str[0] == 'SIN;'):
                    #print(split_str[0])
                return full_str[kol]
                    
        if len(split_str) == 2:
            if (split_str[0] == 'SNN:' or split_str[0] == 'SJN:' or split_str[0] == 'SIN:' or split_str[0] == 'SN:' or split_str[0] == 'SNN' or split_str[0] == 'SN:' or split_str[0] == 'SN' or split_str[0] == 'SIN;'):
                    #print(split_str[1])
                kol -= 1
                return full_str[kol]