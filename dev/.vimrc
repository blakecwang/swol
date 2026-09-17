" ============================================================================
" MODERN MINIMALIST .VIMRC FOR GO DEVELOPERS
" ============================================================================

" ----------------------------------------------------------------------------
" 1. Essential Settings
" ----------------------------------------------------------------------------
set nocompatible          " Disable compatibility with old vi
filetype plugin indent on " Enable detection, plugins, and indenting for filetypes
syntax on                 " Enable syntax highlighting
" autocmd BufNewFile,BufRead *.spec.ts set filetype=typescript  " Treat .spec.ts as .ts

set number               " Show line numbers
set mouse-=a             " Disnable mouse support in all modes
set clipboard=unnamed    " Use system clipboard
set hidden               " Allow background buffers without saving
set noshowmode           " Hide the default -- INSERT -- line (cleaner look with statuslines)

" ----------------------------------------------------------------------------
" 2. Search & Whitespace
" ----------------------------------------------------------------------------
set hlsearch             " Highlight search results
set updatetime=300       " Faster completion and diagnostic updates

" Go style guide mandates tabs over spaces
set tabstop=4            " Number of visual spaces per tab
set shiftwidth=4         " Number of spaces for auto-indent
set noexpandtab          " Keep tabs as tabs (Crucial for Go)
autocmd FileType javascript,typescript setlocal tabstop=2 shiftwidth=2 expandtab  " Set 2-space indentation specifically for JavaScript and TypeScript


" ----------------------------------------------------------------------------
" 3. Visuals & Aesthetics (Minimalist)
" ----------------------------------------------------------------------------
set termguicolors        " True color support
set cursorline           " Highlight the current line
set signcolumn=yes       " Always show sign column to prevent layout shifts

" ----------------------------------------------------------------------------
" 4. Recommended Lightweight Plugins (Using vim-plug)
" ----------------------------------------------------------------------------
" Install vim-plug if you haven't: 
" curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://githubusercontent.com

call plug#begin('~/.vim/plugged')

" Go Support (The gold standard)
Plug 'fatih/vim-go', { 'do': ':GoUpdateBinaries' }

" Git integration (blame, blame splits, etc.)
Plug 'tpope/vim-fugitive'

" The only plugin you need for JS/Node navigation
Plug 'neoclide/coc.nvim', {'branch': 'release'}

" Lighter TypeScript syntax highlighting. Vim's own bundled syntax/typescript.vim
" is yats.vim under the hood, which can catastrophically backtrack on some
" files ('redrawtime exceeded' + hangs while editing). vim-plug puts this
" plugin's syntax file earlier in 'runtimepath' than Vim's bundled one, so it
" loads first, sets b:current_syntax, and the slow bundled version skips
" itself automatically - no extra config needed.
Plug 'leafgarland/typescript-vim'

" Protobuf file detection and syntax highlighting
Plug 'google/protobuf', { 'rtp': 'editors/proto' }

call plug#end()

" ----------------------------------------------------------------------------
" 5. Plugin Configurations
" ----------------------------------------------------------------------------

" vim-go configuration (Keep it minimal and let gopls handle the heavy lifting)
let g:go_gopls_enabled = 1
let g:go_code_completion_enabled = 0          " Let vim-lsp handle completion
let g:go_fmt_command = "goimports"            " Auto-format and manage imports on save
let g:go_diagnostics_enabled = 0              " Let vim-lsp handle errors to avoid duplicates

" Highlight extra Go details for readability
let g:go_highlight_types = 1
let g:go_highlight_fields = 1
let g:go_highlight_functions = 1
let g:go_highlight_function_calls = 1
let g:go_highlight_operators = 1

" coc.nvim extensions (auto-installed/updated on startup)
" coc-pyright adds Python navigation/completion (Microsoft's Pyright LSP),
" reusing the same <C-]> / gd mappings below - no Python-specific keys needed.
let g:coc_global_extensions = ['coc-pyright']

" ----------------------------------------------------------------------------
" 6. Key Mappings & Shortcuts
" ----------------------------------------------------------------------------
let mapleader = " "      " Set Spacebar as the leader key

" Clear search highlights quickly
nnoremap <silent> <Leader>c :noh<CR>

" Coc.nvim Navigation Shortcuts
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> <C-]> <Plug>(coc-definition)

" ----------------------------------------------------------------------------
" 7. GitHub Integration
" ----------------------------------------------------------------------------
" <leader>pr : open the GitHub PR that introduced the current line in the
" browser. Works from a normal source file, and from a fugitive :Git blame
" split (cursor on any blame line resolves to that line's commit).
function! s:GhOpenUrl(url) abort
  if empty(a:url)
    echoerr 'No URL to open'
    return
  endif
  if has('mac') || has('macunix')
    call system('open ' . shellescape(a:url))
  elseif executable('xdg-open')
    call system('xdg-open ' . shellescape(a:url))
  else
    echom 'Open manually: ' . a:url
  endif
endfunction

" <leader>gb : open a git blame split for the current file (:G blame)
nnoremap <silent> <leader>gb :G blame<CR>

" Fugitive blame is opened as a plain temp file (e.g. /tmp/.../*.fugitiveblame)
" living outside the repo, so git commands run from its own directory can't
" find the remote. Its blame split always sits next to the real source
" window in the same tab, so find that window and use its directory instead.
function! s:GhSourceDir() abort
  if &filetype !=# 'fugitiveblame'
    return expand('%:p:h')
  endif
  for winnr in range(1, winnr('$'))
    if getwinvar(winnr, '&filetype') !=# 'fugitiveblame'
      let path = fnamemodify(bufname(winbufnr(winnr)), ':p')
      if filereadable(path)
        return fnamemodify(path, ':h')
      endif
    endif
  endfor
  return ''
endfunction

function! s:GhShaForCurrentLine() abort
  " Fugitive blame splits: each line starts with the commit hash
  " (boundary/root commits are prefixed with ^).
  if &filetype ==# 'fugitiveblame'
    " Same pattern fugitive itself uses internally (s:BlameCommitFileLnum).
    let sha = matchstr(getline('.'), '^\^\=[?*]*\zs\x\+')
    return sha =~# '^0\+$' ? '' : sha
  endif

  " Normal buffer: ask git for the blame info on just this line.
  let dir = shellescape(expand('%:p:h'))
  let file = shellescape(expand('%:t'))
  let ln = line('.')
  let out = system('git -C ' . dir . ' blame -L ' . ln . ',' . ln . ' --porcelain -- ' . file)
  if v:shell_error
    return ''
  endif
  let sha = matchstr(out, '^\zs[0-9a-f]\{40}')
  return sha =~# '^0\+$' ? '' : sha
endfunction

function! s:GhRepoSlug() abort
  let srcdir = s:GhSourceDir()
  if empty(srcdir)
    return ''
  endif
  let dir = shellescape(srcdir)
  let remote = system('git -C ' . dir . ' config --get remote.origin.url')
  let remote = substitute(remote, '\n$', '', '')
  return matchstr(remote, 'github\.com[:/]\zs.\{-}\ze\%(\.git\)\?$')
endfunction

function! s:GhOpenPrForLine() abort
  let sha = s:GhShaForCurrentLine()
  if empty(sha)
    echom 'GhOpenPrForLine: no commit found for this line (uncommitted?)'
    return
  endif

  let slug = s:GhRepoSlug()
  if empty(slug)
    echom 'GhOpenPrForLine: could not determine GitHub repo from remote.origin.url'
    return
  endif

  if !executable('gh')
    echom 'GhOpenPrForLine: gh CLI not found, opening commit instead'
    call s:GhOpenUrl('https://github.com/' . slug . '/commit/' . sha)
    return
  endif

  let pr_url = system('gh api repos/' . slug . '/commits/' . sha . '/pulls --jq ".[0].html_url" 2>/dev/null')
  let pr_url = substitute(pr_url, '\n$', '', '')

  if empty(pr_url) || pr_url ==# 'null'
    " No PR found for this commit (e.g. pushed directly to main) - fall
    " back to the commit view.
    call s:GhOpenUrl('https://github.com/' . slug . '/commit/' . sha)
  else
    call s:GhOpenUrl(pr_url)
  endif
endfunction

nnoremap <silent> <leader>pr :call <SID>GhOpenPrForLine()<CR>
