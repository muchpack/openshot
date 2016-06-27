Name:           openshot
Version:        2.0.7
Release:        5%{?dist}
Summary:        Create and edit videos and movies

Group:          Applications/Multimedia
License:        GPLv3+
URL:            http://www.openshotvideo.com/

Source0:        http://launchpad.net/openshot/2.0/%{version}/+download/openshot-qt-%{version}.tar.gz

BuildArch: noarch

BuildRequires:  python3-devel
BuildRequires:  python3-qt5-devel
BuildRequires:  libopenshot
BuildRequires:  libopenshot-audio
BuildRequires:  desktop-file-utils
# To fix icon
BuildRequires:  ImageMagick

Requires:       mlt
Requires:       mlt-python
Requires:       ladspa
Requires:       notify-python
Requires:       pygoocanvas
Requires:       pygtk2-libglade
Requires:       python3-pillow
Requires:       python3-httplib2
Requires:       pyxdg
Requires:       SDL
Requires:       sox
Requires:       librsvg2
Requires:       frei0r-plugins
Requires:       fontconfig
Requires:       python3-libopenshot >= 0.1.0
Requires:       libopenshot-audio >= 0.1.0
Requires:       qt5-qtsvg
Requires:       qt5-qtwebkit
Requires:       python3-qt5
Requires:       python3-zmq
# Needed because it owns icon directories
Requires:       hicolor-icon-theme
Requires:       python3-qt5-webkit
Recommends:     ffmpeg
Recommends:     blender
Recommends:     vid.stab


%description
OpenShot Video Editor is a free, open-source, non-linear video editor. It
can create and edit videos and movies using many popular video, audio,
image formats.  Create videos for YouTube, Flickr, Vimeo, Metacafe, iPod,
Xbox, and many more common formats!

Features include:
* Multiple tracks (layers)
* Compositing, image overlays, and watermarks
* Support for image sequences (rotoscoping)
* Key-frame animation
* Video and audio effects (chroma-key)
* Transitions (lumas and masks)
* 3D animation (titles and simulations)
* Upload videos (YouTube and Vimeo supported)


%prep
%setup -qc


%build
%{__python3} setup.py build


%install
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}

# We strip bad shebangs (/usr/bin/env) instead of fixing them
# since these files are not executable anyways
find %{buildroot}/%{python3_sitelib} -name '*.py' \
  -exec grep -q '^#!' '{}' \; -print | while read F
do
  awk '/^#!/ {if (FNR == 1) next;} {print}' $F >chopped
  touch -r $F chopped
  mv chopped $F
done

# Validate desktop file
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}-qt.desktop

# Move icon files to the preferred location
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/ \
         %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/
mv %{buildroot}%{_datadir}/pixmaps/%{name}-qt.svg \
   %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

# Provided icon is not square
convert xdg/openshot-qt.png -virtual-pixel Transparent -set option:distort:viewport "%[fx:max(w,h)]x%[fx:max(w,h)]-%[fx:max((h-w)/2,0)]-%[fx:max((w-h)/2,0)]" -filter point -distort SRT 0 +repage %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/openshot-qt.png

%find_lang OpenShot


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f OpenShot.lang
%license COPYING
%doc AUTHORS README
%{_bindir}/*
%{_datadir}/applications/%{name}-qt.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/*
%{python3_sitelib}/%{name}_qt/
%exclude %{python3_sitelib}/%{name}_qt/locale/
%{python3_sitelib}/*egg-info
%{_prefix}/lib/mime/packages/openshot-qt


%changelog
* Sun Jun 26 2016 The UnitedRPMs Project (Key for UnitedRPMs infrastructure) <unitedrpms@protonmail.com> - 2.0.7-5
- Rebuild with new ffmpeg

* Thu Jun  9 2016 Pavlo Rudyi <paulcarroty at riseup.net> - 2.0.7-4
- Added the depends python3-qt5-webkit.

* Fri May 27 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 2.0.7-3
- Added missing dependencies
- Sanitize tabs.

* Mon Apr 18 2016 Richard Shaw <hobbes1069@gmail.com> - 2.0.7-2
- Update to require python3-libopenshot.

* Fri Apr  8 2016 Richard Shaw <hobbes1069@gmail.com> - 2.0.7-1
- Update to latest upstream release.

* Fri Mar  4 2016 Richard Shaw <hobbes1069@gmail.com> - 2.0.6-1
- Update to latest upstream release.

* Mon Jan 11 2016 Richard Shaw <hobbes1069@gmail.com> - 2.0.4-1
- Update to latest upstream release.

* Mon Apr  6 2015 Richard Shaw <hobbes1069@gmail.com> - 1.4.3-3
- Fix broken icon file (BZ#3546).
- Add ladspa as a install requirement (BZ#3472).

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Oct 26 2012 Richard Shaw <hobbes1069@gmail.com> - 1.4.3-1
- Update to latest upstream release.

* Mon Feb 20 2012 Richard Shaw <hobbes1069@gmail.com> - 1.4.2-4
- Fix small packaging bug with icon.

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 06 2012 Richard Shaw <hobbes1069@gmail.com> - 1.4.2-2
- Update to latest release.
- Fixed small build problem with the buildroot path finding it's way into
  a packaged file.

* Mon Feb 06 2012 Richard Shaw <hobbes1069@gmail.com> - 1.4.2-1
- Update to latest release.

* Mon Jan 30 2012 Richard Shaw <hobbes1069@gmail.com> - 1.4.1-1
- Update to latest release.
