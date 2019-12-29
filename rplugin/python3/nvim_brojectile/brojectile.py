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
        }
        self.get_opts()
        self.bookmarks      = {'bookmarks': []}
        self.bookmarks_file = "{}/{}".format(self.options['bookmark_dir'],
                                             self.options['bookmark_file'])
        self.clean_bookmarks()

    def get_opts(self):
        for opt in self.options.keys():
            try:
                self.options[opt] = self.nvim.eval("Brojectile#options#{}".format(opt))
            except Exception:
                None

    def fzf_call(self, sink):
        fzf_wrap = self.nvim.eval("fzf#wrap({{'source': Brojectile_list_bookmarks(), 'sink': '{}'}})".format(sink))
        self.nvim.call("fzf#run", fzf_wrap)

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

    def delete_bookmark(self, bookmark):
        self.read_bookmarks()
        while bookmark in self.bookmarks['bookmarks']:
            self.bookmarks['bookmarks'].remove(bookmark)
        self.write_bookmarks()

    def read_bookmarks(self):
        self.test_file()
        try:
            with open(self.bookmarks_file, 'r') as f:
                self.bookmarks = json.load(f)
        except json.decoder.JSONDecodeError:
            self.error('Corrupt bookmarks file, initializing new one and writing from memory on next write.')

    def write_bookmarks(self):
        self.test_file()
        with open(self.bookmarks_file, 'w', encoding='utf-8') as f:
            json.dump(self.bookmarks, f, ensure_ascii=False, indent=4)

    def debug(self, message):
        if self.options['logging']:
            self.nvim.out_write("Brojectile > {} \n".format(message))

    def error(self, message):
        self.nvim.err_write("Brojectile > {} \n".format(message))

