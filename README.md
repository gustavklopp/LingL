# LingLibre
Learn new languages by reading anything you choose.

This was inspired by other site/projects like the opensource Lwt, the closed source lingq etc...

![Screencast_small_clip](https://user-images.githubusercontent.com/6438275/121800774-05a50a80-cc34-11eb-825a-37145f2e4461.gif)
![lingl_homepage_600px](https://user-images.githubusercontent.com/6438275/116420494-4d1b3700-a83e-11eb-9570-ef473cba9777.png)

**:star: If you find this project interesting, please take a moment to `Star` it (top-right star on Github). :star:**

## 1. How to use it:

- [video channel about using LingLibre](https://tube.tchncs.de/video-channels/linglibre/videos)

## 2. How to install it:

### 2.1. Use the Docker file:

You need [Docker](https://www.docker.com/) installed.

After launching the `Docker` daemon, run:

`docker run -it -p 8000:8000 gustavklopp/lingl`

then visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

**:star: If you find this project interesting, please take a moment to `Star` it on the [Docker repo](https://hub.docker.com/r/gustavklopp/lingl). :star:**

### 2.2. Use the built-in server inside Django:

It will need `python==3.9.0`.

(Use a virtual env preferably: on Windows, use `chocolatey` to install `pyenv` for example, and on macOS, use `homebrew` to install `pyenv`.)

Set a virtualenv with python 3.9.0, then inside the virtual env:

`pip install -r requirements.txt` (it will install all the modules required, along `Django==3.2.4`)

(You need `pip` of course, which is a Python modules manager:
https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```
)

Running the Django project:

move inside the LingL folder (where `manage.py` is) and:
	
```
python manage.py migrate
python manage.py loaddata initial_fixture_USER.yaml
python manage.py loaddata initial_fixture_LANGUAGES.yaml
python manage.py runserver
```
then open your browser to <http://127.0.0.1:8000>

After launching the app, you will need to create an account (this way, the app allows multi-accounts).
There's also a `superuser` account for Django admin use: it's : username: `lingl` / password: `lingl`.

### 2.3 Use the executable (Standalone application):

The standalone is only provided for Linux. For other platforms, you can build it yourself.

the executable is `Linglibre`.

<https://github.com/gustavklopp/LingL/releases>

After launching the app, you will need to create an account (this way, the app allows multi-accounts).

### 2.4. (future) Use the online website:
Maybe later if people interested.

## 3. Upgrading:

Future versions are regularly provided. 

### 3.1 for the Python server version:
   
   1. *(optional)* same backup step 1 as the 'standalone version'.

   2. Delete the database in 'lwt' folder named "LingL_database.sqlite3".

   3. `git pull` or download the source code. The database needs to be recreated with the same steps you've done at first (`./manage.py migrate` and loading the fixtures).
   
   4. launch the server (`./manage.py runserver`)

   5. *(optional)* same restore step 5 as the 'standalone version'.

### 3.2 for the standalone version:


   1. *(optional)* First, backup (if you want to keep your previous data that you've created): in the menu, choose 'Backup/Restore/Delete your account' then click on 'Backup' (you can choose to backup everything or choose which words to backup). 

   2. *(optional)* Delete the old version folder. `LingLibre` doesn't install anything on your system in fact.

   3. Download the latest versions (see the [Releases](https://github.com/gustavklopp/LingL/releases) section) which fits your systems.

   4. Launch this new version (after uncompressing it wherever you want) by clicking on the executable `LingLibre`.

   5. *(optional)* Restore the backup created in step '1': Create an account (whatever name you want, you're not forced to use the same than in the old version). and in the 'Backup/Restore/Delete your account', click on 'Restore' and choose the backup file that you've got in the step '1'.

## 4. Missing a feature? Request it!

This is a hobby project made only by volunteers in their free time. All features of this software are implemented because they 
suit the needs of these volunteers at some point.
 
If you need a special feature and don't want to wait that somebody feels the need to code it, you can still try to fund it! It's easy: 

Create your Feature request on the [Issues page](https://github.com/gustavklopp/LingL/issues). Then go to [Issuehunt](https://issuehunt.io/r/gustavklopp/LingL/issues) and make a pledge for this feature (Consider a reasonable amount).


## 5. Developers:

Discovering a new code is always a challenge but I've done my best to welcome newcomers:
- the code is HIGHLY documented (as much as code as comments in some place)
- I use the less Python shenanigans: No functools, list comprehensions only with moderations etc.
- Diagrams are the best! I've created a flowchart with [Draw.io](https://github.com/jgraph/drawio) to follow how the code works (see below). 


* 5.1 Building:

To build `LingLibre`, use CX_Freeze with the suitable platform:

`python setup_LINUX.py build` on Linux

`python setup_WIN32.py build` on Windows

`python setup_MACOS.py build` on Mac

The build results (with the `LingLibre` executable) will be in the `build` folder.

* 5.2 [Flowchart](https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=AAA_LingLibre.drawio#R7V1Zd5vIEv41Ps48mCN2eExsj2dunGXiTJZ50UECSSRIKIAsO7%2F%2BNojG0F1AS6KhozhnJpEQIFRfVXXtfaZeLh9uIme9eBO6XnCmjNyHM%2FXqTEF%2FTB39kx55zI9o8mh3ZB757u6Y%2FHTgzv%2Fp5QfxaRvf9eLKiUkYBom%2Frh6chquVN00qx5woCrfV02ZhUP3WtTP3qAN3Uyegj3723WSRH5UN%2B%2BmDvzx%2FvsBfbeja7pOlg8%2FOf0q8cNxwWzqkXp%2Bpl1EYJrtXy4dLL0jJhwmzu%2B7Pmk%2BLJ4u8VcJywVJ99f7zF2%2B8uImNT8vo76uf98aFbOxuc%2B8Em%2FwnO9%2Bch%2FFm7TqJJ32L82dPHjFF4q2%2FDJwVevdq5gfBZRiEUfaJ6jqeNZui43EShd%2B90ifG1PImM%2FQJ%2Fcz5z7j3osR7KB3Kf8ONFy69JHpEp%2BSfmnpOz4Kl8vfbJ3x0Oz%2B2KEGj4xOdnCfmxb2fqIZe5ISDiXi50by%2Ft9ZP%2Bf7Oezf6cf%2Fthx1daDpFpSjcrFwvvWiEfnYYJYtwHq6c4DYM1%2BigjA5%2B85LkMed4Z5OE6NAiWQb5p4hA0eOX%2FPrszdf0jaTjt1cP5Q%2BvHvN3ceJEycuU89GBVZjhlB37009%2FVHYOjUIjb8ThJpp6DScquWA60dxLGuiUn%2Be5FZmjkY68wEn8%2B6oIHoNa01PDnD9GNEs28Ys%2FWpDdLvzEu1s7GX22SAlWUexCQprllllutKrYGLTUyAogNQYvoZEp8p8q5WWC9LKqSDob9XWdE%2FVp5s%2Bpn%2FhJ4J0w8ZURI%2BNzI70qzmLhPfjJl92ZVv42vVCWRpqSv3%2B6Mn1TvvC9F%2FmIIl408Koid72q5Je%2BD330Q54YaURIsUJoxt0Pyq8ieKR4DCa2ufr%2B8HWhzL%2Fc%2B%2F976Xx6bf75ea5cKDbFN%2BlPvsvfPnHN9dPRV9NNdJ8xVsol3bGZvB%2BbHcEZMCmENzjAx1ZHzwjuiyAf4Ub2sfNYOmGdCm1cL%2FsKIfvqiHC1iPNV%2BbjzZWNEcNvuiTtVKKosDjvuuW71wY7wiapYGkURFkJTXAw1sTCk7UFRMBQXQl0sCLVnCPeG0BALQjqE9wxhG4SmWBAazxDuDaE1FIQ3szfL%2B%2Fc3%2F7z9or9%2Bvbnbrt%2BYf2N%2F7RlBEEGQZJ07SEfJIH5sOq6I%2FnLG4Wy8DcfTEP3lrNxx7C9PKc5rWhLOd2K%2FD8hNKVoR%2Fe06zt7osgCh3shZxSlXhKsTQkE1SN%2BbhmDEKd7b6G%2FQAETh0ln5P08dARkIufcMgV4HgR9Pw%2BU6JfQ2jNxTBsEcHAS61ABn%2FBbhdvyb4ACVK%2FSMg1mHwzQ80SXBJJYEa3AMrHoMTnVVIEDQ9B5BaDKdIQxSJYR%2BV3LC9C9yDn3QH%2F4NtBB89x4noRO5aEWIkukm6bwALSuFyr0%2FZBl3UpF2QZIWoKxsWQBpFTKH3F1xE%2B1KC588zNmhtTAA14GWXGPwvM6DxHDyzibLe3QC1N2DdlEY0ESOkhS9j7w49ldzdPTcOU%2BvX6X0QvpsHHmO26lKm1lTbwrK3MTSUx2%2FN%2F571PaMqLwsLXhgbQ8vsaP9jPEyvPfGq5T2Ylu2%2B1OfKmvrkfpgsYBJ0bYcPsyLYTsMET5pvq8Vxde5GgR%2FrU6rQfC8wRItTU9dkpAzxQjQ879y%2FXv0cp6%2BvAnRKSGhtP7MXqOb5%2BejI6VLKOjTs6vA1WuoOp3mBP58hY5NEWRpndurVDr8qRO8zD9Y%2Bq6bRaEhsa1yGjc5tCjrg9Ww4yWHtKN%2Fpmgv3HC6WaIf%2F4eU4vn4YrZZTTMfxzsdnWga1QCwDJVZmwAW3MqsVbvRPHCReXCZCluUvrsqvTOcZUrn1SReZxQbnc8bP705YUOjMCyw7zr0SqfRQX1AjU4Df%2Foda9LU%2BgAQetaqNe0SFoN1I%2FeJuU4b%2BgDmmXDT8gmCe62cWcaZDd0mZRmme9CXPjNXu%2Bkst%2BsTaMXmtkroHMIFLJ1oJVtaVY2yNX0xkka62mJSZ%2B8O7UNgtrNFizcoumQbVeXEL%2BQAk4ROaXajikbAbcg7PKsmvjGVNs0E9dZ2oZg%2B%2FfPp9pv%2B7s3Hl68%2B%2F%2BeYH4378SUQ3AJglSQpWXipYTNNInTLquHjrEL0aVSYQM94l%2FE21AHtHDA3JtcENFMnQ85dkHMFv1DxC63iyejnJ%2BN8yIbVbi2YQElRFwh99t%2Fbf81My1Hm7vLDh2n05u71Be1S1jkfOOTZlcwVHnydz%2F9LyJyuEDJnM9p%2FXaSLYH%2BSrmDvMk6qDBooxc5y2YBr4mtR5hPQ%2FVldYqIiI24PUCrW%2FDRw4tifEgZ9JrELZ51%2B9SzwHvKzS13GOz7AXcZnjR3GbKa9TPMAazMxzFR8jPj6hsMjTPPJu40%2Bv3m3nHxVl9vx9EO8cG%2BBxn7Iu0fc8hKdVZm4gM%2BbRPi0%2FHh2avWcVkt7G6a2dXbl7iV1c8ZFIQXi1pl4QZWR2fU8Mh38n84ku1%2FKQznp0c31V2f6Fbu%2BqS0MKKYP5d9yVp7vA%2Bn%2FkWRqWjVQjHE70jfUTAk3Iz3i75Lt6h%2BjetNwNos9LolphetYnGOTb6yag9X7V8RaPOgcDJKT5SyMltL6kcKloaZG9yxXg2wxS5mohtFE2z28ECKXbAElNEUxfdkiKqqYug%2BJNc9b6Cqb3OG8Jox5O0uzpo71wdqD4Lxic8c6hwS%2FJpsVLSONNLNF04CGi9Ao4%2BCNIKpLZioRwNqM2bs8KqV8iBJs1svMqtGuGgpAGT%2Fo%2FJvc9CJdtQnAE3tONF2M1yHyE5BVFPtLP3CivcIBvypg5MApqAEJSharvBDD8n0IYpdEV8ZJI0eEQhVTlgyDtpzLQKpQlMaS8FCHzrGkhS%2BLs43TwPfuVRLO54GQkzsVcnKnBc3BA0kqc1NndCwTJqgIhZuNHHEol9smNIxQ55TkgYc8NQ%2FGEq9wE%2FAdmwrhWi2wwQKPMBx0AiabjFpkT0VULhdkewvQXqSOoCwJNw9SpmNxGR0L1eK5wnU9NjMEu46pGq1QFSSvNDKcAqBngwymTg7zBRuBaVVEss2oidTBZrrAzga9MgyXlxIaOE2wNYS2q3a6L9d7J6bv6lrABlN4Kt3kndHf9afJ1puk2xacEPmJ5QaskIDIz29HAJr9EenjdeA81sVEThMKFRq3zQsKsJxIpyXB%2F74Kt04QnBDZdYLsYN8JpxohkOwtsXp4lleHLcrSaFRd3CVb0VoWeFyogCsTvpaMhNpChcr8McaqBWaboJGj24cnd24TwFnnYg5tYe4TIwO6G40O%2F87mEaqdxw%2BO7n9ntf5YjT%2FsaYpi%2FNHl4fmmTePAX30XMXygEjWWNji5DVi3LG42BJAHyyIwmJRpRc54s%2Fq%2BFWJKTDMjHFp%2BPnjgQKath2nkZdPzfiMYwKLwXnFQ6FgaLQxbdKOTxqHIGw6HA63af0N5UKCC7X5xgOq7SHnw56sw8gT2Lo%2FFARrk1jMObOvDySMBTXPrOeJFVznQEhF4TrTyV%2FPTBUJnjX3xA4JOH0IicfpQGNAcuH6tV4uibZ9BmMIVFsZPFiu7VewMPEzcQhEAELGyVkDL1e8tL4PtswPDc8hWSScMD3aKRYHnkD10ThmewTYagx%2Fn2RgAXWhR4GnuN%2Fr94BHLVjtoq8UThge726LA82wagE64KPDU5LKyamIB%2B1EviggvDquwZqL4zf9T6ZAv0MZDFHiJ2a%2FTzCOHdjLomiTTLTrgIBVNlgzzeJzgyheFBadyDdLvBJLMOuuwI4jg8rzmwAv31UJSRkp5xUiHHRpKy6LxNEZFKxcoydIo28iiYZQKekPWJB1StcS6RqnMi1TnJh5cn0Ru306NS%2BRcn6TRtuNgpkdR4yaN5Gqdm2o1s9GRE4C64y%2BoJr6nYT7HNTPQuUI8iGflbdHf7z5kD%2Bsn9LSc9nk61CZq9CkfPt6Ceq%2F3%2BTqNUtLFfB1DwwYwzhTv3h1d6GhLtlq5sSIpPAbqwBSiIziDFTUeoQ2OWFlYK19VsWI7es8FqsSa0JroYRrVXJgfRtX6kPe3Ppg4oGnG8q%2BWWNI59B%2FuB9oek%2FeCSXZLrPEHiXPgCdPC1LibRECgsCl7Grlt0IV3t9c312%2BvKMYqxU5q6b9HJEQna64A%2Fw2cgkESqLt5JkyBkG%2FOvRNPI3%2BdMDrY4o%2BfbWaMg4t7oRatXqfPqkzj5P%2F6%2BOa2OyhdY2LoBg3lbDZTepjefSyUDdOgQOh4Deui%2BxwB5P6Ns%2FHrfkpIJ9vz6WSmsPMRSdYYWRcSufmsLv67uBpfhMvFDyMZP2z%2Be8RDL3uOjx1irNQ18xf2MLNp0ghlq2HKGpMYzC6FIyR0rPr9IwJudYgoFrHkuujzryiKYOtLr6sjmE8gbT4o6LZya%2Fxz%2BnAJ1j0J28rIJbpBQ6XwsSPNcxI1iy3CS9%2Bn7Ua8zXx6Y7eX35yHjEA%2FNl6cgIpZjABewagdBPAwj3c7HrvoFMa3xfqPf%2BzOoIO%2FqUoVMfkt6%2BTed%2FgebTuKcvT5mAzNrKbA9RLH%2F9XyqgV7sE9TPMxk5JlWxd6IoHP8DpvfxDzrLw%2FOt49bFis0adAjRV%2B67m57WAf9%2FzZLTWXmX5eic9COSgeoMiJsJ9OarOc9yunuqPEm8QM%2F8b14fO9721jINcEiCTn8mmBChjE913iNaPsRse8vtiKYe2Mk4oowbOKri7zXESsCax0MZuTeNh2q8X0sslbLUggO2N2yU8PYbO4a4WA0IFz2sBrA4ii%2BjGOyJr8EMyVMOo5%2F7aKFrbAlflUrwiQFA1CtvKwIcFtUOgLEQ2aYOLhp29b%2BB1%2FDmk3Fm1bgHCYZrOsuqgNvaUrJxSJM2W%2FXDy%2FiPCxyi0odSBIq0LawchfN7CARga0PqmMFEj8RY05%2FIw8cGog2wTn9vMYJwD%2BB5zTm3obqKbRuauK3%2FtdWmPa0s5MP5c93dRNQicga4TRawLweDfJJ1C72%2B4DpSAfYMzrGm8nST4SZS93MA3tYLhIxiR%2FYcEUrtmHpRYsAlUyiz0buCA1NlUxiTi%2FriBhu45FxmEGEnRH2JHzroFysRFpVPXMysx9dj5%2B7JCG5esLa%2Fi7brGsSPpyQdJC7b7HOnOQmGngA1GBdYnsJz1P1jMlePsNkRcHEAVy8xgVXENmSeW5K3F8PRYF2CeoS8p2jrdJo97l%2FOlSnYUi6aeuWZdi6ro3MivIwyaQDc%2F3HyCRDPcpIslSt2ATQqt6Yd%2BSAqdYZOHS%2B8rap%2BZSuFudnyiXzzu34ULx2VqVjaAmwD32Fv7h8y%2FNpHM12NShbxJAJWm1WQj5nuBbysbIuQCGfDNnu4j5c5LnezF9543AVPI6ThR9nLp%2BQz1pu5kT0HAd%2BnJw3P2VLZnOQWrHGZbiLWjFT06peVUfVYrJlFwMlsFFqSAqRK%2B2kZAykEe523Mv%2BrDT2czNG26qrYfOkZSeVbs0T8ERF4WKe7J1p1UfVhAQOjNWZJbYOB9K6ysyCxDpoSkbH%2FFc4NbaulngpHZghm43cBPWd1hnqZifRZvd%2Fl%2FHiv6uP92rg%2FvtWvva%2BxFoxUrS9kbEnw5nQlRYZ56uxlPdlcRs7iEUdvd7M4vKITLLufYWWe%2Bx8peKQKZfctLKmV1hZxmLBFCiwKJlqVtC1InVQfzcoLkCDf5%2BKHLABquJiMjYWdMVtOp32wTHAMfLwxmE0TgeGSBl3kHxZn%2F8puhzr%2ByJrMdwn%2B0AUkoNZZBOI6RXj17rfDpDOPtxlsdUzPIVlNztl9AJRJDVGdzZ4frzbaOtB1SvNbMKOjUJmhgBoVBPKDPHbM5BO8e88EvRdqzBJFtnLeI1utaspehFncfD04C5hdPowQVvL9o2TPvCg55K9dlhaidWvgKZQ%2FApBbjxuBBy3KeRScaESG8daQGs72ECodVFfDqsjmorZ9tXoUNogO5pskiR7cf43%2Buv123ef0T8vb2%2FPRdU%2Bxr6oEJiw7vHDby%2FfQWZk07MSgVLzblzII%2Fd77VoJHeT5qYRXZuZcVOfGkef34sUZh8Q2OuYkcLfhlhQe10lMx3FfTx5ZseEqVkoyoW1qMnJ7szERcjPz6Xu1bEycr5nN0QtyoNTe5xuV5%2BEkJnT%2Fzulky3lFoyGJaZwUzX1%2FboJ1TMOWbFtHnnf%2BX%2FWGrLnyC5lw701LkWT9KVVuMwlmZ7xKp0u4NZZxXO2x1dnKPfpgG2TAzz2Ibca1fLwxSNGKD3Zghs41mURFi2E222PUBTKegcN1qcFNkM9LzR7MCFW4wvM0O%2B9mqMtsklkcGZc877u82CoV%2B5L5Dd2EyUtXgJ4KT7aMVTt0aO9xXGrwUZksXErGLJi5lJqmaei8ePSz%2F97%2Ba2ZajjJ3lx8%2BTKM3d6%2BhpizO%2FdOqqpZZt8gb7ttEzcRQ4G9mbawfrD0aRopvq8XIIlFR7DZYDglBHKOIut1oBPcYiFOVTFhO%2BqFlyCZZpUH2w%2FFWKjlln7eqaJTk560qzmrqOOguS9ylnXZbitisalBD74ABOio%2BVmlW7SLf0VQNU0PFsesFwjSsNnIBOwik%2FqQQ4NbxDlfv0Z14FQRwLc7pIEBEsZm78PhBQA%2FPoIQg9lfzwDstUSCAAPfN6xcIgQI0tfq%2BtcAQ2jysUfT7dx4an5sWg52pVa5MMJxlytarSbzOaIV%2BifFjE6Z21fXOZMvfdSorPc1iGpHrtAZtgsCrLAFmlR57SnmWqgNdFE1mCW9vyjZIpFVuXlAjQY6UObRCIXf3xKSu18kVMDoc9tTqfz1SgBLDRjtIkPUIP3dHspGNB9yZcWe4BPu05MUeXF645selrBK0En4cqS1SU9pS0K5sadxr%2FLHbDQplYIfCJoeA9yJqUPkJxs2PgZEL5Hos20WGrvsVOfni%2FYiX39%2B%2Bkqf34aX7ejy%2F%2BjTQvkQ1i0LrtppguV%2BpDfZrmb2HmtjBJzR%2BdEesrbVUKZAXYIet4YKjzsc7w9RWQ1FVE3uen28Se2CRBXobhely%2BXQ6WgoXb0I3jZdf%2Fx8%3D) of the major Classes and Functions (Javascript and Python) 


* 5.3 Running tests:

you need to have `selenium` and `factory-boy` installed (`pip install selenium` and `pip install factory-boy`).
  1. test for "Splitting and Reading a text":

```
./manage.py test functional_tests.selenium_text_read.Text_read
```
  2. test for "Creating and Modifying Language":

```
./manage.py test functional_tests.selenium_language_detail.Language_detail
```
  3. test for "Creating a text":

```
./manage.py test functional_tests.selenium_text_detail.Text_detail
```

