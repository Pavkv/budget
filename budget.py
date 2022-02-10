class Category:
    def __init__(self, _name, _data):
        self.name = _name
        self.data = _data

    def deposit(self, amount, description):
        self.data.append({"amount": amount, "description": description})
        return self.data[-1]

    def withdraw(self, amount, description):
        if self.getBalance() > amount:
            self.data.append({"amount": -abs(amount), "description": description})
            return True
        else:
            return False

    def getBalance(self):
        balance = 0
        for elem in self.data:
            balance += elem['amount']
        return balance

    def transfer(self, amount, _name):
        if self.withdraw(amount, 'Transfer to ' + _name.name):
            _name.deposit(amount, 'Transfer from  ' + self.name)
            return True
        else:
            return False

    def check_funds(self, amount):
        if self.getBalance() > amount:
            return True
        else:
            return False

    def getBudget(self):
        topRow = '*' * 15 + self.name + '*' * 15
        itemsRos = []
        for item in self.data:
            desc = item['description']
            if len(desc) > 23:
                s = []
                s.extend(desc)
                del s[22: -1]
                desc = ''.join(s)
            itemsRos.append(desc + ' ' * (len(topRow) - len(desc) - len(str(item['amount']))) + str(item['amount']))
        itemsRos.insert(0, topRow)
        itemsRos.append('Total: ' + str(self.getBalance()))
        return '\n'.join(itemsRos)


def create_spend_chart(*args):
    budgets = []
    summ = 0
    for item in args:
        summ += item.getBalance()
        budgets.append([item.name, item.getBalance()])
    for item in budgets:
        item[1] = round(round(item[1]) / round(summ) * 100, -1)
    l = 0
    for item in budgets:
        if len(item[0]) > l:
            l = len(item[0])
    for item in budgets:
        item[0] += ' ' * (l - len(item[0]))
    verticalLine = []
    for f in range(0, 110, 10):
        verticalLine.insert(0, [' ' * (3 - len(str(f))) + str(f) + '|'])
    horizontalLine = ['-' * (len(args) * 3)]
    s = [[]]
    for item in budgets:
        for i in range(len(item[0])):
            if not s[i]:
                s.append([])
            s[i].append(item[0][i])
    del s[-1]
    for item in s:
        item.insert(0, ' ' * 3)
    verticalLine.reverse()
    for item in budgets:
        if item[1] == 0:
            verticalLine[0].append('o ')
        else:
            for i in range(0, int(item[1]) + 10, +10):
                verticalLine[i // 10].append('o ')
        for i in range(int(item[1]) + 10, 110, +10):
            verticalLine[i // 10].append('- ')

    verticalLine.reverse()
    print('Percentage spent by category')
    print('\n'.join(map(' '.join, verticalLine)))
    print(' ' * 4 + ''.join(horizontalLine))
    print('\n'.join(map('  '.join, s)))


food = Category('Food', [])
clothing = Category('Clothing', [])
entr = Category('Entr', [])
work = Category('Work', [])
entr.deposit(1283.42, 'from friend')
entr.withdraw(1123.90, 'to friend')
entr.deposit(12334, 'yes')
entr.transfer(0.1, clothing)
food.deposit(1000.15, 'initial deposit')
food.withdraw(100.05, 'groceries')
food.getBalance()
food.transfer(150, clothing)
food.deposit(15.375, 'from friend for restaurant')
work.deposit(1400.48, 'no')
work.withdraw(13.48, 'yes')
clothing.getBalance()
food.check_funds(205.75)
print(food.getBudget())
print()
print(create_spend_chart(food, clothing, entr, work))