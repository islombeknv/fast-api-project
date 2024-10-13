from app.calculations import InsufficientFunds, add, multiply, subtract, divide, BankAccount
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize('num1, num2, expected', [
    (1, 2, 3),
    (4, 2, 6),
    (7, 6, 13)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(4, 2) == 2

def test_divide():
    assert divide(10, 2) == 5

def test_multiple():
    assert multiply(5, 3) == 15


def test_bank_set_initial_amount():
    bank = BankAccount(50)
    assert bank.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(30)
    assert bank_account.balance == 20

def test_deposit(zero_bank_account):
    zero_bank_account.deposit(20)
    assert zero_bank_account.balance == 20


def test_collect_interest(bank_account):

    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)

])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)