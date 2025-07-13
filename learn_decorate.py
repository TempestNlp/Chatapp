import functools

# '''
#     简单装饰器原理
# '''
# def my_decorator(func):
#     def wrapper():
#         print("在原函数执行前做一些事情")
#         func()  # 调用原函数
#         print("在原函数执行后做一些事情")
#     return wrapper  # 返回新函数

# @my_decorator
# def say_hello():
#     print("Hello!")

# 等价于：say_hello = my_decorator(say_hello)
#
# say_hello()
# 输出：
# 在原函数执行前做一些事情
# Hello!
# 在原函数执行后做一些事情

# '''
#     原函数带有参数的装饰器原理
# '''
# def my_decorator2(func):
#     def warpper(*args,**kwargs):
#         print("在原函数执行前做一些事情")
#         func(*args,**kwargs)
#         print("在原函数执行后做一些事情")
#     return warpper

# @my_decorator2
# def add(a,b):
#     print(a + b)

# add(4,5)



'''
     类作为装饰器的用法
'''
class CountCalls:
    def __init__(self,func):
        self.func = func
        self.count = 0
    
    def __call__(self,*args,**kwargs):
        self.count += 1
        print(f'第{self.count}次调用')
        return self.func(*args,**kwargs)



@CountCalls
def add2(a,b):
    return a+b

print(add2(2,3))
print(add2(5,6))