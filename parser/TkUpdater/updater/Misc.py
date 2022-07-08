import re
import configparser


def find_position(ini, target):
    config = configparser.ConfigParser()
    config.read(ini)
    return config['Config'][target]


def find_label(label_re, address, num):
    label_num = 0
    txt = open(address)
    for line in txt:
        label = re.findall(label_re, line)
        if (len(label) != 0) and (label_num == num):
            txt.close()
            return label[0]
        elif len(label) != 0:
            label_num += 1


def get_ker_seq(address):
    start_label = find_label('Label#:\s*(.+)', address, 0)
    txt = open(address, 'r')
    seq = []
    start_line = ''
    for line in txt:
        if (len(start_line) > 0) and (start_line[0] == start_label):
            seq.append(line)
        else:
            start_line = re.findall('Label#:\s*(.+)', line)
            if (len(start_line) > 0) and (start_line[0] == start_label):
                seq.append(line)
    return seq


def get_hist_seq(address):
    end_label = find_label('Label#:\s*(.+)', address, 1)
    txt = open(address, 'r')
    seq = []
    for line in txt:
        end_line = re.findall(end_label, line)
        if len(end_line) > 0:
            return seq
        seq.append(line)


def cmp_tag(tag1, tag2):
    tag1_element = tag1.split('.')
    tag2_element = tag2.split('.')
    if len(tag1_element) != 3 or len(tag2_element) != 3:
        return False
    elif tag1_element[0] != tag2_element[0]:
        return False
    elif tag1_element[1] != tag2_element[1]:
        return False
    elif tag1_element[2] != tag2_element[2]:
        return False
    else:
        return True


def position_ini_updater(ini, target, new_position):
    config = configparser.ConfigParser()
    config.read(ini)
    with open(ini, 'w') as configfile:
        config.set('Config', target, new_position)
        config.write(configfile)
