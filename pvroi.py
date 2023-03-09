from numpy_financial import irr

def flow(pi, Q, p_S, p_B, O_0, d_T, T, P):
    yield -P
    for m in range(0, 12*T):
        output = (O_0/12)*(1 - m*(1-d_T)/(12*T))
        saved = output*Q*p_B*pow(1+pi/12, m)
        sold = output*(1-Q)*p_S
        print("m: %d, output: %f, saved: %f, sold: %f" % (m, output, saved, sold))
        yield saved + sold

pi = 0.02
Q = 0.25
p_S=0.082
p_B=0.3
O_0 = 900
d_T = 0.8
T=25
P=2000

g = flow(pi, Q, p_S, p_B, O_0, d_T, T, P)
for v in g:
    print(v)

print(irr(list(flow(pi, Q, p_S, p_B, O_0, d_T, T, P))))