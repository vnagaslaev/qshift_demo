  In this example I am having issue with the orbit change due to the kcik produced by the quadrupole magnet,
  shifted horizontally by assigning shift_x=!=0

Here we:

1.	Build the beam line from the madx sequence file
2.	Set up the BPMs 
3.	Initiate the beam of Npart particles with zero coordinates. Track the beam and read BPMs and record
coordinates for the very first turn.
4.	The beam is expected to produce zeros at all bpms in normal conditions.
5.	Copare 3 beam runs with a selected quadrupole (Q105) shifted in x:
	a.	Normal run:  shift_x=0:  expect to read all zeros in bpms
	b.	Shift_x=-1.0mm: expect to see an orbit kick at the location of affected quad
	c.	Shift_x=1.0mm: expect to see an opposite kick at the same location
6.	Plot the orbits:
	a.	Shift_x=0:  orbit is not exactly zero (why?  May be a smoking gun?)
	b.	Shift=-1.0:  single kick at q105
	c.	Shift_x=1.0: no kick seen. Why?  Kick canceled? 
7.	Repeat the same, but now please uncomment line #53 to rebuild the beam line for each run.
	a.	Shift_x=0.0: the same
	b.	Shift_x=-1.0: the same
	c.	Shift_x=1.0: now there is an opposite kick at q105.
8.	Why it needs to rebuild the beam line to reset the reference orbit?
9.	Why the orbit in the first pass is not exactly zero?
