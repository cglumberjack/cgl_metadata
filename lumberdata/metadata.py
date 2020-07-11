# noinspection PyUnresolvedReferences
import os
import re

# TODO I'm going to need to make a dictionary for my big list of stuff i care about and what's needed for
#  every file type....

RAF = ['EXIF:LensModel', 'MakerNotes:RawImageHeight', 'MakerNotes:RawImageWidth', 'EXIF:CreateDate', 'EXIF:ModifyDate',
       'EXIF:SerialNumber', 'Composite:Aperture', 'EXIF:FocalLength', 'EXIF:Make', 'EXIF:Model', 'EXIF:LensMake']
MOV = ['EXIF:LensModel', 'MakerNotes:RawImageHeight', 'MakerNotes:RawImageWidth', 'EXIF:CreateDate', 'EXIF:ModifyDate',
       'EXIF:SerialNumber', 'Composite:Aperture', 'EXIF:FocalLength', 'EXIF:Make', 'EXIF:Model', 'EXIF:LensMake',
       'QuickTime:VideoFrameRate', 'QuickTime:Duration']
R3D = ['ClipName', 'EdgeTC', 'EndEdgeTC', 'TotalFrames', 'FrameHeight', 'FrameWidth', 'Aperture', 'ISO', 'Date',
       'AudioSlate', 'VideoSlate', 'Camera', 'CameraModel', 'CameraPIN', 'MediaSerialNumber', 'LensSerialNumber',
       'FPS', 'AspectRatio', 'Kelvin', 'LensName', 'LensBrand', 'FocalLength', 'Shutter(deg)', 'SensorID', 'SensorName',
       'Take']


def check_exiftool():
    """
    checks if exiftool is installed.
    :return:
    """
    pass


def check_redline():
    """
    checks if redline is installed
    :return:
    """
    pass


def check_ffprobe():
    """
    checks if ffprobe is installed
    :return:
    """
    pass


def get(filein, tool='exiftool', print_output=False):
    """
    Due to issues with the exiftool module this is provided as a way to parse output directly
    from exiftool through the system commands and cglexecute. For the moment it's only designed
    to get the lumberdata for a single file.
    :param filein:
    :return: dictionary containing lumberdata from exiftool
    """
    ext = os.path.splitext(filein)[-1]
    d = {}
    if tool == 'exiftool':
        command = r'exiftool %s' % filein
        output = cgl_execute(command=command, verbose=False, print_output=print_output)
        for each in output['printout']:
            key, value = re.split("\s+:\s+", each)
            d[key] = value
        return d
    elif tool == 'ffprobe':
        command = r'%s %s' % ('ffprobe', filein)
        output = cgl_execute(command=command)
        for each in output['printout']:
            try:
                values = re.split(":\s+", each)
                key = values[0]
                values.pop(0)
                if 'Stream' in key:
                    split_v = values[1].split(',')
                    d['Image Size'] = split_v[2].split()[0]
                    d['Source Image Width'], d['Source Image Height'] = d['Image Size'].split('x')
                    d['Video Frame Rate'] = split_v[4].split(' fps')[0].replace(' ', '')
                if 'Duration' in key:
                    d['Track Duration'] = '%s s' % values[0].split(',')[0]
                value = ' '.join(values)
                d[key] = value
            except ValueError:
                print('skipping %s' % each)
        return d


def get_red_data(filein):
    """
    method for pulling lumberdata from r3d files.  REDLINE is a command line interface from RED that is required
    for this
    https://www.red.com/downloads/options?itemInternalId=16144
    :param filein:
    :return:
    """
    file_, ext_ = os.path.splitext(filein)
    if ext_.upper() == '.R3D':
        command = r'REDLINE --i %s --printMeta 1' % filein
        d = {}
        for line in os.popen(command).readlines():
            line = line.strip('\n')
            line = line.replace('\t', '')
            line = line.replace(' ', '')
            try:
                key_, value = line.split(':', 1)
                if key_ != 'None':
                    d[key_] = value
            except ValueError:
                pass
        return d

