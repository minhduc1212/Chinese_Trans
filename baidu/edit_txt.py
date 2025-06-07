# Description: Edit txt file
with open ('result.txt', 'r', encoding='utf-8' ) as f:
    lines = f.readlines()
with open ('result.txt', 'w', encoding='utf-8') as f:    
    for line in lines:
        if line.strip() != '':
            f.write(line.strip() + '\n' + '\n')
            line = line.replace(' 。', '.')
            
            
            
            


