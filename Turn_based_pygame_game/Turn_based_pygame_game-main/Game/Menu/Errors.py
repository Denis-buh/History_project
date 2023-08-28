



class BreakError(Exception):
    '''Класс ошибки при выходе из игры'''
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'BreakError, {0} '.format(self.message)
        else:
            return 'BreakError'
