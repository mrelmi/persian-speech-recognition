from pydub import AudioSegment
import csv
from tqdm import tqdm


def audio_spliter(address='audio.wav', t0=0, t1=0, folder=''):
    newAudio = AudioSegment.from_mp3(address)
    newAudio = newAudio[t0:t1]
    newAudio.export(folder + '/' + str(t0) + '-' + str(t1) + '.wav', format="wav")


def milisecond(time):
    time = time.split(":")
    hours = int(time[0])
    minute = int(time[1])
    sec = time[2].split(",")
    second = int(sec[0])
    milisec = int(sec[1])

    time = hours * 3.6e6 + minute * 6e4 + second * 1e3 + milisec
    return int(time)


def times_and_texts(address='text.srt', delay=0):
    file = open(address, "r", encoding='UTF8', errors='ignore')
    lines = file.readlines()
    file.close()
    times = []
    texts = []

    for i in range(len(lines) - 4):
        if '-->' in lines[i]:
            line = lines[i]
            t1, t2 = line.split(" --> ")
            t1 = milisecond(t1) + delay
            t2 = milisecond(t2) + delay
            times.append((t1, t2))
            texts.append(lines[i + 1:i + 3])
    return times, texts


def split_and_write_files(audio_file='audio.wav', subtitle_file='text.srt', write_on_csv=True, folder='/dataset',
                          delay=0):
    times, texts = times_and_texts(subtitle_file, delay)
    if write_on_csv:
        header = ['file', 'time', 'text']
        with open(folder + '/' + 'dataset.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for i, (t0, t1) in tqdm(enumerate(times)):
                audio_spliter(address=audio_file, t0=t0, t1=t1, folder=folder)
                writer.writerow([audio_file, str(t0) + '-' + str(t1), texts[i][0] + texts[i][1]])


    else:
        for i, (t0, t1) in tqdm(enumerate(times)):
            audio_spliter(address=audio_file, t0=t0, t1=t1)
            with open(folder + '/' + str(t0) + '-' + str(t1) + '.txt', 'w') as f:
                f.write(texts[i][0] + texts[i][1])


split_and_write_files(audio_file='audio.wav', subtitle_file='text.srt', write_on_csv=True, folder='dataset',
                      delay=24000)
