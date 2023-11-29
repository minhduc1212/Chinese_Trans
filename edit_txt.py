# Description: Edit txt file
with open ('test.txt', 'r', encoding='utf-8' ) as f:
    lines = f.readlines()
with open ('test.txt', 'w', encoding='utf-8') as f:    
    for line in lines:
        if line.strip() != '':
            f.write(line.strip() + '\n')
            line = line.replace(' 。', '.')
            print(line.count('.'))
            
            
            


