import re
import PyUpdate
import time
import os

position = 'position.ini'

history_address = PyUpdate.find_position(position, 'History.txt')
project_dsc_address = PyUpdate.find_position(position, 'Project.dsc')

new_kernel_tag = PyUpdate.find_label('Tag#:\s*(.+)', history_address, 0)

project_dsc = open(project_dsc_address, 'rb+')


while True:
    line = project_dsc.readline()

    strings = re.findall('PcdType/0{3}/Strings\s+|".*\.;(.*);"', line)

    if strings:
        version, date = strings[0].split(';')
        print 'Now version is:', version
        print 'Now date is:   ', date
        print

        now_kernel_tag = re.findall('\.(.*)\.[0-9]*$', version)[0]
        new_version = version.replace(now_kernel_tag, new_kernel_tag)

        new_chipset_tag = raw_input('Enter new chipset tag version:')
        if len(new_chipset_tag) > 1:
            now_chipset_tag = re.findall('\.([0-9]*)$', version)[0]
            new_version = new_version.replace(now_chipset_tag, new_chipset_tag)

        new_date = time.strftime('%m/%d/%Y')

        line = line.replace(version, new_version)
        line = line.replace(date, new_date)

        version, date = strings[0].split(';')
        print 'New version is:', new_version
        print 'New date is:   ', new_date
        print

        project_dsc.seek(file_position)
        project_dsc.writelines(line)
        break

    file_position = project_dsc.tell()

os.system('pause')
