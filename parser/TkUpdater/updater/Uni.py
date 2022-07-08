import re
import PyUpdate
import time

position = 'position.ini'
history_address = PyUpdate.find_position(position, 'History.txt')
project_uni_address = PyUpdate.find_position(position, 'Project.uni')

new_kernel_tag = PyUpdate.find_label('Tag#:\s*(.+)', history_address, 0)

project_uni = open(project_uni_address, 'rb+')

new_chipset_tag = raw_input('Enter new chipset tag version:')

while True:

    line = project_uni.readline().decode('UTF-16BE', 'ignore')
    if not line:
        break

    string = re.findall('#string\s*(\S*)\s*#language\sen-US\s*"(\S*)"', line)

    if string:

        org_file_position = project_uni.tell()

        if string[0][0] == u'STR_MISC_BIOS_VERSION':
            now_kernel_tag = re.findall('\S*?\.(.*)\.[0-9]*$', string[0][1])[0]

            if len(new_chipset_tag) > 1:
                now_chipset_tag = re.findall('\.([0-9]*)$', string[0][1])[0]
                line = line.replace(now_chipset_tag, new_chipset_tag)

            line = line.replace(now_kernel_tag, new_kernel_tag)
            project_uni.seek(file_position)
            project_uni.writelines(line.encode('UTF-16BE'))
            project_uni.seek(org_file_position)

        elif string[0][0] == u'STR_CCB_VERSION':
            line = line.replace(string[0][1], new_kernel_tag)
            project_uni.seek(file_position)
            project_uni.writelines(line.encode('UTF-16BE'))
            project_uni.seek(org_file_position)

        elif string[0][0] == u'STR_MISC_BIOS_RELEASE_DATE':
            new_date = time.strftime('%m/%d/%Y')
            line = line.replace(string[0][1], new_date)
            project_uni.seek(file_position)
            project_uni.writelines(line.encode('UTF-16BE'))
            project_uni.seek(org_file_position)

        elif string[0][0] == u'STR_ESRT_VERSION':
            east_kernel = new_kernel_tag.split('.')
            east_chipset = '10' + str(int(new_chipset_tag))
            east = str(int(east_kernel[0])) + str(int(east_kernel[1]) - 5) + east_kernel[2] + east_chipset
            line = line.replace(string[0][1], east)
            project_uni.seek(file_position)
            project_uni.writelines(line.encode('UTF-16BE'))
            project_uni.seek(org_file_position)

    file_position = project_uni.tell()
