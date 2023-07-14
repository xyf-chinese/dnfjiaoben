from tkinter import *
import selectchc_copy

window = Tk()
window.title("First Window")
window.geometry('600x600')

# 创建标签
label = Label(window, text="从第几个角色开始刷")
label.grid(row=0, column=0, columnspan=2, pady=(200, 10))

# 创建输入框
entry = Entry(window, width=10)
entry.grid(row=1, column=0, padx=20)

# 创建按钮，点击按钮时打印输入框的内容
button = Button(window, text="开始运行", command=lambda: selectchc_copy.jiaobenyunxing(int(entry.get())))
button.grid(row=1, column=1, padx=20)

window.mainloop()
