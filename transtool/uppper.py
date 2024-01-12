def capitalize_after_punctuation(string):
    punctuations = ['\n', '.', ',', '?', '!']
    sentences = string.split('. ')

    for i in range(len(sentences)):
        sentence = sentences[i]
        for punctuation in punctuations:
            if punctuation in sentence:
                words = sentence.split(punctuation)
                for j in range(len(words)):
                    if words[j].strip() != '':
                        words[j] = words[j].strip().capitalize()
                sentences[i] = punctuation.join(words)

    return '. '.join(sentences)

string = "this is a test. this is another test.\nthis is the last test."

result = capitalize_after_punctuation(string)

print(result)