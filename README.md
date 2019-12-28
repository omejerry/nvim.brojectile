# Nvim.Brojectile

Nvim.Brojectile is a [Projectile](https://github.com/bbatsov/projectile)-inspired directory-bookmarks manager.

This plugin enables you to store your current working directory as a bookmark in a JSON file. 
It depends on [fzf.vim](https://github.com/junegunn/fzf.vim) to search through stored bookmarks and change the current working directory.

For now it just switches the current working directory, allowing you to find files in the project with FZF or some other tool.

## Features

* Save current working directory as bookmark.
* Fuzzysearch through [fzf.vim](https://github.com/junegunn/fzf.vim)
* Cleans non-existing directories on start-up

## Installation

## Requirements

* [fzf.vim](https://github.com/junegunn/fzf.vim)
* Neovim

## Vim-plug

```
Plug 'https://gitlab.com:jwiersma/nvim.brojectile.git', { 'do': ':UpdateRemotePlugins' }
```

## Options

The following options can be set through your .vimrc, with the defaults shown.
```
let g:Brojectile#options#logging = 1 "boolean
let g:Brojectile#options#bookmark_dir = '~/.config/nvim/nvim_brojectile' "Path/string
let g:Brojectile#options#bookmark_file = '.bookmarks.cache' "String
let g:Brojectile#options#cd_command = 'FZF' "String, vim command
```

## Commands

Nvim.Brojectile doesn't set any shortcuts by default. So you should map the commands to shortcuts manually if you wish. The following commands are available.

*Example:*
```
:nnoremap <leader>ba :BtileAdd<CR>
:nnoremap <leader>bl :BtileList<CR>
:nnoremap <leader>bc :BtileList 1<CR>
```

|Command          |Description                                                                                    |
|-----------------|-----------------------------------------------------------------------------------------------|
|:BtileAdd        |Adds the current working directory to the bookmarklist by reading PWD. Doesn't add duplicates. |
|:BtileList       |List the available bookmarks in a fuzzysearch window. Takes an optional boolean:               |
|                 |True: Execute cd_command after changing directory.                                             |
|                 |False: Just change directory on select.                                                        |
|:BtileDel        |Lists the available bookmarks in a fuzzysearch window. Delete's bookmark on selection.         |
|:BtileRM         |Removes a given path from the list. Takes a string (path) as argument. Called by :BtileDel.    |
|:BtileCD         |Changes current direcroy. Takes a string (path) as argument. Called on fuzzy selection.        |
|:BtileCDCommand  |Change directory and execute cd_command.                                                       |

## Functions

|Function                     |Description                                             | 
|-----------------------------|--------------------------------------------------------|
|Brojectile_list_bookmarks()  |Returns the current list of bookmarks as a List object. |
