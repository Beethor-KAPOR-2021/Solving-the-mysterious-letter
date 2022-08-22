import nltk

def txt_to_string(file_path):
    with open(file_path) as infile:
        file_string = infile.read()
    return file_string

def generate_author_dict():
    string_by_author = dict()
    string_by_author['unknown'] = txt_to_string(r"file book/lostbook.txt")
    string_by_author['J.K. Rowling'] = txt_to_string(r"file book/Harry-Potter-and-The-Sorcerer’s-Stone.txt")
    string_by_author['Robert T. Kiyosaki'] = txt_to_string(r"file book/Rich-Dad-Poor-Dad .txt")
    return string_by_author

def make_token_dict(string_by_author):
    token_by_author = dict()
    for author in string_by_author:
        author_string = string_by_author[author]
        author_token = nltk.word_tokenize(author_string)

        lower_author_token = []
        for token in author_token:
            if token.isalpha():
                lower_author_token.append(token.lower())

        token_by_author[author] = lower_author_token

    return token_by_author

def calculate_chi2(token_by_author):
    author_chi2_dict = dict()
    for author in token_by_author:
        if author != 'unknown':
            word_freq = nltk.FreqDist(token_by_author[author])
            combined_token = token_by_author['unknown'] + token_by_author[author]
            author_proportion = len(token_by_author[author]) / (len(combined_token))
            combined_freq = nltk.FreqDist(combined_token)
            combined_most_common = combined_freq.most_common(1000)

            author_chi2 = 0
            for word, combined_count in combined_most_common:
                word_count = word_freq[word]
                expected_word_count = combined_count * author_proportion
                word_chi2 = ((word_count - expected_word_count)**2)/expected_word_count
                author_chi2 += word_chi2

            author_chi2_dict[author] = author_chi2
    return author_chi2_dict

def main():
    string_by_author = generate_author_dict()
    token_by_author = make_token_dict(string_by_author)
    chi2_by_author = calculate_chi2(token_by_author)
    least_chi2_author = min(chi2_by_author,key=chi2_by_author.get)
    print(f'Mysterious book is likely to be written by... {least_chi2_author}')
    print(f'With chi2 of {chi2_by_author[least_chi2_author]}')

main()