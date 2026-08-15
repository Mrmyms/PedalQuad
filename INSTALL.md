# INSTALL for PedalCuad

To build PedalCuad (forked from Carla), run the standard make commands. 
The backend C++ engine will compile based on your OS and available libraries.

```bash
$ make
```

Once compiled, you can run the PedalCuad frontend UI without installing it system-wide:
```bash
$ ./source/frontend/pedalcuad
```
*(Note: Do not use the old `carla` launcher, use `pedalcuad` instead).*

## BUILD DEPENDENCIES

There are no strict required C++ build dependencies, but the default build may not be complete without them.

Since the PedalCuad interface is entirely written in Python/Qt, **you will need PyQt5** (python3 version) to run the frontend.

You likely will also want:
 - `libmagic/file` (for auto-detection of binary types, needed for plugin-bridges)
 - `liblo` (for OSC support, essential if you plan to use a remote control app for the pedal)

Optional for Linux hardware builds (e.g. Raspberry Pi):
 - `ALSA`
 - `PulseAudio`
 - `X11` or `Wayland` depending on your display server.

## BUILD BRIDGES

PedalCuad preserves Carla's ability to make use of plugin bridges to load additional plugin types (e.g. running 32bit or Windows plugins on a Linux pedal hardware).

### Windows plugins on Linux (via Wine)

Requires a mingw compiler, and winegcc.
First, we build the Windows bridges using mingw:
```bash
make win32 CC=i686-w64-mingw32-gcc CXX=i686-w64-mingw32-g++
make win64 CC=x86_64-w64-mingw32-gcc CXX=x86_64-w64-mingw32-g++
```

To finalize, we build the wine<->native bridges using winegcc:
```bash
make wine32
make wine64
```
