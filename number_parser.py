import os
import re


def get_number(filepath: str) -> str:
    """
    >>> from number_parser import get_number
    >>> get_number("/Users/Guest/AV_Data_Capture/snis-829.mp4")
    'snis-829'
    >>> get_number("/Users/Guest/AV_Data_Capture/snis-829-C.mp4")
    'snis-829'
    >>> get_number("C:¥Users¥Guest¥snis-829.mp4")
    'snis-829'
    >>> get_number("C:¥Users¥Guest¥snis-829-C.mp4")
    'snis-829'
    >>> get_number("./snis-829.mp4")
    'snis-829'
    >>> get_number("./snis-829-C.mp4")
    'snis-829'
    >>> get_number(".¥snis-829.mp4")
    'snis-829'
    >>> get_number(".¥snis-829-C.mp4")
    'snis-829'
    >>> get_number("snis-829.mp4")
    'snis-829'
    >>> get_number("snis-829-C.mp4")
    'snis-829'
    """
    filepath = os.path.basename(filepath)

    #if '-' in filepath or '_' in filepath:  # 普通提取番号 主要处理包含减号-和_的番号
    filepath = filepath.replace("_", "-")
    filename = str(re.sub(r'22-sht\.me|Carib|1080p|720p|-HD|\d{4}-\d{1,2}-\d{1,2}', '', filepath, flags = re.IGNORECASE))

    if re.search(r'FC', filename, re.I):
        digits = re.search(r'\d{6,7}', filename, re.I).group()
        return 'FC2-' + digits

    file_number = re.search(r'\w+-?\d{2,6}', filename).group().replace('-','')
    if re.search('^T28', file_number, re.I):
        digits = file_number[3:]
        letters = 'T28'
    else:
        digits = re.search(r'[0-9]+$', file_number).group()
        letters = file_number[0:len(file_number)-len(digits)]

    if (len(letters)>0) & (len(digits)>0):
        return  letters + '-' + digits
    elif re.search('^\d{9}$', file_number):
        return file_number[0:6] + '_' + file_number[6:9]
    elif re.search('^\d{8}$', file_number):
        return file_number[0:6] + '_' + file_number[6:8]
    else:
        return None

    #else:  # 提取不含减号-的番号，FANZA CID
    #    try:
    #        return str(re.findall(r'(.+?)\.', str(re.search('([^<>/\\\\|:""\\*\\?]+)\\.\\w+$', filepath).group()))).strip("['']").replace('_', '-')
    #    except:
    #        return re.search(r'(.+?)\.', filepath)[0]


if __name__ == "__main__":
    import doctest
    doctest.testmod(raise_on_error=True)
