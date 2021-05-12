# LingLibre
Learn new languages by reading anything you choose.

This was inspired by other site/projects like the opensource Lwt, the closed source lingq etc...

![lingl_German_800px](https://user-images.githubusercontent.com/6438275/116420467-47bdec80-a83e-11eb-8023-4f67974223ad.png)
![lingl_homepage_600px](https://user-images.githubusercontent.com/6438275/116420494-4d1b3700-a83e-11eb-9570-ef473cba9777.png)


## 1. How to use it:

### 1.1 Use the executable (Standalone application):

Available for Linux/Windows/Max:

the executable is `Linglibre`.

<https://github.com/gustavklopp/LingL/releases>

After launching the app, you will need to create an account (this way, the app allows multi-accounts).

### 1.2. Use the built-in server inside Django:

It will need `python >=3.8` and `Django >= 3.2`

Set a virtualenv with python 3.8, then inside the virtual env:
`pip install -r requirements.txt`

Running the Django project:

move inside the LingL folder (where `manage.py` is) and:
	
```
python manage.py migrate
python manage.py loaddata ./lwt/fixtures/initial_fixture_USER.yaml
python manage.py loaddata ./lwt/fixtures/initial_fixture_LANGUAGES.yaml
python manage.py runserver
```
then open your browser to <http://127.0.0.1:8000>

After launching the app, you will need to create an account (this way, the app allows multi-accounts).
There's also a `superuser` account for Django admin use: it's : username: `lingl` / password: `lingl`.

### 1.3. (future) Use the online website:
Maybe later if people interested.

## 2. Developers:

* Building:

To build `LingLibre`, use CX_Freeze with the suitable platform:

`python setup_LINUX.py build` on Linux

`python setup_WIN32.py build` on Windows

`python setup_MACOS.py build` on Mac

The build results (with the `LingLibre` executable) will be in the `build` folder.

* [Flowchart](https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=LingLibre_flowchart#R7V1Zc5s6FP41nqYP9ZjV%2BLFJ2rQz6TRzc%2B9t%2B%2BSRQcYkgFwhb%2Fn1lTDYgMTiBbBd96XoILbznV1HTke585YPGEwn35AF3Y7cs5Yd5b4jy1JP69P%2FGGW1puiqsibY2LGiSVvCs%2FMG4ysj6syxYJCaSBByiTNNE03k%2B9AkKRrAGC3S08bITT91CmzIEZ5N4PLUH45FJhFV0gfbE1%2BgY0%2FiR%2Buauj7jgXh29CnBBFhokSApnzrKHUaIrI%2B85R10Gfdixqyv%2B5xzdvNmGPqkygWecvv04yccTh4C%2FX8Pf71%2Fm%2Bsfos%2BYA3cWfXFH1l16v1vLmdNDmx3%2BF0DMbuQTiIFJHOTHk%2BjTEvOi7ySrmHsELhl9QjyXEiR6GBCMXuEdchEOpygjQ1O1Hj0zdlw3QR8bJjRNSgeuY%2FuUZkL2eEqYQ0wcitDH6ITnWBZ74O1i4hD4PAUme%2FqCyiOlYTTzLcg40Nu8YJJlERfZPeEyQYpY%2BACRBwle0SnLtGCu0sNFQjh6EW2SkItYCEAkj%2FbmxlvE6EEE2g4Axi%2BQQPAFzEFgYmdK9gFENw04GvOAWAAa49MHZNA6IDIHyNOKTJjO7A6GIY8UXReAoUHDUk8eDElpHQ2dQwO8gOVwNrUAgd2XgEMlWDieC3xYoAH5OnMEFvbVNA9FEr2hJXmoHIOJdzMVfl0Yb9L8GX7v%2FZ6%2F%2FB7gD6rGcQla1E1GQ4SpeNvIB%2B6nLTUjW9s5jwhNI3F%2FgYSsIp8PZgSllYGyEK9%2BRteHg19s0NXi4f0yefJ%2BFY0CAjD5yHw%2FJfgoRDKkfXbYZydEnX1ErjMtFKcAzbAJCyZGRoA%2B1oakgLWyWBYwdAFx5um3E%2BEaXko%2FFqwSE6aIuuogcecnRkhqaUZNtUzkkJkvHzRd7hsZCVy%2F71YeNx%2B%2Bv57zRjeh5kMKP5kFN%2B85MU4LqchEJgTyGOag2EhVNhIZG6ELzKwsMBF6XRZC4th%2FEpznGFoZjKqclwytGus1rSbW85IfsZ44xIWXy3lZqyj0tXFeKWFtgz6v3B0f6vFKPVmOwdrNk5W7qmyQs%2FbE0VUZQI%2FgVySDU68JdKcs7T%2FF4FHSM%2BwS6IgiiQJwra4IXJbrVJOtZvxKKYZYTarKvFExyosrUgndEM7ThNp3gLIclhNxIv2EYRA4vk2p78C7sNTDPovmp0MMgXVUF7Ip7OSXgnaEqbp66JnQVK3qQupSDo2DYuihORz6jPULhK3TjVl3Z35O1tEI94Uuq8%2FxNulHo9SxZWO1h8cWWC%2Fh52sVPXtOWHZ0Y1X0ksUF6gdEp6CMzfocHtObn3Oteq842ijUQ0UvNYKyqEZXmxryJbqOrN5YyJx59EPfdxmcq5vxzA%2BXHm7gOaU0JVD0tbRJFDmkfpOJvMIvCCWDA4sGB3dM1zAb3SdGOvAYn%2F1RMA051ntnF559OJUwowZYyxWsWT8Xr7kWG1HTdczX2I6y2EMA0NWm5uRdg3LItSYDy%2FjDasm6NoM9CvKmC6g1MTM1eako%2Fd2n2C4GsbU8bPR9ptkP373RL8VbDM1%2Fgon1KKjcCbSSYfORzkrVU%2BN5IxxPi%2Bjh1PScrIpyT1ggptDhletD7uYVtZ2x9RGMoJsWm%2BoKTB2N8wZG4f2Y4ETrGPTm2m1Hu6%2BenOQWTjaNItFTOslWDJFi97p9VU076Ri3Aytbar%2BrqKkb97rSIP1PT98UjccBrKXMJfMrfCdUpKlqB6qWY%2BS2zID4bfj4l%2BqJN0bY605XHC4FJca4KSC%2FjSCXtzssPfXTrk42BPmDyNdJRl3OTqqUJMZMZSWVSvbsoKxiHyyKxaMyQkoaINHioCi%2FU6Wu3q8pAuWr6GG0OTQJdtdHBNm2W1dNvSTiK2bnRpiLBF7EUEWtK6DnkzQxO0909S9fRA6RaZHNqW%2FBu8dx9sxqhwKnWlSdKa0SDhryoWI4%2BDWNsP%2BDJaAscz1Ju1LBrIiW6tT6hJrPSEIubswKtIYm8qZMqttcnNjHvEg7NS6K7Iuo5642KFSdY22jLXe7mZsjtdwVqnapoZIGFS2V0m%2FTVGnFnqN%2BZOULhlY91Avt2U%2BZrhDE0Upeg6RmFE0%2FuEGykIWcbY%2Fs%2BmXbc%2BHCSqMGXemL%2BW85JlnAEWsoulz2i2IbIftry5hUXvwp64OpC1bDKQoCZ%2BTCwPEcF%2BDL1gSlqibUBoXE903WmjrtuFpRwZlVdVtVvdY67m4td1I51Yi2WA5dx389xdRJydQgDbli7tSvbY1VUIMM10pjVrJFmeHMf134Z2Vb1F1sS%2BtZk8Q7WZOm%2F6wZ%2Fi%2BCQbjrrlEcZL6QwCvDgt7oonGQBVapYRx40%2F4X6oNwT3CzOIiW%2BLL64Ng%2BwvC8Qs%2BdcFCqZgH14VDNP1w8Eqqo9brZdJj%2F2QJeI1wIsO%2F49uUCobVfl%2BBXTkQqcflQ6KK9Us1GrwbH2xPeZt9pIU9utXC%2F%2BR2fa90iVVNuDQ%2B%2BxfWqLnxJojV4ist8V3jkVqt%2Bgo7PKzx87twaPNdYoASeVnclyoMrPMXwtBqqKfIVnuIWmJxdDw3Bcw0NSuBpakOC%2BOl81VjQTv%2Fl32%2BPx9sGaOkjXRP80OF4PJbb2Qa406q6qJ5W1%2B8cijHLWX4Mm1%2Fr2UVyEP%2Byu0g00QquqKO7vr4ERbQPnRP7TL%2FO6Wwk2adCpuRkiMu0VMcYGd3Ycre5l0QtrsNcrvdQKruPVoMv9ayCL7h0yKbaRo%2FXV%2FW1aLi9ig322tF8FOxFHbAFe%2BGa7oBVsz95oGtJOSqdr%2BhSRu5qaIFV1XYFs7UtPPHvP5z2Hh71rEoezZuAuIO43PzXVBqhw%2B1fK1gr5faPPiif%2FgA%3D) of the major Classes and Functions (Javascript and Python) 


