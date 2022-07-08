import re
import time
import Tkinter
import tkMessageBox
import tkFileDialog
from updater import Misc as Updater


class Update:

    def __init__(self, master):
        master.title('PyUpdate GUI')
        master.geometry("800x400+30+30")
        self.position_ini = 'position.ini'

        file_list = ['Kernel.txt', 'History.txt', 'Project.dsc', 'Project.uni']
        browse_list = [self.kernel_browser, self.history_browser, self.project_dsc_browser, self.project_uni_browser]

        self.entry_kernel = Tkinter.Entry(master)
        self.entry_history = Tkinter.Entry(master)
        self.entry_project_dsc = Tkinter.Entry(master)
        self.entry_project_uni = Tkinter.Entry(master)

        entry_list = [self.entry_kernel, self.entry_history, self.entry_project_dsc, self.entry_project_uni]

        for index in range(len(file_list)):
            place_y = 80 + index * 40
            Tkinter.Label(master, text=file_list[index]).place(x=30, y=place_y, width=80, height=30)
            Tkinter.Button(master, text='Browse', command=browse_list[index]).place(x=710, y=place_y, width=80, height=30)
            entry_list[index].place(x=110, y=place_y, width=600, height=30)
            entry_list[index].insert(0, Updater.find_position(self.position_ini, file_list[index]))

        Tkinter.Label(master, text='Chipset Tag').place(x=30, y=30, width=80)
        self.entry_chipset_tag = Tkinter.Entry(master)
        self.entry_chipset_tag.place(x=110, y=30, width=50)
        self.entry_chipset_tag.insert(0, Updater.find_position(self.position_ini, 'Chipset_Tag'))

        Tkinter.Button(master, text='Confirm', command=self.confirm).place(x=710, y=300, width=80, height=30)

        self.kernel_last_tag = ''
        self.history_last_tag = ''

        self.message_box_content = ''

    def kernel_browser(self):
        name = tkFileDialog.askopenfilename()
        if name:
            self.entry_kernel.delete(0, 'end')
            self.entry_kernel.insert(0, name)

    def history_browser(self):
        name = tkFileDialog.askopenfilename()
        if name:
            self.entry_history.delete(0, 'end')
            self.entry_history.insert(0, name)

    def project_dsc_browser(self):
        name = tkFileDialog.askopenfilename()
        if name:
            self.entry_project_dsc.delete(0, 'end')
            self.entry_project_dsc.insert(0, name)

    def project_uni_browser(self):
        name = tkFileDialog.askopenfilename()
        if name:
            self.entry_project_uni.delete(0, 'end')
            self.entry_project_uni.insert(0, name)

    def kernel_update(self):

        update_status_str = 'failed'
        if not Updater.cmp_tag(self.kernel_last_tag, self.history_last_tag):
            history_sequence = Updater.get_hist_seq(self.entry_history.get())
            kernel_sequence = Updater.get_ker_seq(self.entry_kernel.get())

            kernel = open(self.entry_kernel.get(), 'w+')
            kernel.writelines(history_sequence)
            kernel = open(self.entry_kernel.get(), 'a')
            kernel.writelines(kernel_sequence)
            update_status_str = 'succeeded'
        self.message_box_content += ('Update Kernel.txt ' + update_status_str + '.\n')

    def project_dsc_update(self):
        project_dsc = open(self.entry_project_dsc.get(), 'rb+')

        while True:
            line = project_dsc.readline()

            strings = re.findall('PcdType/0{3}/Strings\s+|".*\.;(.*);"', line)

            if strings:
                version, date = strings[0].split(';')
                self.message_box_content += '\nNow version is: ' + version \
                                            + '\nNow date is:      ' + date + '\n'

                now_kernel_tag = re.findall('\.(.*)\.[0-9]*$', version)[0]
                new_version = version.replace(now_kernel_tag, self.history_last_tag)

                new_chipset_tag = self.entry_chipset_tag.get()
                if len(new_chipset_tag) > 1:
                    now_chipset_tag = re.findall('\.([0-9]*)$', version)[0]
                    new_version = new_version.replace(now_chipset_tag, new_chipset_tag)

                new_date = time.strftime('%m/%d/%Y')

                line = line.replace(version, new_version)
                line = line.replace(date, new_date)

                version, date = strings[0].split(';')
                self.message_box_content += '\nNew version is: ' + new_version \
                                            + '\nNew date is:      ' + new_date + '\n'

                project_dsc.seek(file_position)
                project_dsc.writelines(line)
                break

            file_position = project_dsc.tell()

    def project_uni_update(self):

        project_uni = open(self.entry_project_uni.get(), 'rb+')

        while True:

            line = project_uni.readline().decode('UTF-16BE', 'ignore')
            if not line:
                break

            string = re.findall('#string\s*(\S*)\s*#language\sen-US\s*"(\S*)"', line)

            if string:

                org_file_position = project_uni.tell()

                if string[0][0] == u'STR_MISC_BIOS_VERSION':
                    now_kernel_tag = re.findall('\S*?\.(.*)\.[0-9]*$', string[0][1])[0]

                    if len(self.entry_chipset_tag.get()) > 1:
                        now_chipset_tag = re.findall('\.([0-9]*)$', string[0][1])[0]
                        line = line.replace(now_chipset_tag, self.entry_chipset_tag.get())

                    line = line.replace(now_kernel_tag, self.history_last_tag)
                    project_uni.seek(file_position)
                    project_uni.writelines(line.encode('UTF-16BE'))
                    project_uni.seek(org_file_position)

                elif string[0][0] == u'STR_CCB_VERSION':
                    line = line.replace(string[0][1], self.history_last_tag)
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
                    east_kernel = self.history_last_tag.split('.')
                    east_chipset = '10' + str(int(self.entry_chipset_tag.get()))
                    east = str(int(east_kernel[0])) + str(int(east_kernel[1]) - 5) + east_kernel[2] + east_chipset
                    line = line.replace(string[0][1], east)
                    project_uni.seek(file_position)
                    project_uni.writelines(line.encode('UTF-16BE'))
                    project_uni.seek(org_file_position)

            file_position = project_uni.tell()

    def confirm(self):
        self.kernel_last_tag = Updater.find_label('Tag#:\s*(.+)', self.entry_kernel.get(), 0)
        self.history_last_tag = Updater.find_label('Tag#:\s*(.+)', self.entry_history.get(), 0)

        Updater.position_ini_updater(self.position_ini, 'history.txt', self.entry_history.get())
        Updater.position_ini_updater(self.position_ini, 'kernel.txt', self.entry_kernel.get())
        Updater.position_ini_updater(self.position_ini, 'project.dsc', self.entry_project_dsc.get())
        Updater.position_ini_updater(self.position_ini, 'project.uni', self.entry_project_uni.get())
        Updater.position_ini_updater(self.position_ini, 'chipset_Tag', self.entry_chipset_tag.get())

        self.kernel_update()
        self.project_dsc_update()
        self.project_uni_update()

        tkMessageBox.showinfo('Info', self.message_box_content)
        self.message_box_content = ''

root = Tkinter.Tk()
app = Update(root)
root.mainloop()
