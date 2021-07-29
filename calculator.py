from __future__ import division
from pyparsing import (Literal, CaselessLiteral, Word, Combine, Group, Optional,
                       ZeroOrMore, Forward, nums, alphas, oneOf)
import math
import operator

__author__ = 'Paul McGuire'
__version__ = '$Revision: 0.0 $'
__date__ = '$Date: 2009-03-20 $'
__source__ = '''http://pyparsing.wikispaces.com/file/view/fourFn.py
http://pyparsing.wikispaces.com/message/view/home/15549426
'''
__note__ = '''
All I've done is rewrap Paul McGuire's fourFn.py as a class, so I can use it
more easily in other places.
'''


class NumericStringParser(object):
    '''
    Most of this code comes from the fourFn.py pyparsing example

    '''

    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.exprStack.append('unary -')

    def __init__(self):
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        point = Literal(".")
        e = CaselessLiteral("E")
        fnumber = Combine(Word("+-" + nums, nums) +
                          Optional(point + Optional(Word(nums))) +
                          Optional(e + Word("+-" + nums, nums)))
        ident = Word(alphas, alphas + nums + "_$")
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        div = Literal("/")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        addop = plus | minus
        multop = mult | div
        expop = Literal("^")
        pi = CaselessLiteral("PI")
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                 (ident + lpar + expr + rpar | pi | e | fnumber).setParseAction(self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar + expr + rpar)
                ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + \
            ZeroOrMore((expop + factor).setParseAction(self.pushFirst))
        term = factor + \
            ZeroOrMore((multop + factor).setParseAction(self.pushFirst))
        expr << term + \
            ZeroOrMore((addop + term).setParseAction(self.pushFirst))
        # addop_term = ( addop + term ).setParseAction( self.pushFirst )
        # general_term = term + ZeroOrMore( addop_term ) | OneOrMore( addop_term)
        # expr <<  general_term
        self.bnf = expr
        # map operator symbols to corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = {"+": operator.add,
                    "-": operator.sub,
                    "*": operator.mul,
                    "/": operator.truediv,
                    "^": operator.pow}
        self.fn = {"sin": math.sin,
                   "cos": math.cos,
                   "tan": math.tan,
                   "exp": math.exp,
                   "abs": abs,
                   "trunc": lambda a: int(a),
                   "round": round,
                   "sgn": lambda a: abs(a) > epsilon and cmp(a, 0) or 0}

    def evaluateStack(self, s):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack(s)
        if op in "+-*/^":
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            return self.opn[op](op1, op2)
        elif op == "PI":
            return math.pi  # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            return 0
        else:
            return float(op)

    def eval(self, num_string, parseAll=True):
        self.exprStack = []
        results = self.bnf.parseString(num_string, parseAll)
        val = self.evaluateStack(self.exprStack[:])
        return val
nsp=NumericStringParser()
from tkinter import *
import math
root=Tk()
root.geometry("345x567")
root.maxsize(345,567)
root.minsize(345,567)
root.title("Welcome to Saurav's Calculator")
root.wm_iconbitmap("1_icon.ico")
nsp = NumericStringParser()
# screen
scvalue = StringVar()
scvalue.set("")
screen=Entry(root,textvariable=scvalue,font="arial 20 bold")
screen.grid(row=0,column=0,ipadx=16)
def click(event):
    global scvalue
    text = event.widget.cget("text")
    if text == "=":
        if scvalue.get().isdigit():
            value = int(scvalue.get())
        else:
            try:
                value = nsp.eval(screen.get())
            except Exception as e:
                print(e)
                value = "Error"
        scvalue.set(value)
        screen.update()
    elif text == "C":
        scvalue.set("")
        screen.update()
    else:
        scvalue.set(scvalue.get() + text)
        screen.update()
# button frame
frame_buttons=Frame(root,borderwidth=5,bg="grey",relief=SUNKEN)
frame_buttons.grid()
# button9
button9=Button(frame_buttons,text="9", font="arial 16 bold",padx=20,pady=10)
button9.grid(row=0,column=0,ipadx=20)
button9.bind('<Button-1>',click)
# button 8
button8=Button(frame_buttons,text="8", font="arial 16 bold",padx=20,pady=10)
button8.grid(row=0,column=1,ipadx=20)
button8.bind('<Button-1>',click)
# button 7
button7=Button(frame_buttons,text="7", font="arial 16 bold",padx=20,pady=10)
button7.grid(row=0,column=2,ipadx=20)
button7.bind('<Button-1>',click)
# button 6
button6=Button(frame_buttons,text="6", font="arial 16 bold",padx=20,pady=10)
button6.grid(row=1,column=0,ipadx=20)
button6.bind('<Button-1>',click)
# button 5
button5=Button(frame_buttons,text="5", font="arial 16 bold",padx=20,pady=10)
button5.grid(row=1,column=1,ipadx=20)
button5.bind('<Button-1>',click)
# button 4
button4=Button(frame_buttons,text="4", font="arial 16 bold",padx=20,pady=10)
button4.grid(row=1,column=2,ipadx=20)
button4.bind('<Button-1>',click)
# button 3
button3=Button(frame_buttons,text="3", font="arial 16 bold",padx=20,pady=10)
button3.grid(row=2,column=0,ipadx=20)
button3.bind('<Button-1>',click)
# button 2
button2=Button(frame_buttons,text="2", font="arial 16 bold",padx=20,pady=10)
button2.grid(row=2,column=1,ipadx=20)
button2.bind('<Button-1>',click)
# button 1
button1=Button(frame_buttons,text="1", font="arial 16 bold",padx=20,pady=10)
button1.grid(row=2,column=2,ipadx=20)
button1.bind('<Button-1>',click)
#button 0
button0=Button(frame_buttons,text="0", font="arial 16 bold",padx=20,pady=10)
button0.grid(row=3,column=0,ipadx=20)
button0.bind('<Button-1>',click)
#plus button
button_plus=Button(frame_buttons,text="+", font="arial 16 bold",padx=20,pady=10)
button_plus.grid(row=3,column=1,ipadx=20)
button_plus.bind('<Button-1>',click)
#subtract button
button_subtract=Button(frame_buttons,text="-", font="arial 16 bold",padx=23,pady=10)
button_subtract.grid(row=3,column=2,ipadx=20)
button_subtract.bind('<Button-1>',click)
#divide button
button_divide=Button(frame_buttons,text="/", font="arial 16 bold",padx=23,pady=10)
button_divide.grid(row=4,column=0,ipadx=20)
button_divide.bind('<Button-1>',click)
# multiply button
button_multiply=Button(frame_buttons,text="*", font="arial 16 bold",padx=22,pady=10)
button_multiply.grid(row=4,column=1,ipadx=20)
button_multiply.bind('<Button-1>',click)
# percent button
button_percent=Button(frame_buttons,text="%", font="arial 16 bold",padx=18,pady=10)
button_percent.grid(row=4,column=2,ipadx=20)
button_percent.bind('<Button-1>',click)
# squrare root button
button_squareroot=Button(frame_buttons,text="sqrt", font="arial 16 bold",padx=6,pady=10)
button_squareroot.grid(row=5,column=0,ipadx=20)
button_squareroot.bind('<Button-1>',click)
# square button
button_sqaure=Button(frame_buttons,text="^2", font="arial 16 bold",padx=14,pady=10)
button_sqaure.grid(row=5,column=1,ipadx=20)
button_sqaure.bind('<Button-1>',click)
# log button
button_log=Button(frame_buttons,text="log", font="arial 16 bold",padx=11,pady=10)
button_log.grid(row=5,column=2,ipadx=20)
button_log.bind('<Button-1>',click)
# sin button
button_sin=Button(frame_buttons,text="sin", font="arial 16 bold",padx=11,pady=10)
button_sin.grid(row=6,column=0,ipadx=20)
button_sin.bind('<Button-1>',click)
# cos button
button_cos=Button(frame_buttons,text="cos", font="arial 16 bold",padx=8,pady=10)
button_cos.grid(row=6,column=1,ipadx=20)
button_cos.bind('<Button-1>',click)
# equals button
button_equal=Button(frame_buttons,text="=", font="arial 16 bold",padx=20,pady=10)
button_equal.grid(row=6,column=2,ipadx=20)
button_equal.bind('<Button-1>',click)
# reset  button
button_reset=Button(frame_buttons,text="C", font="arial 16 bold",padx=18,pady=11)
button_reset.grid(row=7,column=0,ipadx=20)
button_reset.bind('<Button-1>',click)
# decimal button
button_decimal=Button(frame_buttons,text=".", font="arial 16 bold",padx=23,pady=11)
button_decimal.grid(row=7,column=1,ipadx=20)
button_decimal.bind('<Button-1>',click)
# double 00
button_doublezero=Button(frame_buttons,text="00", font="arial 16 bold",padx=15,pady=11)
button_doublezero.grid(row=7,column=2,ipadx=20)
button_doublezero.bind('<Button-1>',click)
# ----------------------------------------------------------------------------------------
root.mainloop()
