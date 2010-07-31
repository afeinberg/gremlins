#!/usr/bin/env python

import signal

from gremlins import faults, metafaults, triggers

v_kill_long = faults.kill_daemons(["VoldemortServer"], signal.SIGKILL, 100)
v_kill_short = faults.kill_daemons(["VoldemortServer"], signal.SIGKILL, 3)

v_pause_long = faults.pause_daemons(["VoldemortServer"], 62)
v_pause_short = faults.pause_daemons(["VoldemortServer"], 3)

v_drop_inbound_packets = faults.drop_packets_to_daemons(["VoldemortServer"], 64)

profile = [
  triggers.Periodic(
    45,
    metafaults.pick_fault([
      (5, v_kill_long),
      (5, v_kill_short),

      # simulate a gc pause
      (10, v_pause_short),

      # simulate a longer pause
      (1, v_pause_long),
      
      # simulate a network outage
      (1, v_drop_inbound_packets)
      ]))
  ]
      
