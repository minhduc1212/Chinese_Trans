str = 'abc, abc, 时.'
my_dict = ['a', 'b', 'c']

positions = []
for index, character in enumerate(str):
    if character not in my_dict:
        positions.append(index)

print(positions)