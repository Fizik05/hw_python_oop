import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.week = dt.date.today() - dt.timedelta(days=7)
        self.today = dt.date.today()

    def add_record(self, someone):
        self.records.append(someone)

    def get_today_stats(self):
        today_stats = 0
        for i in self.records:
            if i.date == self.today:
                today_stats += i.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        for i in self.records:
            if self.week <= i.date <= self.today:
                week_stats += i.amount
        return week_stats


class CashCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    EURO_RATE = 87.39
    USD_RATE = 71.78

    def get_today_cash_remained(self, currency='rub'):
        self.currency = currency
        currency_dict = {'rub': 'руб',
                         'eur': 'Euro',
                         'usd': 'USD'}
        conv = self.limit - self.get_today_stats()
        today_remain: float = 0
        if self.currency == 'rub':
            today_remain = round(conv)
        elif self.currency == 'usd':
            today_remain = round(conv / self.USD_RATE)
        elif self.currency == 'eur':
            today_remain = round(conv / self.EURO_RATE)
        if today_remain > 0:
            return(f'На сегодня осталось {today_remain:.2f} '
                   f'{currency_dict[self.currency]}')
        elif today_remain == 0:
            return('Денег нет, держись')
        else:
            return('Денег нет, держись: твой долг - '
                   f'{abs(today_remain):.2f} {currency_dict[self.currency]}')


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        today_ate = self.limit - self.get_today_stats()
        if today_ate > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {today_ate} кКал')
        else:
            return 'Хватит есть!'


class Record(Calculator):
    def __init__(self, amount, comment, date=None):
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.amount = amount
        self.comment = comment


cash_calculator = CashCalculator(1000)
calories_calculator = CaloriesCalculator(3000)
cash_calculator.add_record(Record(amount=85674, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=145, comment='кофе'))
calories_calculator.add_record(Record(amount=4145, comment='кофе'))

print(cash_calculator.get_today_cash_remained('eur'))
print(calories_calculator.get_calories_remained())
