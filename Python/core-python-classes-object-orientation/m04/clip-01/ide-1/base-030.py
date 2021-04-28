class Base:
    def __init__(self):
        print('Base initializer')

    def f(self):
        print('Base.f()')


class Sub(Base):
    def f(self):
        print('Sub.f()')
