# . = ;
# {} = =
# dec = int
# in = cin
# out = cout
# loop = for
# [ ] = { }
# < = <<
# > = >>
# ret = return
# & = +
# -> = for range
# ^x = sqrt(x)
# $ = *
# 17 = if
# >>> = >

# program 1

dec a.
in > a.
out < a.

a {} 0.
dec b {} a.
out < b.

ret 0.

# program 2

dec n.
in > n.
dec s {} 0.
loop 1 -> n:
[
    dec x.
    in > x.
    17 x >>> 0:
    [
        s {} s & x.
    ]

]
out < s.
ret 0 .

# program 3

dec a.
dec b.
in > a.
in > b.
loop 1 -> ^b:
[
    a {} a $ a.
]
out < a.

# program 4

dec a;
in > a.
for a -> n:
{
    a {} 0.
}
out < a.
