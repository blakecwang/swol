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
Plugin 'leafgarland/typescript-vim'
Plugin 'peitalin/vim-jsx-typescript'
"Plugin 'klen/python-mode'
Plugin 'hashivim/vim-terraform'
Plugin 'github/copilot.vim'
call vundle#end()            " required
filetype plugin indent on    " required
let g:python_highlight_all = 1
let g:jedi#show_call_signatures = 0
let g:jedi#popup_on_dot = 0

"
"Copilot stuff
"
let g:copilot_node_command = '/home/vagrant/.nvm/versions/node/v22.22.0/bin/node' " must match `which node`
let g:copilot_filetypes = {
\ '*': v:false,
\ 'python': v:true,
\ 'sql': v:true,
\ }
" Navigation
imap <C-n> <Plug>(copilot-next)
imap <C-d> <Plug>(copilot-dismiss)

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
let &colorcolumn=join(range(101,999),",")
highlight ColorColumn ctermbg=yellow guibg=yellow

" Disable mouse in all modes
set mouse-=a

" Yank more lines
set viminfo='100,<1000,s100,h

" Scrolling
set scrolloff=5
set lazyredraw

" Highlight trailing whitespace
highlight ExtraWhitespace ctermbg=black guibg=black
match ExtraWhitespace /\s\+$/

