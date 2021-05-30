word1 = input()
word2 = input()

# How many letters does the longest word contain?
longest = word1
if len(word2) > len(word1):
    longest = word2
print(len(longest))
