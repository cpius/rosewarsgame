import copy

class A(object):
        pass


a = A()

a.v1 = 7



b = copy.copy(a)

c = a


b.v1 = 8

print a.v1
print b.v1
print c.v1

