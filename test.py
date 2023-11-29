def load_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        dictionary = {}
        for line in lines:
            key, value = line.strip().split('=')
            dictionary[key] = value
        return dictionary
    
def replace_words_in_paragraph(paragraph, dictionary):
    words = paragraph.split()
    replaced_words = []
    for word in words:
        if word in dictionary:
            replaced_words.append(dictionary[word])
        else:
            replaced_words.append(word)
    return ' '.join(replaced_words)

dictionary_file_path = 'dictionary.txt'
paragraph = 'This is a sample paragraph to test the word replacement tool.'
dictionary = load_dictionary(dictionary_file_path)
replaced_paragraph = replace_words_in_paragraph(paragraph, dictionary)
print(replaced_paragraph)