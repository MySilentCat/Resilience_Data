# 正则表达式匹配\n和偶数个空格的
import re
re1 = re.compile(r'\n((\s)^(m+1)), such that m>=0, m mod 2 = 1')
# 匹配偶数个空格的正则表达式
str = "hello\n    world"
# 按re1的规则进行分割
print(re1.split(str))