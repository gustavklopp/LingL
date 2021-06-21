# LingLibre
Learn new languages by reading anything you choose.

This was inspired by other site/projects like the opensource Lwt, the closed source lingq etc...

![Screencast_small_clip](https://user-images.githubusercontent.com/6438275/121800774-05a50a80-cc34-11eb-825a-37145f2e4461.gif)
![lingl_homepage_600px](https://user-images.githubusercontent.com/6438275/116420494-4d1b3700-a83e-11eb-9570-ef473cba9777.png)


## 1. How to use it:

- [video channel about using LingLibre](https://tube.tchncs.de/video-channels/linglibre/videos)

## 2. How to install it:

### 2.1 Use the executable (Standalone application):

Available for Linux/Windows/Max:

the executable is `Linglibre`.

<https://github.com/gustavklopp/LingL/releases>

After launching the app, you will need to create an account (this way, the app allows multi-accounts).

### 2.2. Use the built-in server inside Django:

It will need `python >=3.8` and `Django >= 3.2`

Set a virtualenv with python 3.8, then inside the virtual env:
`pip install -r requirements.txt`

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

### 2.3. (future) Use the online website:
Maybe later if people interested.

## 3. Upgrading:

Future versions are regularly provided. 

### 3.1 for the standalone version:

   1. *(optional)* First, backup (if you want to keep your previous data that you've created): in the menu, choose 'Backup/Restore/Delete your account' then click on 'Backup' (you can choose to backup everything or choose which words to backup).

   2. *(optional)* Delete the old version folder. `LingLibre` doesn't install anything on your system in fact.

   3. Download the latest versions (see the [Releases](https://github.com/gustavklopp/LingL/releases) section) which fits your systems.

   4. Launch this new version (after uncompressing it wherever you want) by clicking on the executable `LingLibre`.

   5. *(optional)* Restore the backup created in step '1': Create an account (whatever name you want, you're not forced to use the same than in the old version). and in the 'Backup/Restore/Delete your account', click on 'Restore' and choose the backup file that you've got in the step '1'.

### 3.2 for the Django server version:
   
   1. *(optional)* same backup step 1 as the 'standalone version'.

   2. Delete the database in 'lwt' folder named "LingL_database.sqlite3".

   3. `git pull` or download the source code. The database needs to be recreated with the same steps you've done at first (`./manage.py migrate` and loading the fixtures).
   
   4. launch the server (`./manage.py runserver`)

   5. *(optional)* same restore step 5 as the 'standalone version'.


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


* 4.1 Building:

To build `LingLibre`, use CX_Freeze with the suitable platform:

`python setup_LINUX.py build` on Linux

`python setup_WIN32.py build` on Windows

`python setup_MACOS.py build` on Mac

The build results (with the `LingLibre` executable) will be in the `build` folder.

* 4.2 [Flowchart](https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=AAA_LingLibre.drawio#R7V1bd5tIEv41Os48WIf75TGxHWc2zmXizCQzLzpYIIkEgQLIsvPrt0E0hu4CGokGonjPblYghKG%2Bquq690S%2BWD9ch9Zm9S6wHW8iCfbDRL6cSJKkaiL6v%2BTM4%2F6Mpsj7E8vQtfenxKcTt%2B5PJzspZGe3ru1EpQvjIPBid1M%2BOQ9835nHpXNWGAa78mWLwCv%2F1Y21dKgTt3PLo89%2Bce14lZ0VNfPpizeOu1zhP62pyv6btYWvzl4lWll2sCuckq8m8kUYBPH%2B0%2FrhwvES6mHC7H%2F3uuLb%2FMlCx49ZfrCWX3388tWZra4j7Z91%2BOflz3vtXNT2t7m3vG32ytY362G23dhW7Ey%2FRdmzx4%2BYItHOXXuWj45eLVzPuwi8IEy%2FkW3LMRZzdD6Kw%2BC7U%2FhGmxvO3QJ9Qz9z9hr3Thg7D4VT2TtcO8HaicNHdEn2ra5m9Mw4SlKy490TPqqZnVsVoFHxhVbGE8v83k9UQx8ywsFEvNgqzp8746d4f%2Bt8EH7cf%2FthhueKSlEpDLa%2B7SQ%2FEtBrB2G8CpaBb3k3QbBBJ0V08psTx48Zx1vbOECnVvHay75FBAofv2a%2FTw%2F%2BTQ6mKj68fCh%2BefmYHUWxFcYvE85HJ%2FwgxSk999pNXiq9hkahljeiYBvOnZoLpUwwrXDpxDV0yq5z7JLM0UiHjmfF7n1ZBI9Bre6pYc6fIZrF2%2BjFHw3I7lZu7NxurJQ%2BO6QDyyh2ISH1csssN0pZbDRaakQJkBqNl9CIFPlPlfIiQXpRlqYqG%2FVVlRP1aebPqB%2B7seecMPElgZHxuZFeHs9i4Ty48df9lUZ2mPxQnAqKlB0%2F%2FTI5KP7woxO6iCJOOPCqIna9qmQ%2F%2FRi46EWeGEkgpFgiNOP%2BhbJfETySPwYT21x%2Bf%2Fh3JS2%2F3rv%2Fe2n981Z%2F%2FWUpnUsmxTfJK99mh09cc%2FV09tV8G96njJVwSXdsJrZjsyM4AybF6A0O8LFl4RnBtgjyEW5kH1uPhQs2idBG1bIvEbIvC4SrRVwvi8ddL2oCwW37J%2B5UocjieNix5brVBzvCF8rj0ijSaCHUx4uhMi4MaXtwLBiOF0J1XBAqzxC2hlAbF4R0CO8ZwiYI9XFBqD1D2BpCYygIrxfv1vcfr%2F96%2F1V9%2B3Z7u9u80%2F%2FE%2FtozgiCCIMk6d5COkkH82HRcEf1jzYLFbBfM5gH6x%2FLtWeSuTynOqxuJ1Vvy%2B4DclKTk0d%2Bu4%2By1LgsQ6g0tP0q4IvBPCAVZI31vGgKBU7y31t%2BgAQiDteW7P08dAREIufcMgVoFgRvNg%2FUmIfQuCO1TBkEfHAS61ABn%2FFbBbvab4ACVK%2FSMg16Fwzw40SVBJ5YEY3AMjGoMTnVVIEBQ1B5BqDOdIQwSJYTeKz5h%2Buc5hz7oD78DLQQrx9skJXVjLDw7JykIEFA0DICCEpkq7q6GifaYO3SBp7pI5AkFUW5whNOjQ0sDMoZoLA3AlaAF5xi8rvMwMZy%2BM8kCH5XAe%2F%2BgXZQG1JGjIEcfQyeKXH%2BJzp5ZZ8nv%2FYReSKPNQseyO1VqC2PuzEHpuzPURMu3xr9FdY9gEKsKa3UPL4mkPY3ZOrh3Zn5C%2B3Hbtu2pLxN83yf1wXIBnaJtMYCYlcN2qSHVkn7sKEgIqEHwbVVaDYLXDZZqqXvqgoRMJM1Dz%2F%2FKdu%2FRx2Xy8TpAlwSE0nqdfkY3z65HZwo%2FoaBPri4DV62hqnSa5blLH52bI8iS5exVIh3u3PJeZl%2BsXdtO49CQ2JY5jZscGpRhwmra8ZJD2tWfSMoLO5hv1%2Bjl%2F5gmeD6%2BWGz9eerlOKejE3WtHAIWoUJrHcCCW6G1bNaaBzYyDy4SYQuTo8vCkWatEzr7d9EmpZhwtqz99vqEDQ1JHs7OgHtO6LA%2BoEbnnjv%2FjjVpYn0ACD1r1YqGCcK0FIFMgij2iblKG%2FoA5qlw0%2FIJgnslTQxtYkK3SViG6R70T5%2BZq9l0Fpv1CbRic1slVA6RBJZetIItLcta0Zo%2BF6aC2ne4oVbuRhNvkNSpqZWVE7%2BQA0wSOqnZjSoSgNuQd3hWTXxjKk2aCequ7UIx%2FfPXPzff1A%2FvPr989eU%2FS%2F%2Bs3c8ugOAWAOt0Oo1XTmLYzOMQ3bJs%2BFh%2BgL4NcxPoGe8i3hoZxenTzgGzY2JFQDNxMsTMBTmT8AcZf1BKnox6djLOh6gxRDl1oKioC4S%2BuB%2FNNwvdsKSlvf70aR6%2Bu317TruUVc4HDnl2JXO5B1%2Fl8%2F8SMqdKhMyZjPZfF5kk2J%2Bka9i7jJNKgwZKsbNcNODq%2BHosEwroDq0uMZGREdcClJI1P%2FesKHLnhEGfSuzK2iR%2FeuE5D9nVhT7jPR%2FgPuNJbY8xm2kv0jzA2k4MMxUfI7665fAI0%2Fzuw1ZdXn9Y3%2F0rr3ez%2BadoZd8Arf2Qd4%2B45SW6qjRzAV93F%2BLLsvPppeVrGi3tXZDY1ukv9x%2BpmzMuCgkQN9ad45UZmV3PI9PB%2FWndpfdLeCgjPbq5%2BmqiXrLrm8qagXz%2BUPZXJsUJP5D%2BF6a6opQDxRi3I31DRZ%2FidqRH%2FLdEs%2FwfrXzTYLGIHC6JaYnrYJxjk2%2BsmoPV%2B5fGtXjQORgkJ%2BtFEK6nm0cKl5rqGtUxbAWyxQzpTta0Otq28EKIGgoDqK7Jy%2BmLFlFex9R9SKx%2B4kJX2eQOJzZhzJtZmjV1rA7WIATnFet71jkk%2BBVRn5RLoBS9QdOAhsuoUcbBm5GoLpGpRABrM2bv8qiU8iFKsF4vM6tGs2woAIX8oPOvc9OLdN0mAE%2FkWOF8NdsEyE9AVlHkrl3PCluFA35VwMiRU1ALEpQslnkhhuX7EMQuiL6Mk0aOCIVKujjVNNpyLgIpQ1EaY4rHOnSOJS18aZxtlgS%2B95%2FiYLn0RllCLZGzOw1oEh5IUpGbOqNjmTBBx1C4WcsRh3K5qUPjCFVOSR54zFP9aKzxFW4CvmNdIVyjBTZY4BGGg07ApLNR8%2BzpGJXLOdngAjQYyQKUJeHmQYp0LC6lY65aHHt0fY%2F1DMGuY8pGK1QFySuNDKcA6Okgg6mTw3zBWmAaFZFoMmoiebCpLrCzQa8Mw%2BWlRg2cMrI1hLar9rov03snpu%2BqWsAGU3gy3ead0t925%2FHOuUu6LE%2BI%2FMRyA1ZIQOTntycAzf6I9NHGsx6rYiKnCYUMDdzmBQVYTqTSkuB%2B94Od5XknRHaVIDvYd8KpRgh%2BhfrBlp37dEePNGZdkVkXZGz9j2VBpkt2s610Zp7rfx%2BjSycTdW8mOE8L0CUGN70O5CZSrxiTMqmSmG3977tRzO6oZ4RDS4IHd%2BZEWqPPQyedafYbwQAW6vaKg0THN2hh2KEbnTQOeS5nOBxo1f4byoMEFdH2iwNUc0PKg7v0g9AZscV%2FLA7QeK2ecWBbH04eCWjGVs9RCDrzTEuE51ih7%2FrL0wVCZY1H8AOCTulAInH6UGjQ2K5%2BrVeDom3zmOsRTbbu3E8eV8Yh36%2F1t41bjCuRAHTB%2FN7iMtjmJzA8h%2Bxfc8LwYJ94LPAcsrHJKcMz2O5P8OM82wKgBz0WeOpbQH4%2FeMZlqh20%2F90Jw4O97bHA82wagD74WOCpSGWlBZ4jbBE8zwO8OKrCmojil%2BSW6Ygv0FlB1NyMs4WinkcOLS5XlalId02Asy0Ucarpx%2BME1oBoEgtOxbKQ3wkkcHAzR4jgiqn6uAv31WIqCVJxxUjmz2lSw6LxNNlCwdMs0skWU0GSJ7XTLdAB2SNa2sru8PEXtVNgB6j%2FzX7asKc2NcFu%2F0rcJtgptO04mOmBuajIQngL5UoOOmIey%2BFsBFUj9zRG5bgycjojiEeg%2BM4O%2FfvhU%2FqwbkzPKWmeZEJtYEVf8unzDajeep9sUisMXUw20RRs5%2BJ88P7oSH2BNNjUlEs3lqYSj1EmMIXoQM1gKYBBJB%2BvC80LyLhCOGrPZaiE6pdagVk1JDe3MrSykSG2NzKYOKBuuu2vlj9SOXR%2BtQOtxcwz7y69Jdb4g4Qz8GzfAYCGVb9O%2BP256djTsGONLq%2B7ubq%2Ben9JMVYhRFJJ%2FxYBD5WsrALcNHD%2BAEmg7iZJMMU7vln3VjQP3U3M6EePf%2FBnPWMcXMILNcf0OvdTZhrk%2Febzu5vuoLS1O03VaCgXi4XUw9zkY6GsmcMDQsdrTBLdYQYg93eUDr52E0Ja6W47JzP%2Fmo9IsobCupDI7Rd59d%2F55ew8WK9%2BaPHsYfvfIx432HMY7BBjpaqNOreHmU2TWigbDVPWmMRgdikcIaFD0h8fEXD%2BIaKYh4yrgsy%2FoiiCDS69ro5g2oC0%2BaCBx75d4Z%2FTpwuwtiRsIyMX6AaN88HnjjTPSdQMtkAufZ%2BmG%2FE28%2BkttV5%2Bsx5SAv3YOlEMKuZxBPByRu0ggId5vNvBxHk%2FML4t1n%2F8Y3caHfxNVOoYc9yiSu46hu%2FRtJcjR5%2BPydBMSwdsJ7bcXy19mrMH%2Bxy7w0xGntlT7I2MdILaYZNzmKesZcH55kG34wpNavQwx5e2vd%2BY00L%2Fe5%2BmplLzr0vROWgvmwNUGRG2E2lN1vPu0HQP1Gwbu54bu040u3edXTTKNcEgCTn8mqBDhjE9UXaDaPsZse8vtiLorTEa44owbOKri7zXESsCa7kLZuTetnup8H0MsiTLkAgO2N%2ByU8NYr28O4WA0IFxaWA1gDRRfxtFZk18jMyV0Oo5%2FZaOFLbclflUrQicFA1CtvKwIcENKOgLEQ2aYOLhuw8z%2BRw7Dmk3G2wXgHCYZrOsuqgNvJknJxSpI2G%2Ff9T7GqVfk5oAqkCSUoA05xS5a1kEiAkPny8MDYjcex4T0Wh44NBCtgxPSeQ0NgF%2BB5xzc3lrQJVo31fFb%2F2srTHva2cnGoWf7aY1QiYgK4TQawFQeBfJJ5C52WoDpSAfYUzpG27u1G49mInA9D7SwXKbEDHRgqwsl3wCjFy0CVDKNfSptR2go8lQnJqSyDoLhNpgWhxnGMJO%2BJeGLmh5%2BN4FR1TMnM%2FvR9fi5CxKSqSes7W%2FTbZLugocTkg5y3yPWyZLcRAOPeRqsGayV8DxVz%2Bjs5TNMVhRMHMDFq11wRyJbIs%2FtYPvrocjRLkDd2K11BNrA5uV97lwN1WloU1U3VcPQTFVVBL2kPHQy6cBc%2FyHoZKhHEqaGrOTbrxnlG%2FOOHDDVOgOnznxnl5hPyWpxNpEumPfMxqeijeUXzqElwDz0E%2F7DxVuezaNwsa9B2SGGjNFq44%2FyOYPNKB8r7QIc5ZMh2328Dxc6trNwfWcW%2BN7jLF65UeryjfJZi82ciJ4zz43is%2FqnbMhsDlIrVrsMj3kbe9Ew87kR2CjVphKRK%2B2kZAykEe52bGV%2Flvr3uRmjTdXVsHki9WmegBdKEhfzpHWmVRXKCQkcGKsyS0wVDqR1lZkFiXXQMIyO%2BS93akxVLvBSMhdjvyl6q77TKkNd7yTabP%2FvIlr9d%2Fn5Xvbsv9%2BLV87XSMknhzY3MvZkOBO60iDjfBWWclsWN7GDmNfRq%2FUsLgpkkrX1L5TMY%2BcrFYcMs%2BSmlRW1xMoiFgumQIFByVS9gq4UqYP6u0FxARr8%2B1TkgA1AbHzP2FjQFbepdNoHxwBnyMObBeEsGRgyTbmD5Mvq%2FE%2Fe5VjdF1mJYZvsA1FIDmaRdSCml09Z634jNjr7cJvGVid4Cst%2BdorwAlEkMUb3Nnh2vtto60HVK%2FVswo6NRGaGAGhkHcoMdVHVAofh6RT%2F3iNBf8sP4niVfow26Fb7mqIXURoHT07uE0anDxO0qWffOKkDz3Mu2GuHpZVY%2FQpoCsWvEOTG40bAqZqjXCrOZWLLTgNobQcbCJUu6sthdURTMd04GJ1KGmSFu20cpx%2FO%2FkT%2FvH3%2F4Qv6v5c3N2dj1T5aW1QITFh38uG3i%2Bogo7DpkYhAqXk3LmTt3rEDuZBtPT%2BZ8Mr0jIuq3Djy%2Bl68OO2Q2EbHnHTIwEWuk5iO476ePDKD2OU8n0%2FUkJFrzcZEyE3Ppu9VsjFxvaLXRy%2FIgVKtr9dKz8NJTIYZBPJk6cmaXmT0xrgzFI2ABa1ezkqS2oPw9FQIfy4KUomLTGzL9xTP0OiGsNMpv%2BCV3oC4qHbCOHc2InSRrplT01QlXcj%2By8RTAHcS8SLdkKai%2BlR7YTJp%2Bs54lc6%2FcetU5Gg%2BYjemkXvUwTZWgZ97EGOfaz9CbdSrER%2FsEQ%2BdvNSJEilNrzfwqR%2BIeKgSV9sFd9U%2BLzUtmBEqmYYHtHbeHlOVKifTgqLOZrLQKUmZCqaK%2FKa4wuSlS4pPhScb5vQdOgX6OC7V%2BKhMFi4lg2DMXEqNZ9VUXjz6xf1ovlnohiUt7fWnT%2FPw3e1bqMuPc0O%2BLMtF1s0T0W0dPSaGAt%2BZdVLDYP32MFJ8e3cEg0RFMptg6XkTkcPZAA6gSjQfDFvmTlhO6qF17TpZ9kM2WPJWKhlln%2Fc%2BqZXk571PJhWFQXTbLm77T9p3x9j9rFFTFIGJTDI%2BV%2Bp%2B7iKBVldeVUHFme14o%2BmAruUCdhBI%2FUkhwG2EAlwOSrd2lhDAxV2ngwCRFmFu6%2BQHAT2NhRKCyPWXnnNaokAAAe632C8QIwrQVOr7xopVaDe6WtHv33mofW5aDPamVrHURbPWCVv7d9EmpRV6E%2B3HNkjsqqu9yZYddSorPQ33Esh1WoF21eBV5wKzSo9Nyjx7H4C2nDqzhLc3ZWok0jI3L6iWIEfKHFqhkLt7YlLX6ygUGB0Om7T1vx5JQM1qrR00kvUIP3dHspHOm9ybcRNc039a8mIOLi9c8%2BPTtLS4FH4U5AapKexRaZa2wu41%2FtjtjpcisOVlnUPAexHVqPwE46bZwAwPcj0WzTxDd%2FSKjA7DIBH3p8uRKK%2FeBXYS77v6Pw%3D%3D) of the major Classes and Functions (Javascript and Python) 


* 4.3 Running tests:

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

