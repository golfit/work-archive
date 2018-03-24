from MDSplus import *

my_tree=Tree('test',-1,'edit')

#Set up nodes
try :
    my_tree.addNode('scratch','structure')
    my_node=my_tree.getNode('scratch')
    my_node.addNode('my_name','text')
    my_node.addNode('my_age','numeric')
    my_node.addNode('age_months','numeric')
    my_node.addNode('timebase','axis')
    my_node.addNode('my_cosine','signal')
except :
    print("Couldn't add scratch example nodes")

try :
    my_tree.addNode('demo_time','structure')
    my_node=my_tree.getNode('demo_time')
    my_node.addNode('tsync_sig','signal')
    my_node.getNode('tsync_sig').addNode('comment','text')
    my_node.getNode('tsync_sig.comment').record='Pulse-width-modulated signal encoding the global time.  The rising edges of pulses always occur at times that are integer multiples of 0.01 s on the global lab clock.  The duration of time that each pulse is on encodes the global time by the scale factor, 0.001 seconds of pulse on time = 1 s on the global clock.  A pulse duration of 0.00075 s then means that that lab time was 0.75 s at the rising edge of this pulse.'

    my_node.addNode('t_trig_ideal','numeric')
    my_node.getNode('t_trig_ideal').addNode('comment','text')
    my_node.getNode('t_trig_ideal.comment').record='Ideal trigger time [s] of the signal, which is likely in error from what the actual hardware achieved.'

    my_node.addNode('t_samp_ideal','numeric')
    my_node.getNode('t_samp_ideal').addNode('comment','text')
    my_node.getNode('t_samp_ideal.comment').record='Ideal sampling time [s] of the signal, which is likely in error from what the actual hardware achieved.'

    my_node.addNode('t_trig_corr','numeric')
    my_node.getNode('t_trig_corr').addNode('comment','text')
    my_node.getNode('t_trig_corr.comment').record='Corrected trigger time based on analysis of tsync_sig [s].'

    my_node.addNode('t_samp_corr','numeric')
    my_node.getNode('t_samp_corr').addNode('comment','text')
    my_node.getNode('t_samp_corr.comment').record='Corrected sampling time based on analysis of tsync_sig [s].'

except :
    print("Couldn't add demo_time nodes")

try :
    my_node=my_tree.getNode('demo_time')
    my_node.addNode('v_thresh','numeric')
    my_node.getNode('v_thresh').addNode('comment','text')
    my_node.getNode('v_thresh.comment').record='Threshold voltage delineating the boundary between the ON and OFF logic levels for tsync_sig [V].'
    my_node.getNode('v_thresh').record=2.5
except :
    print("Couldn't add threshold voltage node")

try :
    my_node=my_tree.getNode('demo_time.tsync_sig')
    my_node.addNode('raw_sig','numeric')
    my_node.addNode('ideal_time','axis')
except :
    print("Couldn't add numeric nodes for tsync_sig")

my_tree.write()
