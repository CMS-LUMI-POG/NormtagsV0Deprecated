#!/usr/bin/python

# Calculates the coefficients for the PLT polynomial
# given the sigmavis and the accidental corrections.

sigmavis=float(raw_input("Enter the sigmaVis (1e30): "))
acc0=float(raw_input("Enter the accidental constant term (no negative sign): "))
acc1=float(raw_input("Enter the accidental linear term (no negative sign): "))

k=11246.0/sigmavis
p2=-(k*k*acc1)
p1=k*(1-acc0)

print "Coefficients are: %f, %f, %f" % (p2, p1, 0)
