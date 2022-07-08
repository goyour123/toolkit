import PyUpdate
import os

position = 'position.ini'

kernel_address = PyUpdate.find_position(position, 'Kernel.txt')
history_address = PyUpdate.find_position(position, 'History.txt')

kernel_last_tag = PyUpdate.find_label('Tag#:\s*(.+)', kernel_address, 0)
history_last_tag = PyUpdate.find_label('Tag#:\s*(.+)', history_address, 0)

if not PyUpdate.cmp_tag(kernel_last_tag, history_last_tag):
    history_sequence = PyUpdate.get_hist_seq(history_address)
    kernel_sequence = PyUpdate.get_ker_seq(kernel_address)

    kernel = open(kernel_address, 'w+')
    kernel.writelines(history_sequence)
    kernel = open(kernel_address, 'a')
    kernel.writelines(kernel_sequence)
    print 'Update Kernel.txt succeeded'
else:
    print 'Kernel.txt or History.txt isn\'t right'

os.system('pause')
