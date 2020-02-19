#!/usr/bin/env python3
"""xob - A lightweight overlay volume/anything bar for the X Window System.
Copyright (C) 2018 Florent Ch.

xob is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

xob is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with xob.  If not, see <https://www.gnu.org/licenses/>.
"""

from pulsectl import Pulse, PulseLoopStop
import sys

# Adapt to your use-case
sink_id = 0

with Pulse() as pulse:
  def callback(ev):
    if ev.index == sink_id:
        raise PulseLoopStop
  try:
    pulse.event_mask_set('sink')
    pulse.event_callback_set(callback)
    last_value = round(pulse.sink_list()[sink_id].volume.value_flat * 100)
    last_mute = pulse.sink_list()[sink_id].mute == 1
    while True:
      pulse.event_listen()
      value = round(pulse.sink_list()[sink_id].volume.value_flat * 100)
      mute = pulse.sink_list()[sink_id].mute == 1
      if value != last_value or mute != last_mute:
        print(value, end='')
        if mute:
            print('!')
        else:
            print('')
        last_value = value
        last_mute = mute
      sys.stdout.flush()
  except:
    pass
