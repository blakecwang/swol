set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line

Plugin 'VundleVim/Vundle.vim'
Plugin 'tpope/vim-fugitive'
Plugin 'Vimjas/vim-python-pep8-indent'
Plugin 'vim-python/python-syntax'
Plugin 'nvie/vim-flake8'
Plugin 'davidhalter/jedi-vim'
"Plugin 'klen/python-mode'
call vundle#end()            " required
filetype plugin indent on    " required

" Enable syntax highlighting
syntax on

" Tab Handling
set tabstop=4       " Number of spaces tabs count for
set softtabstop=4   " Number of spaces to use when editing
set shiftwidth=4    " Number of spaces used for autoindent
set expandtab       " Use spaces instead of tabs
set autoindent

" Show line numbers
set number

" Highlight the current line
set cursorline

" Highlight columns after the 100th column
let &colorcolumn=join(range(81,999),",")

" Highlight trailing whitespace
match Error /\s\+$/
