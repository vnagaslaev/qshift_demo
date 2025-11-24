
from cpymad.madx import Madx             # Python bridge to MAD-X
import xtrack as xt                      # Xsuite's high-level tracking API
import matplotlib.pyplot as plt          # Plotting
import xplt                              # Simple plotting helpers for Xsuite (e.g., FloorPlot)
import numpy as np                       # Arrays / numerics
import xobjects as xo                    # Backend/context management (CPU/GPU/etc.)
from docutils.writers.latex2e import block_name
#import random

ctx = xo.ContextCpu()

mad = Madx(stdout=False)                              # Start a fresh MAD-X session
mad.call('debuncher_seq.madx')            
mad.beam()  # Define a default "beam" block (uses defaults if not specified)
mad.use(sequence='debuncher')             # Activate the named sequence inside MAD-X

#  Define a function to build the tracker with debuncher ring
def build_line(seq, NT=1):
    line_l = xt.Line.from_madx_sequence(mad.sequence.debuncher)
# replace horizontal BPM elements (DRIFTS) with BeamPositionMonitor instances
    for name, element in line_l.element_dict.items():
        if(name.find("hbpm")>-1):
            new_el = xt.BeamPositionMonitor(start_at_turn=0, stop_at_turn=NT, )
            line_l.element_dict[name]=new_el
    line_l.build_tracker()
    return line_l

# %%
Npart=100
N_turn = 10
frev=5.9e5

line=build_line(seq=mad.sequence.debuncher,NT=N_turn)

# record a dictionary with BPM S-positions
# OK since it's all the same line structure every time
sbpms={}
s_positions=line.get_s_elements()
names=line.element_names
for name,s in zip(names,s_positions):
    if(name.find("hbpm")>-1):
        sbpms[name]=s

# %%
sh_list=[0.0, -1.0, 1.0]  #array of quad shifts in mm to loop
kick_data=[]                # BPM traces for each quad shift

# start loop over different quad shifts here
for sh in sh_list:
    print(f"Loop over quad shifts; sh={sh}")
# to re-build the line again: testing purposes - uncomment next line
#    line = build_line(seq=mad.sequence.debuncher, NT=N_turn)

# add a horizontal shift to the quad Q105
    line.element_dict["q105_"].shift_x = sh*0.001
# create reference orbit, generate the beam along the orbit, track it
    line.particle_ref = xt.Particles(q0=1, mass0=xt.PROTON_MASS_EV, p0c=8.89e9)
    x_gen = np.random.normal(loc=0.0, scale=0.001, size=Npart)
    particles = line.build_particles(x=x_gen, px=0, y=0, py=0, zeta=0, delta=0)
    line.track(particles, num_turns=N_turn)

# read the first turn TBT data from all BPMs
    turnsx1=[]
    for bname,s in sbpms.items():
        bpmX = line.element_dict[bname]
        xcords=bpmX.x_sum/Npart    # array of averages over Npart particles for this BPM
        turnsx1.append(xcords[0])  # coordinate at bpm bname on first turn
    kick_data.append(turnsx1)   # record first turn for quad shift sh

fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))
turnss=sbpms.values()    # S coordinates
#First turn orbit for Quad shift #1
axs[0,0].plot(turnss, kick_data[0], color='blue',linestyle='-',label=str(sh_list[0]))
axs[0, 0].set_title(f"Shift ={sh_list[0]}")
axs[0, 0].set_xlabel('X-axis')
axs[0, 0].set_ylim(-0.005,0.005)
axs[0, 0].set_ylabel('Y-axis')

#First turn orbit for Quad shift #2
axs[0,1].plot(turnss, kick_data[1], color='green',linestyle='-',label=str(sh_list[1]))
axs[0, 1].set_title(f"Shift ={sh_list[1]}")
axs[0, 1].set_xlabel('X-axis')
axs[0, 1].set_ylim(-0.005,0.005)
axs[0, 1].set_ylabel('Y-axis')

#First turn orbit for Quad shift #3
axs[1,0].plot(turnss, kick_data[2], color='red',linestyle='--',label=str(sh_list[2]))
axs[1, 0].set_title(f"Shift ={sh_list[2]}")
axs[1, 0].set_xlabel('X-axis')
axs[1, 0].set_ylim(-0.005,0.005)
axs[1, 0].set_ylabel('Y-axis')

#First turn orbit for Quad shift #3, zoomed
axs[1,1].plot(turnss, kick_data[2], color='red',linestyle='--',label=str(sh_list[2]))
axs[1, 1].set_title(f"Shift ={sh_list[2]} zoomed in")
axs[1, 1].set_xlabel('X-axis')
axs[1, 1].set_ylim(-0.001,0.001)
axs[1, 1].set_ylabel('Y-axis')

plt.tight_layout()
plt.show()






# %%

# %%
