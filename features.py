import matplotlib.pyplot as plt
from numpy import append, array, diff

class ContactStream(object):
  def __init__(self):
    self.x_pos = array([])
    self.y_pos = array([])
    self.orientation = array([])
    self.major_axis = array([])
    self.minor_axis = array([])
    self.total_force = array([])

  def append(self, event):
    self.x_pos = append(self.x_pos, event.x_pos)
    self.y_pos = append(self.y_pos, event.y_pos)
    self.total_force = append(self.total_force, event.total_force)
    self.orientation = append(self.orientation, event.orientation)
    self.minor_axis = append(self.minor_axis, event.minor_axis)
    self.major_axis = append(self.major_axis, event.major_axis)

  def plot(self, graph):
    graph.plot(self.x_pos, label='x pos')
    graph.plot(self.y_pos, label='y pos')
    graph.plot(self.orientation, label='orientation')
    graph.plot(self.major_axis, label='major axis')
    graph.plot(self.minor_axis, label='minor axis')
    graph.plot(self.total_force, label='force')
    graph.legend()


class Gesture(object):
  def __init__(self, contact_streams):
    # remove all zero length contact_streams
    contact_streams = [x for x in contact_streams if len(x.x_pos) > 0]
    self.contact_streams = sorted(contact_streams, cmp=lambda x,y: cmp(x.x_pos[0], y.x_pos[0]))

  def plot(self):
    fig = plt.figure()

    for i in xrange(1, 6):
      if i > len(self.contact_streams):
        sp = fig.add_subplot(5, 1, i)
        continue

      sp = fig.add_subplot(5, 1, i)
      self.contact_streams[i - 1].plot(sp)

    plt.show()
      

def get_features(gesture):
  cs = gesture.contact_streams

  return array([
      # Distance between x's
      get_mid(cs[1].x_pos) - get_mid(cs[0].x_pos),
      get_mid(cs[2].x_pos) - get_mid(cs[1].x_pos),
      get_mid(cs[3].x_pos) - get_mid(cs[2].x_pos),
      get_mid(cs[4].x_pos) - get_mid(cs[3].x_pos),

      # Distance between y's
      get_mid(cs[1].y_pos) - get_mid(cs[0].y_pos),
      get_mid(cs[2].y_pos) - get_mid(cs[1].y_pos),
      get_mid(cs[3].y_pos) - get_mid(cs[2].y_pos),
      get_mid(cs[4].y_pos) - get_mid(cs[3].y_pos),
  ])

def get_mid(a):
  return a[len(a) / 2]

def similarity_vector(v1, v2):
  # Return the euclidean distance
  return sum(abs(v1 - v2))
