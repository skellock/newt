Summary: A development library for text mode user interfaces.
Name: newt
%define version 0.50.28
Version: %{version}
Release: 1
Copyright: LGPL
Group: System Environment/Libraries
Source: ftp://ftp.redhat.com/pub/redhat/code/newt/newt-%{version}.tar.gz
BuildRequires: python,python-devel,perl
Requires: slang
Provides: snack
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%package devel
Summary: Newt windowing toolkit development files.
Requires: slang-devel %{name} = %{version}
Group: Development/Libraries

%package python2
Summary: Snack for python2
Requires: python2
Group: System Environment/Libraries

%Description
Newt is a programming library for color text mode, widget based user
interfaces.  Newt can be used to add stacked windows, entry widgets,
checkboxes, radio buttons, labels, plain text fields, scrollbars,
etc., to text mode user interfaces.  This package also contains the
shared library needed by programs built with newt, as well as a
/usr/bin/dialog replacement called whiptail.  Newt is based on the
slang library.

%description devel
The newt-devel package contains the header files and libraries
necessary for developing applications which use newt.  Newt is a
development library for text mode user interfaces.  Newt is based on
the slang library.

Install newt-devel if you want to develop applications which will use
newt.

%description python2
The newt-python2 package contains a snack module for python2.

%prep
%setup

%build
# gpm support seems to smash the stack w/ we use help in anaconda??
#./configure --with-gpm-support
./configure 
make
make shared
chmod 0644 peanuts.py popcorn.py

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make instroot=$RPM_BUILD_ROOT install
make instroot=$RPM_BUILD_ROOT install-sh

python -c 'from compileall import *; compile_dir("'$RPM_BUILD_ROOT'/usr/lib/python1.5",10,"/usr/lib/python1.5")'

%if 0
# cheat... build python2 stuff here
make clean
perl -pi -e "s/python1.5/python2.0/g" *
./configure
make instroot=$RPM_BUILD_ROOT install
make instroot=$RPM_BUILD_ROOT install-sh
python -c 'from compileall import *; compile_dir("'$RPM_BUILD_ROOT'/usr/lib/python2.0",10,"/usr/lib/python2.0")'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel -p /sbin/ldconfig

%postun devel -p /sbin/ldconfig


%files
%defattr (-,root,root)
%doc CHANGES COPYING
/usr/lib/libnewt.so.*
/usr/bin/whiptail
/usr/lib/python1.5/snack.py*
/usr/lib/python1.5/lib-dynload/_snackmodule.so

%files devel
%defattr (-,root,root)
%doc tutorial.sgml peanuts.py popcorn.py
/usr/include/newt.h
/usr/lib/libnewt.a
/usr/lib/libnewt.so

%if 0
%files python2
%defattr (-,root,root)
/usr/lib/python2.0
%endif

%changelog
* Thu Jul 05 2001 Crutcher Dunnavant <crutcher@redhat.com>
- added 'hide_checkbox' and 'unselectable' options to CheckboxTrees

* Mon Jun 25 2001 Jeremy Katz <katzj@redhat.com>
- ClistBox -> Clistbox for API consistency
- fixup replace() method of Clistbox

* Fri Jun 8 2001 Jeremy Katz <katzj@redhat.com>
- few bugfixes to the CListBox

* Fri Jun 8 2001 Jeremy Katz <katzj@redhat.com>
- added python binding for newtListboxClear() for Listbox and CListBox
- let ButtonBars optionally be made of CompactButtons

* Wed Jun  6 2001 Crutcher Dunnavant <crutcher@redhat.com>
- added CListBox python convenience class

* Tue May 15 2001 Michael Fulbright <msf@redhat.com>
- added python binding for CompactButton()

* Tue Apr  3 2001 Matt Wilson <msw@redhat.com>
- change from using SLsmg_touch_screen to SLsmg_touch_lines to prevent
  excessive flashing due to screen clears when using touch_screen (more
  Japanese handling)

* Mon Apr  2 2001 Matt Wilson <msw@redhat.com>
- redraw the screen in certain situations when LANG=ja_JP.eucJP to
  prevent corrupting kanji characters (#34362)

* Mon Apr  2 2001 Elloit Lee <sopwith@redhat.com>
- Allow python scripts to watch file handles
- Fix 64-bit warnings in snackmodule
- Misc snack.py cleanups
- Add NEWT_FD_EXCEPT to allow watching for fd exceptions
- In newtExitStruct, return the first file descriptor that an event occurred on 

* Fri Mar 30 2001 Matt Wilson <msw@redhat.com>
- don't blow the stack if we push a help line that is longer than the
  curret number of columns
- clip window to screen bounds so that if we get a window that is
  larger than the screen we can still redraw the windows behind it
  when we pop

* Sun Feb 11 2001 Than Ngo <than@redhat.com>
- disable building new-python2 sub package again

* Thu Feb 01 2001 Erik Troan <ewt@redhat.com>
- gave up on separate CHANGES file
- added newtCheckboxTreeSetCurrent() and snack binding
- don't require python2 anymore

* Mon Jan 22 2001 Than Ngo <than@redhat.com>
- don't build newt-python2 sub package.

* Fri Dec 15 2000 Trond Eivind Glomsr�d <teg@redhat.com>
- use %%{_tmppath}
- add python2 subpackage, with such support
- fix use of append in snack.py

* Fri Sep 08 2000 Trond Eivind Glomsr�d <teg@redhat.com>
- bytecompile the snack python module
- move the libnewt.so symlink to the devel package
- include popcorn.py and peanuts.py in the devel package,
  so we have some documentation of the snack module

* Tue Aug 22 2000 Erik Troan <ewt@redhat.com>
- fixed cursor disappearing in suspend (again)

* Sat Aug 19 2000 Preston Brown <pbrown@redhat.com>
- explicit requirement of devel subpackage on same version of main package
  so that .so file link doesn't break

* Wed Aug 16 2000 Erik Troan <ewt@redhat.com>
- fixed cursor disappearing in suspend
- moved libnewt.so to main package from -devel

* Thu Aug  3 2000 Matt Wilson <msw@redhat.com>
- added setValue method for checkboxes in snack

* Wed Jul 05 2000 Michael Fulbright <msf@redhat.com>
- added NEWT_FLAG_PASSWORD for entering passwords and having asterix echo'd

* Fri Jun 16 2000 Matt Wilson <msw@redhat.com>
- build for new release

* Fri Apr 28 2000 Jakub Jelinek <jakub@redhat.com>
- see CHANGES

* Mon Mar 13 2000 Matt Wilson <msw@redhat.com>
- revert mblen patch, go back to our own wide char detection

* Fri Feb 25 2000 Bill Nottingham <notting@redhat.com>
- fix doReflow to handle mblen returning 0

* Wed Feb 23 2000 Preston Brown <pbrown@redhat.com>
- fix critical bug in fkey 1-4 recognition on xterms

* Wed Feb  9 2000 Matt Wilson <msw@redhat.com>
- fixed snack widget setcallback function

* Thu Feb 03 2000 Erik Troan <ewt@redhat.com>
- strip shared libs

* Mon Jan 31 2000 Matt Wilson <msw@redhat.com>
- added patch from Toru Hoshina <t@kondara.org> to improve multibyte
  character wrapping

* Thu Jan 20 2000 Erik Troan <ewt@redhat.com>
- see CHANGES

* Thu Jan 20 2000 Preston Brown <pbrown@redhat.com>
- fix segfault in newtRadioGetCurrent

* Mon Jan 17 2000 Erik Troan <ewt@redhat.com>
- added numerous bug fixes (see CHANGES)

* Mon Dec 20 1999 Matt Wilson <msw@redhat.com>
- rebuild with fix for listbox from Nalin

* Wed Oct 20 1999 Matt Wilson <msw@redhat.com>
- added patch to correctly wrap euc kanji

* Wed Sep 01 1999 Erik Troan <ewt@redhat.com>
- added suspend/resume to snack

* Tue Aug 31 1999 Matt Wilson <msw@redhat.com>
- enable gpm support

* Fri Aug 27 1999 Matt Wilson <msw@redhat.com>
- added hotkey assignment for gridforms, changed listbox.setcurrent to
  take the item key

* Wed Aug 25 1999 Matt Wilson <msw@redhat.com>
- fixed snack callback function refcounts, as well as optional data args
- fixed suspend callback ref counts

* Mon Aug 23 1999 Matt Wilson <msw@redhat.com>
- added buttons argument to entrywindow

* Thu Aug 12 1999 Bill Nottingham <notting@redhat.com>
- multi-state checkboxtrees. Woohoo.

* Mon Aug  9 1999 Matt Wilson <msw@redhat.com>
- added snack wrappings for checkbox flag setting

* Thu Aug  5 1999 Matt Wilson <msw@redhat.com>
- added snack bindings for setting current listbox selection
- added argument to set default selection in snack ListboxChoiceWindow

* Mon Aug  2 1999 Matt Wilson <msw@redhat.com>
- added checkboxtree
- improved snack binding

* Fri Apr  9 1999 Matt Wilson <msw@redhat.com>
- fixed a glibc related bug in reflow that was truncating all text to 1000
chars

* Fri Apr 09 1999 Matt Wilson <msw@redhat.com>
- fixed bug that made newt apps crash when you hit <insert> followed by lots
of keys

* Mon Mar 15 1999 Matt Wilson <msw@redhat.com>
- fix from Jakub Jelinek for listbox keypresses

* Fri Feb 27 1999 Matt Wilson <msw@redhat.com>
- fixed support for navigating listboxes with alphabetical keypresses

* Thu Feb 25 1999 Matt Wilson <msw@redhat.com>
- updated descriptions
- added support for navigating listboxes with alphabetical keypresses

* Mon Feb  8 1999 Matt Wilson <msw@redhat.com>
- made grid wrapped windows at least the size of their title bars

* Fri Feb  5 1999 Matt Wilson <msw@redhat.com>
- Function to set checkbox flags.  This will go away later when I have
  a generic flag setting function and signals to comps to go insensitive.

* Tue Jan 19 1999 Matt Wilson <msw@redhat.com>
- Stopped using libgpm, internalized all gpm calls.  Still need some cleanups.

* Thu Jan  7 1999 Matt Wilson <msw@redhat.com>
- Added GPM mouse support
- Moved to autoconf to allow compiling without GPM support
- Changed revision to 0.40

* Wed Oct 21 1998 Bill Nottingham <notting@redhat.com>
- built against slang-1.2.2

* Wed Aug 19 1998 Bill Nottingham <notting@redhat.com>
- bugfixes for text reflow
- added docs

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- devel package moved to Development/Libraries

* Thu Apr 30 1998 Erik Troan <ewt@redhat.com>
- removed whiptcl.so -- it should be in a separate package

* Mon Feb 16 1998 Erik Troan <ewt@redhat.com>
- added newtWinMenu()
- many bug fixes in grid code

* Wed Jan 21 1998 Erik Troan <ewt@redhat.com>
- removed newtWinTernary()
- made newtWinChoice() return codes consistent with newtWinTernary()

* Fri Jan 16 1998 Erik Troan <ewt@redhat.com>
- added changes from Bruce Perens
    - small cleanups
    - lets whiptail automatically resize windows
- the order of placing a grid and adding components to a form no longer
  matters
- added newtGridAddComponentsToForm()

* Wed Oct 08 1997 Erik Troan <ewt@redhat.com>
- added newtWinTernary()

* Tue Oct 07 1997 Erik Troan <ewt@redhat.com>
- made Make/spec files use a buildroot
- added grid support (for newt 0.11 actually)

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- Added patched from Clarence Smith for setting the size of a listbox
- Version 0.9

* Tue May 28 1997 Elliot Lee <sopwith@redhat.com> 0.8-2
- Touchups on Makefile
- Cleaned up NEWT_FLAGS_*

* Tue Mar 18 1997 Erik Troan <ewt@redhat.com>
- Cleaned up listbox
- Added whiptail
- Added newtButtonCompact button type and associated colors
- Added newtTextboxGetNumLines() and newtTextboxSetHeight()

* Tue Feb 25 1997 Erik Troan <ewt@redhat.com>
- Added changes from sopwith for C++ cleanliness and some listbox fixes.
