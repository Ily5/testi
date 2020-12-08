from jiwer import wer

# ground_truth = "hello world"
# hypothesis = "hello duck"
#
# error = wer(ground_truth, hypothesis)
# error2 = mer(ground_truth, hypothesis)
# error3 = wil(ground_truth, hypothesis)
# print(error)
# print(error2)
# print(error3)

# g = ' '.join(list("helloworld"))
# h = ' '.join(list("hellodu"))
# h = list("hello duck")
# g = "hello world hello retard hello"
# h = "hello world hell not"
g = list("helloboy")
h = list("hell")

error4 = wer(g, h)
print(g)
print(h)
print(error4)
# error = S+D+I/N
# n = "Hello world"
# m = "Hello guys"
# error = wer(n, m)
# print(error)

n = "Hello world"
m = "world Hello"

# s = "але ой извините пока нет щас я на работе извините пожалуйста я просто никак сейчас угу так а а по цене это будет сколько коллер да",
# z = "але ой извините пока нет щас я на работе извините пожалуйст я  никак сейчас угу так а а по цене это будет привет сколько коллер да",

