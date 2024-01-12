ch_s = set()
hv_s = set()

with open('Vietphrase_new.txt', 'r', encoding='utf-8') as f:
    for line in f:
        ch, vi = line.strip().split('=')
        if len(ch) == 1:
            ch_s.add(ch)

with open('ch.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(ch_s))

with open('hv.txt', 'r', encoding='utf-8') as f:
    for line in f:
        ch, vi = line.strip().split('=')
        if ch not in ch_s:
            hv_s.add(line)
            print(line)

with open('hv_new.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(hv_s))