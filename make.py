import numpy as np
from scipy.io import wavfile
import operator
import time

rate = 44100

higth = [
    1.0, 
    0.72, 
    0.5, 
    0.35
    ]

just_intonation = [
    1/1, 
    16/15, 
    9/8, 
    6/5, 
    5/4, 
    4/3, 
    45/32, 
    3/2, 
    8/5, 
    5/3, 
    16/9, 
    15/8, 
    2/1, 
    0/1
    ] # 純正律

equal_temperament = [
    1.00000000, 
    1.05946309, 
    1.12246205, 
    1.18920712, 
    1.25992105, 
    1.33483985, 
    1.41421356, 
    1.49830708, 
    1.58740105, 
    1.68179283, 
    1.78179744, 
    1.88774863, 
    2.00000000, 
    0.00000000
    ]

ratio = just_intonation

tone = [
    16.35159783, 
    32.70319566, 
    65.40639133, 
    130.81278265, 
    261.6255653, 
    523.2511306, 
    1046.5022612, 
    2093.0045224, 
    4186.00904481, 
    0.0
    ]
notes = [
    "c", "h", "d", "n", "e", "f", "j", "g", "t", "a", "i", "b", "w", "p", 
    "C", "H", "D", "N", "E", "F", "J", "G", "T", "A", "I", "B", "W", "P"
    ]#cハdニefヘgトaイbロ(cdefgabとハニホヘトイロハを組み合わせたもの(abcがナチュラル，イロハがシャープ・フラット) j, Jはhの隣で代用したため) w, Wは1オクターブ上 p, Pはpass(休符)

overtone = {
    "piano":[0.63, 0.17, 0.1, 0.03, 0.04, 0.0, 0.04, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
    "trumpet":[0.18, 0.31, 0.35, 0.06, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "violin":[0.31, 0.14, 0.0, 0.0, 0.06, 0.06, 0.21, 0.07, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}

def chord(a, b):#[list a, list b]　和音
    if len(a) > len(b):
        b = np.concatenate([b, [0]*abs(len(a)-len(b))])
    elif len(a) < len(b):
        a = np.concatenate([a, [0]*abs(len(a)-len(b))])
    return a + b

def join(a, b):#[list a, list b]　連結
    return np.concatenate([a, b])

def tempo(data):#[str data]　速度
    data = data.split(",")
    return 60 / (int(data[1]) * (4 / int(data[0])))

def piano(sound, scale, length):#[str sound, str:int scale, str:float length]　ピアノ 単ノーツ
    length = (4 / int(length)) * speed
    sound = notes.index(sound) % 14
    frequency = tone[int(scale)] * ratio[sound]
    phases = 2.0 * np.pi * frequency / rate * np.zeros(int(rate * float(length)))
    print(len(phases), type(phases), end="")
    for i in range(24):
        phases_ = np.sin((np.cumsum(2.0 * np.pi * (frequency * (i + 1)) / rate * np.ones(int(rate * float(length))))))
        phases_ = np.array(list(map(lambda phases_: phases_ * float(overtone["piano"][i]), phases_)))
        phases = [x + y for (x, y) in zip(phases, phases_)]
    phases = np.array(phases)
    return phases

def pianos(sound, scale, length):#[list sound, list scale, list length]　ピアノ 複ノーツ
    print("length : " + str(len(sound)))
    s = np.array([])
    for i in range(len(sound)):
        if len(sound[i]) > 1:
            a = ([0])
            for j in range(len(sound[i])):
                #a = chord(a, list(map(lambda x: x * higth[len(sound[i]) - 1], piano(sound[i][j], scale[i][j], length[i][j]))))
                a = chord(a, list(map(lambda x: x / len(sound[i]), piano(sound[i][j], scale[i][j], length[i][j]))))
        else:
            a = piano(sound[i], scale[i], length[i])
        s = np.concatenate([s, a])
        print("  line : " + str(i))
    return s

def play(sound, scale, length, instrument="piano"):#[str sound, str:int scale, str:float length, str instrument="piano"]　単ノーツ
    length = (4 / int(length)) * speed
    sound = notes.index(sound) % 14
    frequency = tone[int(scale)] * ratio[sound]
    phases = 2.0 * np.pi * frequency / rate * np.zeros(int(rate * float(length)))
    print(len(phases), type(phases), end="")
    for i in range(24):
        phases_ = np.sin((np.cumsum(2.0 * np.pi * (frequency * (i + 1)) / rate * np.ones(int(rate * float(length))))))
        phases_ = np.array(list(map(lambda phases_: phases_ * float(overtone[instrument][i]), phases_)))
        phases = [x + y for (x, y) in zip(phases, phases_)]
    phases = np.array(phases)
    return phases

def plays(sound, scale, length, instrument="piano"):#[list sound, list scale, list length, str instrument="piano"]　複ノーツ
    print("length : " + str(len(sound)))
    s = np.array([])
    for i in range(len(sound)):
        if len(sound[i]) > 1:
            a = ([0])
            for j in range(len(sound[i])):
                #a = chord(a, list(map(lambda x: x * higth[len(sound[i]) - 1], play(sound[i][j], scale[i][j], length[i][j], instrument))))
                a = chord(a, list(map(lambda x: x / len(sound[i]), play(sound[i][j], scale[i][j], length[i][j], instrument))))
        else:
            a = piano(sound[i], scale[i], length[i])
        s = np.concatenate([s, a])
        print("  line : " + str(i))
    return s
start = time.time()
chart = ";"#楽譜
chart = chart.split(";")#楽譜の分割
code = chart[1]#音符
speed = tempo(chart[0])#テンポ
data = [[], [], []]
j, last = 0, 0
for i in range(int(len(code) / 3)):
    if code[(i + 1) * 3 - 3 + j] == "[":
        j += 1
        data[0].append([])
        data[1].append([])
        data[2].append([])
        while True:
            if code[(i + 1) * 3 - 3 + j] == "]":
                j -= 2
                break
            else: # tryでexitすべき
                #print((i + 1) * 3 - 1 + j)
                data[0][len(data[0]) - 1].append(code[(i + 1) * 3 - 3 + j])
                data[1][len(data[1]) - 1].append(code[(i + 1) * 3 - 2 + j])
                data[2][len(data[2]) - 1].append(int(code[(i + 1) * 3 - 1 + j], 33))
                j += 3
    else:
        data[0].append(code[(i + 1) * 3 - 3 + j])         #音
        data[1].append(code[(i + 1) * 3 - 2 + j])         #音階
        data[2].append(int(code[(i + 1) * 3 - 1 + j], 33))#長さ(n分音符)
    if (i + 1) * 3 + j >= len(code):
        break

#wave = (piano("c", "4", "2.0") * float(2 ** 15 - 1)).astype(np.int16)
#wavfile.write("c4.wav", rate, wave)

#list(map(lambda x: (4 / x) * speed, data[2]))

wave = (pianos(data[0], data[1], data[2]))#楽譜を音にする
wave = (wave * float(2 ** 15 - 1)).astype(np.int16)#量子化する
wavfile.write(".wav", rate, wave)#wav形式で出力
print(str(time.time() - start) + "s")

#print(data[0])
#print(data[1])
#print(data[2])
