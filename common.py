# common functions
#
#*-- convert to meter per second from kmph
def meter_per_second(kmph):
    return (kmph * 0.2777777777777777778)

#*-- convert to kmph from meter per seocond
def kmph(mps):
    return (mps * (18.0 / 5.0))

#*-- return a nice string with 2 decimal places
def nice_s(x):
    return str(float("{:3.2f}".format(x)))


