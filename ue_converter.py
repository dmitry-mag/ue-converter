import tkinter as tk
import csv
from collections import OrderedDict

# read types and values from file "types.csv"
with open('types.csv', 'r') as file_types:
    reader = csv.reader(file_types, delimiter=';')
    header = next(reader)
    # dict for types of devices usage
    dict_usage = OrderedDict()
    for index, item in enumerate(header[1:]):
        dict_usage[item] = index
    # dict for types of devices
    dict_types = OrderedDict()
    for line in reader:
        dict_types[line[0]] = list(map(lambda x: float(x.replace(',','.')), \
                                                            line[1:]))

# global result variables
result_ue = 0
task_ue = 0
result_ots = 0
result_vts = 0
task_ots = 0
task_vts = 0
task_list = []
result_list = []
result_tasks_list = []
current_task = -1
current_line = 0
current_id = 0
index_list = []

# first line in output file
first_out_line = ['№ Заявки', 'Заказчик', 'Проверяемые ТС', 'Количество', \
                                    'Кол. ОТСС', 'Кол. ВТСС', 'у.е.']

# empty line for delimiter
empty_out_line = ['' for _ in range(7)]


def click_new(*args):
    """action on press new button"""
    global result_list
    global task_list
    global index_list
    global current_task
    global task_ots
    global task_vts
    global task_ue

    # check user input
    if text_output.compare('end-1c', '!=', '1.0') and len(task_list) == 0:
        var_message.set('Нет ТС по последней\n введенной заявке!')
        return None 
    elif not entry_task.get():
        var_message.set('Введите № заявки!')
        return None
    elif not entry_customer.get():
        var_message.set('Введите заказчика!')
        return None

    # save task if task list is not empty
    if len(task_list) > 0:
        task_list.sort(key=lambda x: x[5])
        result_list += task_list
        
    # make new row in tasks result with task and customer
    result_tasks_list.append([entry_task.get(), entry_customer.get(), '', 0, \
                                                        0, 0, 0])
    # increase task counter
    current_task += 1

    # clear device list and add new task to past inputs text
    task_list = []
    text_output.configure(state=tk.NORMAL)
    if text_output.compare('end-1c', '!=', '1.0'):
        text_output.insert(tk.END, '\n')
        # add empty pointer to index list
        index_list.append(None)
    text_output.insert(tk.END, 'Заявка № ' + entry_task.get() + '\n')
    text_output.see(tk.END)
    text_output.configure(state=tk.DISABLED)
    # add empty pointer to index list
    index_list.append(None)
    # set task counts to zero
    task_ots = 0
    task_vts = 0
    task_ue = 0
    # clear task input field
    entry_task.delete(0,tk.END)


def click_next(*args):
    """action on press next button"""
    global result_list
    global task_list
    global task_ue
    global task_ots
    global task_vts
    global current_task
    global current_id

    # check user input
    if text_output.compare('end-1c', '==', '1.0'):
        var_message.set('Добавьте заявку!')
        return None 
    elif not entry_name.get():
        var_message.set('Введите наименование!\nИли двойной клик в списке.')
        return None
    elif not entry_type.get(tk.ANCHOR):
        var_message.set('Выберите тип ТС!')
        return None
    elif not var_usage.get():
        var_message.set('Выберите условие\n эксплуатации!')
        return None
    try:
        if int(entry_count.get()) < 1:
            raise ValueError
    except ValueError:
        var_message.set('Количество ТС должно\n быть целым положительным!')
        return None
    next_ue = int(entry_count.get()) * \
        dict_types[entry_type.get(tk.ANCHOR)][dict_usage[var_usage.get()]]
    if next_ue == 0:
        var_message.set('Выбранный тип ТС\n не эксплуатируется\n в качестве ОТС!')
        return None

    # calculation and print user input
    if 'ОТС' in var_usage.get():
        num_ots, num_vts = entry_count.get(), ''
    else:
        num_ots, num_vts = '', entry_count.get()
    task_list.append(['', '', entry_name.get(), '', num_ots, num_vts, next_ue, \
                                    current_task, current_id])
    

    result_str = '{} {}\n'.format(entry_count.get(), entry_name.get())
    var_result.set(next_ue)
    var_message.set('')
    text_output.configure(state=tk.NORMAL)
    text_output.insert(tk.END, result_str)
    text_output.see(tk.END)
    text_output.configure(state=tk.DISABLED)
    # add pointer to index list
    index_list.append(current_id)

    # increment id counter
    current_id += 1
    # set out focus, when call from pressing enter on Entry
    if args:
        entry_usage.focus()


def click_end():
    """action on press end button"""
    global result_list
    global task_list
    
    # check user input
    if text_output.compare('end-1c', '==', '1.0'):
        var_message.set('Добавьте заяку и ТС!')
        return None 
    if len(task_list) == 0:
        var_message.set('Нет ТС по последней\n введенной заявке!')
        return None

    # save past input task
    task_list.sort(key=lambda x: x[5])
    result_list += task_list

    # calculate results for every task
    for item in result_list:
        if item[4]:
            result_tasks_list[item[7]][4] += int(item[4])
            result_tasks_list[item[7]][3] += int(item[4])
        if item[5]:
            result_tasks_list[item[7]][5] += int(item[5])
            result_tasks_list[item[7]][3] += int(item[5])
        result_tasks_list[item[7]][6] += item[6]
    

    # calculate last result line
    last_res_line = ['', '', 'итого:', 0, 0, 0, 0]
    for task in result_tasks_list:
        last_res_line[3] += task[3]
        last_res_line[4] += task[4]
        last_res_line[5] += task[5]
        last_res_line[6] += task[6]
    last_res_line[6] = str(last_res_line[6]).replace('.', ',')

    # write output file
    with open('result.csv', 'w', newline='') as file_out:
        writer = csv.writer(file_out, delimiter=';', dialect='excel')
        # write first line with titles
        writer.writerow(first_out_line)
        # write tasks and devices to file
        for num, task in enumerate(result_tasks_list):
            writer.writerow([task[0], task[1], '', '', '', '', ''])
            for device in [x for x in result_list if x[7] == num]:
                writer.writerow(device[:-3] + [str(device[-3]).replace('.', ',')])
            # write task results
            writer.writerow(['', '', 'всего:', task[3], task[4], \
                            task[5], str(task[6]).replace('.', ',')])

        # write last line in out file with delimiter line
        writer.writerow(empty_out_line)
        writer.writerow(last_res_line)
    window.destroy()


def click_del():
    """action on press delete button"""
    global current_line
    global result_list
    global task_list
    global num_of_deleted

    # check for valid line selection
    if current_line and int(current_line) <= len(index_list):
        selected_id = index_list[int(current_line) - 1]
    else:
        selected_id = None
    # check line for device and removing
    if selected_id != None:
        index_list[int(current_line) - 1] = None
        new_list = []
        if selected_id in [x[8] for x in result_list]:
            for item in result_list:
                if item[8] != selected_id:
                    new_list.append(item)
            result_list = new_list
        elif selected_id in [x[8] for x in task_list]:
            for item in task_list:
                if item[8] != selected_id:
                    new_list.append(item)
            task_list = new_list
        text_output.configure(state=tk.NORMAL)
        text_output.delete(current_line + '.0', current_line + '.end')
        text_output.insert(current_line + '.0', 'удалено')
        text_output.configure(state=tk.DISABLED)
    else:
        var_message.set('Выберите строку с ТС!')


def double_click_list(event):
    """Adding type name from list to device name entry"""
    entry_name.delete(0, tk.END)
    entry_name.insert(0, entry_type.get(entry_type.curselection())) # tk.ANCHOR))
    entry_count.select_range(0, tk.END)
    entry_count.focus()


def focus_to(event, obj):
    """change focus to recived object"""
    obj.select_range(0, tk.END)
    obj.focus()


def click_text(event):
    """set line pointer on click"""
    global current_line

    try:
        current_line = text_output.index(tk.INSERT).split('.')[0]
        text_output.tag_remove('line', '1.0', 'end')
        text_output.tag_add('line', current_line + '.0', current_line + '.end')
        text_output.tag_config('line', background='Gray')
    except:
        current_line = None

if __name__ == '__main__':
    # geometry parameters of elements
    WIDTH_L = 30
    WIDTH_M = 52
    WIDTH_R = 25
    WIDTH_B = 15
    
    # main window parameters
    window = tk.Tk()
    window.resizable(False, False)
    window.title('Расчет у.е. ТС')

    # tkinter variables
    var_result = tk.StringVar(window)
    var_message = tk.StringVar(window)
    var_usage = tk.StringVar(window)
    var_usage.set(list(dict_usage.keys())[0])

    # frames parameters:
    frame_output = tk.Frame(window, width=WIDTH_L)
    frame_output.grid(row=5, column=0, rowspan=5)

    frame_types = tk.Frame(window, width=WIDTH_M)
    frame_types.grid(row=1, column=1, rowspan=10)

    frame_result = tk.Frame(window, width=WIDTH_R)
    frame_result.grid(row=10, column=2)

    # labels parameters
    label_task = tk.Label(window, text='№ заявки:', font=('Verdana', 12))
    label_task.grid(row=0, column=0, sticky='W')
    label_customer = tk.Label(window, text='Заказчик:', font=('Verdana', 12))
    label_customer.grid(row=2, column=0, sticky='W')
    label_output = tk.Label(window, text='Список введенных ТС:', \
                                                    font=('Verdana', 12))
    label_output.grid(row=4, column=0, sticky='W')
    label_type = tk.Label(window, text='Тип ТС:', font=('Verdana', 12))
    label_type.grid(row=0, column=1, sticky='W')
    label_usage = tk.Label(window, text='Условия эксплуатации:', \
                                        font=('Verdana', 12))
    label_usage.grid(row=0, column=2, sticky='W')
    label_count = tk.Label(window, text='Количество ТС:', font=('Verdana', 12))
    label_count.grid(row=2, column=2, sticky='W')
    label_name = tk.Label(window, text='Наименование ТС:', font=('Verdana', 12))
    label_name.grid(row=4, column=2, sticky='W')
    label_message = tk.Label(window, textvariable=var_message, height=3,\
                                                    font=('Verdana', 12))
    label_message.grid(row=8, column=2)
    label_result = tk.Label(frame_result, text='последний ввод у.е.:', \
                                                    font=('Verdana', 12))
    label_result.pack(side=tk.LEFT)
    label_result = tk.Label(frame_result, textvariable=var_result, \
                                                    font=('Verdana', 12))
    label_result.pack(side=tk.RIGHT, fill=tk.BOTH)

    # user inputs
    entry_task = tk.Entry(window, font=('Verdana', 12), width=WIDTH_L)
    entry_task.grid(row=1, column=0)
    entry_customer = tk.Entry(window, font=('Verdana', 12), width=WIDTH_L)
    entry_customer.grid(row=3, column=0)
    entry_count = tk.Entry(window, font=('Verdana', 12), width=WIDTH_R)
    entry_count.grid(row=3, column=2)
    entry_name = tk.Entry(window, font=('Verdana', 12), width=WIDTH_R)
    entry_name.grid(row=5, column=2)
    # add 'enter' functionality to entry
    entry_task.bind('<Return>', lambda event, arg=entry_customer: \
                                                        focus_to(event, arg))
    entry_count.bind('<Return>', lambda event, arg=entry_name: \
                                                        focus_to(event, arg))
    entry_customer.bind('<Return>', click_new)
    entry_name.bind('<Return>', click_next)

    # menu for usage types
    entry_usage = tk.OptionMenu(window, var_usage, *list(dict_usage.keys()))
    entry_usage.grid(row=1, column=2)
    entry_usage.config(font=('Verdana', 12), bg='white', width=WIDTH_R - 4)
    entry_usage['menu'].config(font=('Verdana', 12), bg='white')
    # listbox for types
    scroll_types = tk.Scrollbar(frame_types)
    scroll_types.pack(side=tk.RIGHT, fill=tk.Y)
    entry_type = tk.Listbox(frame_types, selectmode=tk.BROWSE, width=WIDTH_M, \
            height=23, font=('Verdana', 12), yscrollcommand=scroll_types.set, \
            selectbackground='Grey', exportselection=False)
    for item in list(dict_types.keys()):
        entry_type.insert(tk.END, item)
    entry_type.pack(side=tk.LEFT, fill=tk.BOTH)
    scroll_types.config(command=entry_type.yview)
    # double-click adding to device name
    entry_type.bind('<Double-Button-1>', double_click_list)
    # "enter" action for list of types
    entry_type.bind('<Return>', double_click_list)

    # show past inputs
    scroll_output = tk.Scrollbar(frame_output)
    scroll_output.pack(side=tk.RIGHT, fill=tk.Y)
    text_output = tk.Text(frame_output, width=WIDTH_L - 2, font=('Verdana', 12), \
               height=16, yscrollcommand=scroll_output.set, state=tk.DISABLED)
    text_output.pack(side=tk.LEFT, fill=tk.BOTH)
    scroll_output.config(command=text_output.yview)
    # bind mouse button for choice line
    text_output.bindtags(('Text', 'post-class-bindings', '.', 'all'))
    text_output.bind_class('post-class-bindings', '<Button-1>', click_text)

    # buttons
    button_new = tk.Button(window, text='Ввод № заявки', command=click_new, \
                            font=('Verdana', 12), width=WIDTH_B)
    button_new.grid(row=6, column=2)
    button_next = tk.Button(window, text='Ввод ТС', command=click_next, \
                            font=('Verdana', 12), width=WIDTH_B)
    button_next.grid(row=7, column=2)
    button_end = tk.Button(window, text='Сохранить расчет', command=click_end, \
                            font=('Verdana', 12), width=WIDTH_B)
    button_end.grid(row=9, column=2)
    button_del = tk.Button(window, text='Удалить ТС', command=click_del, \
                            font=('Verdana', 12), width=WIDTH_B)
    button_del.grid(row=10, column=0)

    # start programm
    window.mainloop()
