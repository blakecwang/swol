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
Plugin 'fatih/vim-go'
call vundle#end()            " required
filetype plugin indent on    " required
let g:python_highlight_all = 1
let g:jedi#show_call_signatures = 0
let g:jedi#popup_on_dot = 0

" vimspector config
" Plugin 'puremourning/vimspector'
" let g:vimspector_enable_mappings = 'HUMAN'
" packadd! vimspector
" syntax enable
" filetype plugin indent on

"
"Copilot stuff
"
" What to do if:
" Copilot: Process exited with status 1
" it's because copilot can't find node version 22 - it finds version 20
" added `nvm use 22` to .bashrc to override .nvmrc version in repo root
"
let g:copilot_node_command = '/home/vagrant/.nvm/versions/node/v22.22.0/bin/node' " must match `which node`
imap <C-n> <Plug>(copilot-next)
imap <C-d> <Plug>(copilot-dismiss)
autocmd VimEnter * Copilot disable


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
set viminfo='100,<10000,s100,h

" Scrolling
set scrolloff=5
set lazyredraw

" Highlight trailing whitespace
highlight ExtraWhitespace ctermbg=black guibg=black
match ExtraWhitespace /\s\+$/

" Find main.go for easier debugging with dlv
function! StartProjectDebug()
    " 1. Start from the folder of the file currently being edited
    let l:current_file_dir = expand('%:p:h')

    " 2. Search upward to find the project root (marked by go.mod)
    let l:go_mod = findfile("go.mod", l:current_file_dir . ";")

    if empty(l:go_mod)
        echo "Could not find go.mod! Are you inside a Go project?"
        return
    endif

    " 3. Get the absolute path of that project root folder
    let l:project_root = fnamemodify(l:go_mod, ":p:h")

    " 4. Search downward from the project root to locate main.go
    " The '**' tells Vim to look recursively into all subfolders (like cmd/)
    let l:main_file = findfile("main.go", l:project_root . "/**")

    if empty(l:main_file)
        echo "Found project root at " . l:project_root . " but couldn't find a main.go inside it!"
        return
    endif

    " 5. Get the directory where main.go actually lives
    let l:main_dir = fnamemodify(l:main_file, ":p:h")

    " 6. Launch Delve inside that specific package folder
    execute "vertical terminal dlv debug " . l:main_dir
endfunction

" Map it to \d (or your leader key + d)
nnoremap <leader>d :call StartProjectDebug()<CR>
