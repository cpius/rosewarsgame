class A:
    pass


a = A()
a.l = False
b = A()
c = A()
b.l = True
c.l = False

elems = [a,b,c]

print any(elem.l for elem in elems)