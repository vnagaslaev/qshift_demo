  Issue with the orbit change due to the kcik produced by the quadrupole magnet,
  When a single Quad.shift_x is assigned a non-zero value X0, a single pass orbit reflects correctly the kick produced by this quad.
  However, if then Quad.shift_x is assigned an opposite value -X0, it does not result in an opposite kick by this quad.
  Instead, the orbit is flat like if the kick is cancelled.

Here we:

1.	Build the beam line from the madx sequence file
2.	Set up the BPMs 
3.	Initiate the beam of Npart particles with zero coordinates. Track the beam and read BPMs and record
coordinates for the very first turn.
4.	The beam is expected to produce zeros at all bpms in normal conditions.
5.	Copare 4 beam runs with a selected quadrupole (Q105) shifted in x:
	a.	Normal run:  shift_x=0:  expect to read all zeros in bpms
	b.	Shift_x=-1.0mm: expect to see an orbit kick at the location of affected quad
	c.	Shift_x=1.0mm: expect to see an opposite kick at the same location
	d.	Shift_x=1.0mm again expect to make no change
6.	Plotting the orbits, observe
	a.	Shift_x=0:  orbit is exactly zero (within statistics)
	b.	Shift=-1.0:  single kick at q105
	c.	Shift_x=1.0: no kick seen. Why?  Kick canceled?
	d.	Shift_x=1.0: supposed to repeat #c, instead - kick opposite to #b is observed now
7.	Repeat the same, but now please uncomment line #53 to rebuild the beam line for each run.
	a.	Shift_x=0.0: the same
	b.	Shift_x=-1.0: kick at q105
	c.	Shift_x=1.0: now there is an opposite kick at q105.
	d. 	Shift_x=1.0:  same orbit as in #c again
8.	Why it needs to rebuild the beam line to reset the reference orbit?
9.	Is the reference orbit changing at some point?
