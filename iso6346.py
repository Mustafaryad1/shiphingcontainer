"""
iso 6346 shipping container code.
"""

def create(owner_code, serial, category='U'):
    
    if not(len(owner_code) == 3 and owner_code.isalpha()):
        raise ValueError(f'Invaled ISO 6346 owner code :{owner_code}')
    
    if category not in ('U','J','Z','R'):
        raise ValueError(f'Invaled ISO 6346 category Identifier :{category}')
    
    if not(len(serial)==6 and serial.isdigit()):
        raise ValueError(f'Invaled ISO 6346 serial number :{serial}')
    
    raw_code = owner_code + category + str(serial)
    full_code = raw_code + str(check_digit(raw_code))
    return full_code

def check_digit(raw_code):
    s = sum(code(char)* 2**index for index,char in enumerate(raw_code))
    return s %11 %10

def code(char):
    return int(char) if char.isdigit() else letter_code(char)

def letter_code(char):
    value = ord(char.lower()) - ord('a') +10
    return value + value //11