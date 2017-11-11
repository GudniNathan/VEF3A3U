def validate(kennitala):
    k = list()
    if len(str(kennitala)) != 10:
        return False
    try:
        for c in str(kennitala):
            k.append(int(c))
    except ValueError:
        return False
    if k[8] == 11 - ((3*k[0] + 2*k[1] + 7*k[2] + 6*k[3] + 5*k[4] + 4*k[5] + 3*k[6] + 2*k[7]) % 11):
        return True
    else:
        return False