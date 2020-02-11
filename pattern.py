import re

text = ['E43BAR_2020_01_27__11_03_01','jhgjh','23e23de','sdad34', 'E43BAR_2020_01_27__11_33_01', 'E43BAR_2020_01_27__12_03_01', 'E43BAR_2020_01_27__12_33_01', 'E43BAR_2020_01_27__13_03_01', 'E43BAR_2020_01_27__13_33_01', 'E43BAR_2020_01_27__14_03_01','E43BAR_2020_01_27__14_33_01', 'FYG-8418_2020_01_31__13_50_23','FYG-8418_2020_01_31__14_20_23', 'FZT-6579_2020_01_15__09_46_20', 'FZT-6579_2020_01_15__10_16_20']

def check_pattern(text):
    result =[]
    for element in text:
        pattern = re.compile(r'\S{3,12}_\d{4}_\d{2}_\d{2}__\d{2}_\d{2}_\d{2}$')
        matches = pattern.findall(element)
        for i in matches:
            result.append(i)
    return result
print(check_pattern(text))
