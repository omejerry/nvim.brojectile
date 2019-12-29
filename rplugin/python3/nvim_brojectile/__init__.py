import pynvim
from .brojectile import Brojectile

@pynvim.plugin
class BrojectileHandler(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.Brojectile = Brojectile(nvim)

    @pynvim.command('BtileList', nargs='*', sync=False)
    def read_Brojectile_bookmarks(self, args):
        if len(args) == 1:
            wrapcommand = "BtileCD {}".format(args[0])
        elif len(args) == 0:
            wrapcommand = 'BtileCD'
        else:
            self.Brojectile.error('BtileList takes 1 or 0 arguments, showing normal list')
            wrapcommand = 'BtileCD'

        self.nvim.async_call(self.Brojectile.fzf_call, wrapcommand)

    @pynvim.command('BtileAdd', sync=False)
    def add_Brojectile_pwd(self):
        pwd = self.nvim.command_output('pwd')
        self.Brojectile.add_bookmark(pwd)

    @pynvim.command('BtileDel', sync=False)
    def del_Brojectile_pwd(self):
        self.nvim.async_call(self.Brojectile.fzf_call, 'BtileRM')

    @pynvim.command('BtileRM', nargs=1, sync=True)
    def delete_entry(self, args):
        path = str(args).strip("[']").replace(' ', '').replace('\\', '')
        self.Brojectile.delete_bookmark(path)

    @pynvim.command('BtileCD', nargs='*', sync=False)
    def change_directory(self, args):
        if len(args) > 1:
            path = args[1]
            command = True
        else:
            path = args[0]
            command = False

        path = str(path).strip("[']").replace(' ', '').replace('\\', '')
        self.nvim.chdir(path)
        if command:
            self.nvim.command(args[0])

    @pynvim.function('Brojectile_list_bookmarks', sync=True)
    def list_bookmarks(self, args):
        self.Brojectile.read_bookmarks()
        return self.Brojectile.bookmarks['bookmarks']
