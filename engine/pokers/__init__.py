from pokers.junior import Junior
from pokers.calculator import Calculator

def create_poker(code, logger):
    if code == 'junior':
        poker = Junior(logger)
    elif code == 'calculator':
        poker = Calculator(logger)
    else:
        raise Exception('Invalid poker code %s' % code)
    return poker
