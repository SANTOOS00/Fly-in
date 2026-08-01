def starts_a(w):
    return w.startswith("a")

li = ["apple", "banana", "avocado", "cherry", "apricot"]
res = filter(lambda x: x.startswith('a'), li)
print(list(res))