print('Перед запуском рекомендуется прочесть инструкцию\nрепликатор будет невозможно остановить\nпока он не обработает весь damp\n\nby Фисаков А.С. и Пантюхин В.А. отдел АСУТП \n\n')

from pynput import keyboard, mouse  # Библиотеки для управление клавиатуры и мышки
from pynput.mouse import Button     # Подтягивание контроллеров клавиатуры и мышки
import time                         # Подтягивание библиотеки для переменных управления временем
from threading import Thread        # Подтягивание библиотеки управления мультипоточностью
import PySimpleGUI as sg            # Подтягивание библиотеки интерфейса
from pyautogui import keyUp, keyDown, mouseDown, mouseUp


keyb = keyboard.Controller()    # Присвоение контроллера клавиатуры
mouse = mouse.Controller()      # Присвоение контроллера мыши
ctrl_l = keyboard.Key.ctrl_l    # Присвоение клавиши LCtrl в более удобную переменную
sg.theme('Default')             #Обьясление цветовой схемы интерфейса
layout = [          #Интерфейс
    [sg.Text('Перед началом работы рекомендуется прочесть инструкцию!')],   #Сообщение
    [sg.Text('Для немедленной остановки репликатора нажмите RShift')],      #Сообщение2
    [sg.Text('Строчка для замены тега'), sg.Input(default_text='Введите заменяемый тег', key='TAG')],   #Строчка для замены тега
    [sg.Text('Строчка для замены комментария'), sg.Input(default_text='Введите заменяемый комментарий', key='TAGС')], #Строчка для замены комментария
    [sg.Checkbox('Реплицировать в один столбец', key='simple', default=False), sg.Checkbox('Реплицировать в два столбца', key='double', default=True)], #Ввод выбора режима реплицирования
    [sg.Text('Status: ready', key='out')], #Вывод статуса программы
    [sg.Button('!!GO!!')]   #Кнопка
]

# Словарь с кординатами
cords = {"main": (712, 166),            # Главное подпрограмм
         "buf": (829, 166),             # Буферная подпрограмма
         "rep_up": (1106, 637),         # Верхняя строка в откне замены
         "sel_all_up": (1168, 768),     # "Выбрать все" в верхней строке
         "rep_down": (1098, 665),       # Низняя строка в откне замены
         "sel_all_down": (1164, 802),   # "Выбрать все" в внижней строке
         "rep_all": (1231, 690),        # "Заменить все" в откне замены
         "close": (1279, 602),          # Закрыть окно замены
         "past": (898, 215),            # Окно вставки
         "past_here": (986, 348)}       # "Вставить сюда" в окне вставки


def cler_poles():
    mouse.position = cords["rep_up"]
    mouse.click(Button.left)
    mouse.click(Button.right)
    mouse.position = cords["sel_all_up"]
    mouse.click(Button.left)
    keyDown("backspace")
    keyUp("backspace")
    time.sleep(0.2)

    mouse.position = cords["rep_down"]
    mouse.click(Button.left)
    mouse.click(Button.right)
    mouse.position = cords["sel_all_down"]
    mouse.click(Button.left)
    keyDown("backspace")
    keyUp("backspace")
    time.sleep(0.2)


with open("C:/Replicator/damp.txt", "r") as file:  # Перенос тегов без окончания в новый файл
    f = open("C:/Replicator/damp_correct.txt", "w")
    f.close()
    for line in file.readlines():
        line = line[:line.find("|")+1] + line[-1]
        with open("C:/Replicator/damp_correct.txt", "a") as f:
            f.write(line)


#Обьявление окна интерфейса
window = sg.Window('Replicator', layout)


def Replicator(key):        #Главный алгоритм репликатора
    past = values['TAG']                #Присвоение значения введенного для замены тега
    way = ("C:/Replicator/damp_correct.txt")    #Путь к файлу с тегами
    file = open(way, "r", encoding="UTF-8")               #Открытие все того же файла для чтения
    
    pastc = values['TAGС']              #Присвоение значения введенного для замены комментария
    way2 = ("C:/Replicator/damp2.txt")    # Путь к файлу
    filec = open(way2, "r",  encoding="UTF-8")            # Открытие файла
    j = 0

    while True:                     # Цикл строчек
        if j == 0:
            linePast = past  # Перекладка строчки из dump в переменную line
            linePastC = pastc  # Перекладка строчки из dump в переменную line
        else:
            linePast = lineFuture  # Перекладка строчки из dump в переменную line
            linePastC = lineFutureC  # Перекладка строчки из dump в переменную line
            print()
        lineFuture = file.readline() # Перекладка строчки из dump в переменную line
        lineFutureC = filec.readline() # Перекладка строчки из dump в переменную line
        if not lineFuture:
            print('Обработанны все строки в файле damp, рапликатор остановлен')
            window['out'].update(f'Status: Обработанны все строчки, репликатор остановлен')
        if not lineFuture or not thread2.is_alive(): # Остановка цикла, если строчка окажется пустой
            break
        j = j + 1

        mouse.position = cords["buf"] # Выбор буфферного окна
        mouse.click(Button.left)    # Клик

        time.sleep(0.2)
        keyb.press(keyboard.Key.ctrl_l)   # ОБЯЗАТЕЛЬНО ОТОЖМИ БЛЯТЬ
        time.sleep(0.1)      #
        keyb.press('р')      #
        time.sleep(0.1)      # Ctrl+H
        keyb.release(keyboard.Key.ctrl_l) #
        time.sleep(0.1)      #
        keyb.release('р')    #

        cler_poles()    # Ну тупо очищаем все поля чтоб было с кайфом


        ###########################!!!!!!!!!!!ЗАМЕНА!!!!!!!!!!!!!!!!!!!########################
        mouse.position = cords["rep_up"] # Верхняя строка в окне замены
        mouse.click(Button.left,2)   # Правый клик 
        time.sleep(0.1)
 
            ######## ЗАПИСЬ СЛОВА ИЗ СТРОЧКИ ФАЙЛА ##########
        long = len(linePast)        # Определение длинны строчки
        i = 0                   # Внутренний цикловый счетчик
        while i < long:         # Цикл символов
            if linePast[i] == (' '):
                keyflow = '_'
            else:
                keyflow = linePast[i]       # Присваивание символа переменной key
            keyb.press(keyflow)     # Нажимаем key
            keyb.release(keyflow)   # Отпускаем key
            i = i + 1           # Счетчик cPantyukhin
            if keyflow == ('\n'):    # Проверка символа на равенство "ПРБЕЛУ"
                break           # Останавливаем запись слова, если текущий смвол"ПРОБЕЛ"
       
        mouse.position = cords["rep_down"] # Нижнеяя строка в окне замены
        mouse.click(Button.left, 2)  # Двойной клик
        time.sleep(0.1) 


                    ######## ЗАПИСЬ СЛОВА ИЗ СТРОЧКИ ФАЙЛА ##########
        long = len(lineFuture)        # Определение длинны строчки
        i = 0                   # Внутренний цикловый счетчик
        while i < long:         # Цикл символов
            if lineFuture[i] == (' '):
                keyflow = "_"
            else:
                keyflow = lineFuture[i]       # Присваивание символа переменной key
                keyb.press(keyflow)     # Нажимаем key
                keyb.release(keyflow)   # Отпускаем key
            i = i + 1           # Счетчик cPantyukhin
            if keyflow == ('\n'):    # Проверка символа на равенство "ПРБЕЛУ"
                break           # Останавливаем запись слова, если текущий смвол"ПРОБЕЛ"
        
        time.sleep(0.1)
        mouse.position = cords["rep_all"] # Кнопка "заменить все" в окне замены
        mouse.click(Button.left)    # Клик
  
        mouse.position = cords["rep_up"] # Верхняя строка в окне замены
        mouse.click(Button.left, 2)   # Правый клик 
        time.sleep(0.1)


            ######## ЗАПИСЬ СЛОВА ИЗ СТРОЧКИ ФАЙЛА ##########
        long = len(linePastC)        # Определение длинны строчки
        i = 0                   # Внутренний цикловый счетчик
        while i < long:         # Цикл символов
            if linePastC[i] == (' '):
                keyDown("space")
                keyUp("space")
            else:
                keyflow = linePastC[i]       # Присваивание символа переменной key
                keyb.press(keyflow)     # Нажимаем key
                keyb.release(keyflow)   # Отпускаем key
            i = i + 1           # Счетчик cPantyukhin
            if keyflow == ('\n'):    # Проверка символа на равенство "Энетер"
                break           # Останавливаем запись слова, если текущий смвол"Энтер"
       
        mouse.position = cords["rep_down"] # Нижнеяя строка в окне замены
        mouse.click(Button.left, 2)  # Двойной клик
        time.sleep(0.1) 
        
                    ######## ЗАПИСЬ СЛОВА ИЗ СТРОЧКИ ФАЙЛА ##########
        long = len(lineFutureC)        # Определение длинны строчки
        i = 0                   # Внутренний цикловый счетчик
        while i < long:         # Цикл символов
            if lineFutureC[i] == (' '):
                keyDown("space")
                keyUp("space")
            else:
                keyflow = lineFutureC[i]       # Присваивание символа переменной key
                keyb.press(keyflow)     # Нажимаем key
                keyb.release(keyflow)   # Отпускаем key
            i = i + 1           # Счетчик cPantyukhin
            if keyflow == ('\n'):    # Проверка символа на равенство "ПРБЕЛУ"
                break           # Останавливаем запись слова, если текущий смвол"ПРОБЕЛ"
        
        time.sleep(0.1)
        mouse.position = cords["rep_all"] # Кнопка "заменить все" в окне замены
        mouse.click(Button.left)    # Клик

        time.sleep(0.1)
        mouse.position = cords["close"] # Кнопка "закрыть" в окне замены
        mouse.click(Button.left)    # Клик

        time.sleep(0.2)
        keyb.press(keyboard.Key.ctrl_l)   # ОБЯЗАТЕЛЬНО ОТОЖМИ БЛЯТЬ
        time.sleep(0.1)      #
        keyb.press('ф')      #
        time.sleep(0.1)      # Ctrl+A
        keyb.release(keyboard.Key.ctrl_l) #
        time.sleep(0.1)      #
        keyb.release('ф')    #

        keyb.press(keyboard.Key.ctrl_l)   # ОБЯЗАТЕЛЬНО ОТОЖМИ БЛЯТЬ
        time.sleep(0.1)      #
        keyb.press('с')      #
        time.sleep(0.1)      # Ctrl+C
        keyb.release(keyboard.Key.ctrl_l) #
        time.sleep(0.1)      #
        keyb.release('с')    #

        mouse.position = cords["main"] # Переключение в основную подпрограмму
        mouse.click(Button.left)    # Клик
        if values['double']:
            if j % 2 == 1:
                keyb.press(keyboard.Key.ctrl_l)   # ОБЯЗАТЕЛЬНО ОТОЖМИ БЛЯТЬ
                time.sleep(0.1)      #
                keyb.press('м')      #
                time.sleep(0.1)      # Ctrl+V
                keyb.release(keyboard.Key.ctrl_l) #
                time.sleep(0.1)      #
                keyb.release('м')    #  
            else:
                mouse.position = cords["past"]
                mouse.click(Button.right)    # Клик
                time.sleep(0.2)
                mouse.position = cords["past_here"]
                mouse.click(Button.left)    # Клик
                time.sleep(0.2)
                mouseDown()
                mouse.position = mouse.position[0], mouse.position[1]-24 #Ровняем блок если он во второй колонке
                time.sleep(0.1)
                mouseUp()
        if values['simple']:
            keyb.press(keyboard.Key.ctrl_l)   # ОБЯЗАТЕЛЬНО ОТОЖМИ БЛЯТЬ
            time.sleep(0.1)      #
            keyb.press('м')      #
            time.sleep(0.1)      # Ctrl+V
            keyb.release(keyboard.Key.ctrl_l) #
            time.sleep(0.1)      #
            keyb.release('м')    #

    file.close()    # Закрытие файла
    filec.close()    # Закрытие файла

def Listener():
    def stop(key):
        if key == keyboard.Key.shift_r:
            print('Нажат RShift репликатор остановлен')
            window['out'].update(f'Status: был нажат RShift, репликатор остановлен')
            return False
            thread2.join()
    with keyboard.Listener(on_press=stop) as listener:     # Инициализация чтения клавиатуры
        listener.join()

thread1 = Thread(target=Replicator, args=('Y'))
thread2 = Thread(target=Listener, args=())

while True:
    event, values = window.read()
    if values['simple'] == True:
        values['double'] = False
    if values['double'] == True:
        values['simple'] = False
    if event is None or event == sg.WIN_CLOSED:
        break
    if event == '!!GO!!':
        thread1.start()
        thread2.start()
        window['out'].update(f'Status: Репликатор запущен')
        window['!!GO!!'].update(f'CLOSE')