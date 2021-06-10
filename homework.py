import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.week = dt.date.today() - dt.timedelta(days=7)

    def add_record(self, someone):
        self.records.append(someone)

    def get_today_stats(self):
        today_stats = 0
        for i in self.records:
            if i.date == dt.date.today():
                today_stats += i.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        for i in self.records:
            if i.date <= self.week <= dt.date.today():
                week_stats += i.amount
        return week_stats

    pass


class CashCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency='rub'):
        dic_currency = {'rub': 1, 'eur': 70, 'usd': 60}
        self.currency = currency
        today_remained = 0
        for i in self.records:
            if self.currency == 'rub':
                today_remained = self.limit - self.get_today_stats()
            elif self.currency == 'eur':
                cur = dic_currency[self.currency]
                today_remained = self.limit - (self.get_today_stats() / cur)
            elif self.currency == 'usd':
                cur = dic_currency[self.currency]
                today_remained = self.limit - (self.get_today_stats() / cur)
        if today_remained > 0:
            return f'На сегодня осталось {today_remained} {self.currency}'
        elif today_remained == 0:
            return 'Денег нет, держись'
        else:
            today_remained *= (-1)
            return ('Денег нет, держись: твой долг - '
                    f'{self.today} {self.currency}')


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        today_ate = 0
        for i in self.records:
            self.today_ate = self.limit - self.get_today_stats()
        if today_ate > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {self.limit - today_ate} кКал')
        else:
            return 'Хватит есть!'


class Record(Calculator):
    def __init__(self, amount, comment, date=None):
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = date
        self.amount = amount
        self.comment = comment
    pass


cash_calculator = CashCalculator(1000)
calories_calculator = CaloriesCalculator(3000)
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=145, comment='кофе'))
calories_calculator.add_record(Record(amount=145, comment='кофе'))

print(cash_calculator.get_today_cash_remained('rub'))
print(calories_calculator.get_calories_remained())
