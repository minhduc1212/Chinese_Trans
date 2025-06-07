#lặp qua các phần tử nếu thấy phần tử tiếp theo lớn hơn 1 thì đưa vào list nếu ko thì tạo list mới
def find_consecutive_sequences(lst):
    sequences = []
    current_sequence = [lst[0]]

    for i in range(1, len(lst)):
        if lst[i] == lst[i-1] + 1:
            current_sequence.append(lst[i])
        else:
            sequences.append(current_sequence)
            current_sequence = [lst[i]]
    
    sequences.append(current_sequence)
    return sequences

numbers = [1, 3, 4, 5, 6, 12, 13, 19]   
consecutive_sequences = find_consecutive_sequences(numbers)
print("Consecutive sequences:", consecutive_sequences)
for sequence in consecutive_sequences:
    if len(sequence) > 1:
        start = sequence[0]
        end = sequence[-1] + 1
        print(start, end)