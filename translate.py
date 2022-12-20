with open("Script/aqu_01_01.binu8", "rb") as f:
    data = bytearray(f.read())

# うさみみハリケーンで抽出したテキストを読み込む
with open('extract/aqu_01_01.txt', 'r', encoding='utf-16') as f:
    text = f.read()

# 改行で分割してリストにする
lines = text.split('\n')

# \tが区切り文字となっているので、それで分割する
# これで、リストの中にリストが入っている状態になる
lines = [line.split('\t') for line in lines]

replace_list = [
    "--The whole area was on fire.",
    "The two were cornered, and they were already ready to go.",
    "Torres",
    "@v20000「Damn, We're surrounded by fire. There is no escape now.」",
    "Emily",
    "@v10000「I'm sorry……because I wished for a wayward love……」",
    "@v10001「I tried to be your lover, only to be chased out of the mansion and burned down hideout……」",
    "@v10002「And finally, we're trapped on the edge of a cliff！」",
    "@v10003「I wish I had never fallen in love with you if this was going to happen…」"
]

offset = 0
for i, line in enumerate(lines):
    if line[0] == "":
        break
    address = int(line[0], 16) + offset
    string_length = data[address-0x04]
    string = data[address:address+string_length].decode("utf-8")
    print(string_length, string)

    if i < len(replace_list):
        replace_string = replace_list[i]
        replace_string = replace_string.encode("utf-8")
        replace_string_length = len(replace_string)+1
        data[address-0x04] = replace_string_length
        data = data[:address] + replace_string + data[address+string_length-1:]

        offset += replace_string_length - string_length

with open("mod/aqu_01_01.binu8", "wb") as f:
    f.write(data)
