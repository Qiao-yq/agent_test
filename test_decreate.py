class decreate():
    def __init__(self, f, *args, **kwargs):
        # self.func = f
        f(*args, **kwargs)
        print("use it")
        # self.func = f
    
    def __call__(self, *args, **kwargs):
        # print("before call")
        # res = self.func(*args, **kwargs)
        print("after call")
        # return res
        return 12

@decreate
def test(*args, **kwargs):
    print("IT")
    return 12

# test()
# func = decreate(test)
# func()

# def decreate2(func):
#     def wrapper(*args, **kwargs):
#         print("before call")
#         res = func(*args, **kwargs)
#         print("after call")
#         return res
#     return wrapper

# # @decreate2
# def test2(*args, **kwargs):
#     print("in test2")
#     return 12

# #test2()
# func2 = decreate2(test2)
# func2()