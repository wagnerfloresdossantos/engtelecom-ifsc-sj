from poller import Callback

class Subcamada(Callback):

  def __init__(self, fd, tout):
    Callback.__init__(self, fd, tout)
    self.upper = None
    self.lower = None
  
  def envia(self, dados):
    raise NotImplementedError('abstrato')

  def recebe(self, dados):
    raise NotImplementedError('abstrato')

  def conecta(self, superior):
    self.upper = superior
    superior.lower = self
    