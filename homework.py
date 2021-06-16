import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, someone):
        self.records.append(someone)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(
            record.amount
            for record in self.records if record.date == today
        )

    def get_week_stats(self):
        week = dt.date.today() - dt.timedelta(days=7)
        today = dt.date.today()
        return sum(
            record.amount
            for record in self.records
            if week < record.date <= today
        )


class Record(Calculator):
    def __init__(self, amount, comment, date=None):
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.amount = amount
        self.comment = comment


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    EURO_RATE = 87.39
    USD_RATE = 71.78

    def get_today_cash_remained(self, currency='rub'):
        currency_dict = {'rub': (self.RUB_RATE, 'руб'),
                         'eur': (self.EURO_RATE, 'Euro'),
                         'usd': (self.USD_RATE, 'USD')}
        minus = self.limit - self.get_today_stats()
        if minus == 0:
            return 'Денег нет, держись'
        if currency not in currency_dict:
            raise ValueError('Плохая валюта')
        else:
            value = minus / currency_dict[currency][0]
            currency_1 = currency_dict[currency][1]
        if value > 0:
            return(f'На сегодня осталось {value:.2f} '
                   f'{currency_1}')
        modul = abs(value)
        return('Денег нет, держись: твой долг - '
               f'{modul:.2f} {currency_1}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        today_ate = self.limit - self.get_today_stats()
        if today_ate > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {today_ate} кКал')
        return 'Хватит есть!'


cash_calculator = CashCalculator(1000)
calories_calculator = CaloriesCalculator(3000)
cash_calculator.add_record(Record(amount=1, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=145, comment='кофе'))
calories_calculator.add_record(Record(amount=4145, comment='кофе'))

print(cash_calculator.get_today_cash_remained('rub'))
print(calories_calculator.get_calories_remained())
