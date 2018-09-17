# -*- coding: utf-8 -*-

with open("referat.txt", 'r', encoding = "utf-8") as src_file:
    with open("referat2.txt", 'w', encoding = "utf-8") as dst_file:
        str_lenght = 0
        word_score = 0
        for ln in src_file:
            str_lenght += len(ln)

            dst_file.write(ln.replace('.','!'))

            word_score += len(ln.strip().split(' '))

print(str_lenght)
print(word_score)
