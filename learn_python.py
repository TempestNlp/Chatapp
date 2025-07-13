def sub_generator():
    total = 0
    while True:
        value = yield  # 接收外部发送的值
        if value is None:
            return total  # 返回总和给主生成器
        total += value

def main_generator():
    result = yield from sub_generator()  # 接收子生成器的返回值
    yield f"Total: {result}"

# 使用示例
gen = main_generator()
next(gen)  # 启动主生成器，执行到第一个 yield

gen.send(10)  # 发送值到子生成器
gen.send(20)  # 发送值到子生成器
gen.send(None)  # 终止子生成器，触发返回值

# 输出: Total: 30
print(next(gen))