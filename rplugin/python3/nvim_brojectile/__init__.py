import neovim
from .brojectile import Brojectile

@neovim.plugin
class BrojectileHandler(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.Brojectile = Brojectile(nvim)
