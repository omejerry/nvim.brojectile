import pynvim
import os
import json
from pathlib import Path

@pynvim.plugin
class Brojectile(object):

    def __init__(self, nvim):
        self.nvim           = nvim
        self.options        = {
                'logging'       : True,
                'bookmark_dir'  : "{}/.config/nvim/nvim_brojectile".format(os.environ["HOME"]),
                'bookmark_file' : '.bookmarks.cache',
                'cd_command'    : 'FZF',
        }
        self.bookmarks      = {'bookmarks': []}
        self.bookmarks_file = "{}/{}".format(self.options['bookmark_dir'],
                                             self.options['bookmark_file'])

        self.get_opts()
        self.clean_bookmarks()

    def get_opts(self):
        for opt in self.options.keys():
            try:
                self.options[opt] = self.nvim.eval("Brojectile#options#{}".format(opt))
            except Exception:
                None

    @pynvim.command('BtileList', nargs='*', sync=False)
    def read_Brojectile_bookmarks(self, command_after_cd=False):
        if command_after_cd:
            wrapcommand = "fzf#wrap({'source': Brojectile_list_bookmarks(), 'sink': 'BtileCDCommand'})"
        else:
            wrapcommand = "fzf#wrap({'source': Brojectile_list_bookmarks(), 'sink': 'BtileCD'})"
        fzf_wrap = self.nvim.eval(wrapcommand)
        self.nvim.call("fzf#run", fzf_wrap)

    @pynvim.command('BtileAdd', sync=False)
    def add_Brojectile_pwd(self):
        pwd = self.nvim.command_output('pwd')
        self.add_bookmark(pwd)

    @pynvim.command('BtileDel', sync=False)
    def del_Brojectile_pwd(self):
        fzf_wrap = self.nvim.eval("fzf#wrap({'source': Brojectile_list_bookmarks(), 'sink': 'BtileRM'})")
        self.nvim.call("fzf#run", fzf_wrap)

    @pynvim.command('BtileRM', nargs=1, sync=True)
    def delete_entry(self, args):
        path = str(args).strip("[']").replace(' ', '').replace('\\', '')
        while path in self.bookmarks['bookmarks']:
            self.bookmarks['bookmarks'].remove(path)
        self.write_bookmarks()

    @pynvim.command('BtileCD', nargs=1, sync=False)
    def change_directory(self, args):
        path = str(args).strip("[']").replace(' ', '').replace('\\', '')
        self.nvim.chdir(path)

    @pynvim.command('BtileCDCommand', nargs=1, sync=False)
    def change_directory_and_command(self, args):
        self.change_directory(args)
        self.nvim.command(self.options['cd_command'])

    @pynvim.function('Brojectile_list_bookmarks', sync=True)
    def list_bookmarks(self, args):
        self.read_bookmarks()
        return self.bookmarks['bookmarks']

    def clean_bookmarks(self):
        self.read_bookmarks()
        for bookmark in self.bookmarks['bookmarks']:
            if not os.path.exists(bookmark):
                while bookmark in self.bookmarks['bookmarks']:
                    self.bookmarks['bookmarks'].remove(bookmark)
        self.write_bookmarks()

    def add_bookmark(self, path):
        self.read_bookmarks()
        if path not in self.bookmarks['bookmarks']:
            self.bookmarks['bookmarks'].append(path)
        self.write_bookmarks()
        self.debug(path)

    def test_file(self):
        if not os.path.exists(self.options['bookmark_dir']):
            os.makedirs(self.options['bookmark_dir'])
        if not os.path.isfile(self.bookmarks_file):
            Path(self.bookmarks_file).touch()
            self.write_bookmarks()

    def read_bookmarks(self):
        self.test_file()
        try:
            with open(self.bookmarks_file, 'r') as f:
                self.bookmarks = json.load(f)
        except json.decoder.JSONDecodeError:
            self.error('Invalid JSON loaded, happens if you just deleted your bookmarks file')

    def write_bookmarks(self):
        self.test_file()
        with open(self.bookmarks_file, 'w', encoding='utf-8') as f:
            json.dump(self.bookmarks, f, ensure_ascii=False, indent=4)

    def debug(self, message):
        if self.options['logging']:
            self.nvim.out_write("Brojectile > {} \n".format(message))

    def error(self, message):
        self.nvim.err_write("Brojectile > {} \n".format(message))

