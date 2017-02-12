from numpy import diff, mean, abs, sum
from numpy.lib import pad
from numpy.linalg import norm


def similarity(g1, g2):
  s = []
  for i in xrange(len(g1.contact_streams)):
    s.append(similarity_contact_stream(g1.contact_streams[i], g2.contact_streams[i]))

  return mean(s)

# Returns a score with how different two contact streams are.
# Lower scores indicates higher similarity.
def similarity_contact_stream(g1, g2):
  # Get the similarity of the different vectors.
  similarities = [
    similarity_vector(g1.x_pos, g2.x_pos),
    similarity_vector(g1.y_pos, g2.y_pos),
    similarity_vector(g1.total_force, g2.total_force),
    similarity_vector(g1.major_axis, g2.major_axis),
    similarity_vector(g1.minor_axis, g2.minor_axis)
  ]

  print "similarities", similarities

  return mean(similarities)

def similarity_vector(v1, v2):
  # For all the features we have, we only care about the rate of change as
  # opposed to the actual values. We'll start by getting the derivatives.

  diff_g1 = diff(v1)
  diff_g2 = diff(v2)

  print 'original', v1
  print 'diff', diff_g1
  print 'original', v2
  print 'diff', diff_g2

  # Pad vectors with zero if necessary to make sure they are the same length.
  diff_g1, diff_g2 = pad_vectors(diff_g1, diff_g2)

  # Return the euclidean distance
  return sum(abs(diff_g1 - diff_g2)) #norm(diff_g1 - diff_g2)


def pad_vectors(v1, v2):
  """Return the two vectors, but padding them with zeros as necessary to
  be the same length.
  """
  if len(v1) < len(v2):
    # pad v1
    v1 = pad(v1, (0, len(v2) - len(v1)), 'constant', constant_values=(0,0)) 
  elif len(v2) < len(v1):
    # pad v2
    v2 = pad(v2, (0, len(v1) - len(v2)), 'constant', constant_values=(0,0)) 

  return v1, v2
