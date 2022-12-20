import re
import os
import librosa as lr
import soundfile as sf
import sys

for c in ["aqua", "fubuki", "marine"]:
    # キャラクターのフォルダがなければ作成する
    if not os.path.exists('voice/' + c):
        os.mkdir('voice/' + c)
    # voice_text.txtを削除する
    with open(f'voice/{c}/voice_text.txt', 'w') as f:
        f.write('')

# うさみみハリケーンで抽出したテキストを読み込む
with open('extract/all.txt', 'r', encoding='utf-16') as f:
    text = f.read()

# 改行で分割してリストにする
lines = text.split('\n')

# \tが区切り文字となっているので、それで分割する
# これで、リストの中にリストが入っている状態になる
lines = [line.split('\t') for line in lines]
size = len(lines)


def preprocess_text(text):
    # いくつかのスペース（例えば全角スペース、半角スペース、タブ）をまとめて削除
    text = re.sub(r"[\u3000 \t]", "", text)

    # 「を削除
    text = text.replace('「', '')
    text = text.replace('」', '')

    # @から始まり、半角英数字が続く部分を削除
    text = re.sub(r"@[a-zA-Z0-9!-/:-@¥[-`{-~]+", "", text)

    # 改行を削除
    text = text.replace('\\n', '')
    # 改行を削除
    text = text.replace("\n", "")
    # 改行を削除
    text = text.replace("\r", "")
    # 鍵かっこを削除
    text = text.replace("『", "")
    text = text.replace("』", "")
    # …を削除
    text = text.replace("…", "")
    # （を削除
    text = text.replace("（", "")
    # ）を削除
    text = text.replace("）", "")
    # ―をーに置換
    text = text.replace("―", "ー")
    # ーーを削除
    text = text.replace("ーー", "")
    # ——
    text = text.replace("——", "")
    # ～をーに置換
    text = text.replace("～", "ー")
    return text


for index, line in enumerate(lines):
    # 改行のみの行は無視する
    if len(line) == 1:
        continue
    # 0番目の要素は、オフセット
    # 1番目の要素は、テキスト
    # テキストが@vから始まっている場合は、ボイス付きのテキスト
    # ボイス付きのテキストの場合
    if line[1].startswith('@v'):
        # ボイス付きのテキストの場合、@vの後にボイスファイル名が続く(半角英数字)
        # そのボイスファイル名を取得する
        voice_file = re.search(r'@v([a-zA-Z0-9]+)', line[1]).group(1)
        # テキストはボイスファイル名を削除したもの
        text = re.sub(r'@v[a-zA-Z0-9]+', '', line[1])
        # テキストを前処理する
        text = preprocess_text(text)

        print(voice_file, text)

        # ボイスのファイル名から@vを削除
        voice_file = voice_file.replace('@v', '')

        # キャラクター別にファイルを保存する
        character_name = ""
        # 0から始まる場合は、Aquaのボイス
        if voice_file.startswith('0'):
            character_name = 'aqua'
        # 1から始まる場合は、Fubukiのボイス
        elif voice_file.startswith('1'):
            character_name = 'fubuki'
        # 2から始まる場合は、Marineのボイス
        elif voice_file.startswith('2'):
            character_name = 'marine'
        # それ以外の場合は、無視する
        else:
            continue
        with open(f'voice/{character_name}/voice_text.txt', 'a', encoding='utf-8') as f:
            f.write(voice_file + ':' + text + '\n')

        # ボイスファイルをそれぞれのキャラクターのフォルダに.opusから.wavに変換する
        # 例：voice/aqua/voice/00000.wav
        # 例：voice/fubuki/voice/10000.wav
        # 例：voice/marine/voice/20000.wav

        print(f"変換完了 {index}/{size}")

        # voiceフォルダがなければ作成する
        if not os.path.exists(f'voice/{character_name}/voice'):
            os.makedirs(f'voice/{character_name}/voice')
        # VoiceRename1～VoiceRename6フォルダのどこかにある.opusファイルを変換する
        print(voice_file)
        for i in range(1, 7):
            # VoiceRename1～VoiceRename6フォルダのどこかにある.opusファイルを変換する
            if os.path.exists(f'voice/VoiceRename{i}/{voice_file}.opus'):
                y, sr = lr.load(
                    f'voice/VoiceRename{i}/{voice_file}.opus', sr=48000)
                sf.write(
                    f'voice/{character_name}/voice/{voice_file}.wav', y, samplerate=48000, subtype="PCM_24")
                print(f"変換完了 {index}/{size}")
                break
