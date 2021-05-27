# LingLibre
Learn new languages by reading anything you choose.

This was inspired by other site/projects like the opensource Lwt, the closed source lingq etc...

![lingl_German_800px](https://user-images.githubusercontent.com/6438275/116420467-47bdec80-a83e-11eb-8023-4f67974223ad.png)
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


## 4. Developers:

* Building:

To build `LingLibre`, use CX_Freeze with the suitable platform:

`python setup_LINUX.py build` on Linux

`python setup_WIN32.py build` on Windows

`python setup_MACOS.py build` on Mac

The build results (with the `LingLibre` executable) will be in the `build` folder.

* [Flowchart](https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=LingLibre.draw.io#R7V1td5u4Ev41Oel%2BCMe8449p2mZ7m267296%2B3C8%2BxFZiWgxewHHSX38FRgSkAWQbgULTs9saWcZ4npnRzGhmdKJfrO4vI3e9fB8ukH%2BiTRb3J%2FqrE03TdGOK%2F0lHHnYjlqHvBm4jb7EbUh8HPnm%2FUD44yUc33gLFlYlJGPqJt64OzsMgQPOkMuZGUbitTrsJ%2Feq3rt1bxAx8mrs%2BO%2FrVWyTLfFS1po9v%2FIm82yX5ass0du%2BsXDI7%2Fynx0l2E29KQ%2FvpEv4jCMNm9Wt1fID%2BlHiHM7nNvat4tnixCQcLzgZX%2B8uPXb2i2vIytL6vo7atfd9ZZ%2FjPuXH%2BT%2F%2BITzfLx%2FV4uvDv88jZ9%2Bd8YRemNggRF7jzxwoBMwt9Wmpf%2FzuSBUC9B9%2Bn4Mln5eEDFL%2BMkCn%2Bii9APo2yKfu2YhjnB79x4vl8av3HmaD7H467v3QZ4bI7Sr8cDdyhKPIzQef7Gylss0i98uV16Cfq0dufpt28xP%2BKxKNwEC5RSYFI8YJlkORXTe6L70lBOwksUrlASPeAp91XGzPlZzwm4LTHHJJ%2ByLPEFYQI358fb4saPiOEXOWgwgBcbA73dOr%2FUu0%2Fow%2BTfux%2F%2FTqMzy2SojhaYhfPLIAwQQ4YwSpbhbRi4%2FlUYrnNkfqAkecgF0N0kYRU3TLDo4Vv6ecUkl9%2FL7726z2%2B%2Bu3rIr%2BLEjZLzVBAfHyYbe%2BOlv7MZlTjcRHPUwL0EDHzDW5Q0UEnPhTIlTSPKEfLdxLurSv8xoDU%2Bd0nsfrh3bjyPvHVyiBRZcwdd37BStHCRcyO%2FFDmT%2FqQIBkRjAPn4gIUkOAQMR7vWLQsAw0TOwpAeDLVPnQajYTFouD%2Fc%2B9lmvXATpPyIGVTirbfy3Uy71ElAvcx0QELbrNJQM1iONqcADU1D1MJgsAtDh6tAeQ0oLQmdrgKNvNG6NmicS4Mm1crA6qES588wzZJN%2FOKPFmQhrVFCsQsJaZZbbrkxqmJjAeuABkiNJUpoVIb8Y6W8atBaX1NMPuqbpiDqs8yfUz%2FxEh%2BNmPjahJPxhZFel2exQPdeknsaTn6ZeRrKxNDy68dPphflD35EkYcpklpVg64qaterSv7RjyH2wsumGyXFtE22%2B0H5pygeKR6Di21e%2Fbz%2FvtRuv915%2Fzl3v7yz33y91c60KcM3Ze%2FzkWteP46%2BnG%2Biu4yx1E49U3U%2FNjuCM2BSSG9wgI%2BtT54R3BdBMcKN7WP3oTRhnQptXC%2F7GiX7%2BoSK%2F1HzdTp0ted81ZpQ3LZ74k4Viq7Kw457rlt9sCM8UZdLo2jSQmjLi%2BFgAUoYQ9YelAVDeSE05YLQeIZwbwgtuSBs3tt5hhCaaMsFofUM4d4QOkNBeHnzfnX38fLvv76Z795tPm3X7%2B23xF97RhBEECRZ5w7SUTJIHpuNK%2BK%2F3Fl4M9uGs3mI%2F3KDxSz2VmOK89pOavVW%2FD5gb0oziuhv13H2RpcFCPVGbhCnXBEGI0JBt2jfm4UA2mLtIt7b6G%2BwAEThyg28X2NHQAVC7j1DYNZB4MXzcLVOCb0No8WYQbAHB4FNNSA7fstwO%2FtNcIDSFXrGwa7DYR6OdEmwqSUBSILqGQOnHoOxrgoUCIbZIwhNpjOEQaqE0vSzEdO%2F2HPog%2F7wb2CFYIn8dZrnLWPiGZPGASQS6FDimbjsPeJuicklqKYfP%2Fq8x3nAOejtCccnjAMMzhssFNz01OXk1gjFsRfc4tFT9zT9fJD%2BLKxcZhFyF53qlyKTvz73f0%2BY%2BMXDoQwdwM6B82xECQdr889W4R2aBSnp5bYy9ya%2B5VC6CVhchVEf3Li3Gdr2WSshUFmBv9ZklRVcQjKUsmp66uaKpMsQTwkpnfUme41vPpbipI7kkPb2uJ09YTVLAMTGi0U436zwb%2F9DSeF8eHGzCbJasxdoPCpRp2KxKrQg2QAWwjKeSbFHjXGwwMbBRSprUXr1qnRluauUzsF1vM4oNjm9bXz3csRmhjqclQHXfrDhdUCJzn1v%2FpPo0dT2AAB61qk12yrt0WRV7RNykzXyAcgz0Qak86wYy3HNmIKeBrMA8yXP7NPOPlq7xuiXfQQ47TxVXyVbWXf0fazl7OrQdH9uE3owhx%2FOybVpvUP6K5Bb7B60i3x%2FmB7stuEeWqYYyj5w9qxlBGuZouJ0AC3z5e8vVz%2FMD%2B8%2Fn7%2F8%2Bj%2FX%2FmzdzS6AQBQArKIoyRKldsg8ifAtq3aKG4T43aiwWJ4Rrxii0wHtEnBTSa0JPqYugZo7DKcaeaGTF0bF7zBPx%2BMqqLqtVJ1A0AcEsnGEBSWLfhsSROwrRsPcd7EnOqfshkx%2Bl%2B46%2FeIbH93ns4%2FoI6JxrvLqYHH96w8b8%2Fbyw%2Br6u77azub%2FxMvFFVAvC6jTFK9zPKtSyEzmXUdkWj6eTa3OaV2Jt2G69maf3L1kbs6pplOyXrnXyK%2ByEr%2FmxYrF%2B%2BVeZ%2FdLmSkvocI3N1%2BemK%2F45bp2I67oNJV%2Fy0m5lxMk7xPFNoyqvBPcjrQFDVshOf4P5LvUafWPVb1peHMTo2MNQ5hgQrtNHBtH5%2B4nxKkHtKHUAPw0bDwVy8nqJoxWyvqBwaVhy5o0qKlvaVNL2z22hagtawfYsy5yVMvrX5Ec0L3321zG3NXGUIdtUDQgZ7txyWrdBTIHy7qH9wiaC0EF7NUZql3RMsrEsFs0DRiDkBplso8giepSuXb7iDZL98a5DImjtocOUYLNeplbNU6rhgKQHQs6BrYwvcgmQwHwxMiN5svZOsS2OraKYm%2Fl%2BW5EkhlGDRjdxwXK64d2fnRRiBH5PgSxCyrZedTI6RRytqpYFms5l4HUASA1RyG10p1jyQpfFgmbpWGx3askvL31pcxL1OiGeFB2M0RQVZhosBvdMDllyMBq5IdDeRyKM5kABOK6qzX3mpEv%2FwrwG5sSWlqtr%2BlQxhcMBxuazZoNFjsrMiqWMzpjHEgq1CeQkSRs7xRoHpvRsVAsaCFdIVEzQ%2FBrmKrBCvVvhJLPhWkYgy23lyOSze0HNgLTqojUKacm0gdrkwA7GuzK0CVu2niAMyRbQ1iraqf7cr03Mn1HV9tAGe29KjydrZvM6L%2Fw5skWXadlSyMiP7XcgBYtRH5xTbZZ9sekj9e%2B%2B1AXDxknFDqUaCAKCrjTDusu7yQB%2BWPTQhqVPwAdnyBKC4G0B%2FKNC9qnmeQ%2BGhkCFoWANjT3m%2Bw64P0Mwq3r%2ByMiu0kpHcjfEJU5A%2F%2BE5j6JnUc0ju6Qy2uP8pqjxPeVxRxl81Pz48Jmvhf8lDGgoVNVklOwPROgSxxhVg2wK5fFhAgp0%2Fyg2Sb4uZWiFUQzIxxawzN4KENlNfo8QlmLrN8IBhXYUesXB42N7rHCsMU3GjUOGq%2BFIw4HVrX%2FhvKgTQfHAco2o%2BXBuw3CCEls8R%2BLA9StqWcc%2BNaH0SMBtWzqOQbH5lywEuEjNwqwKzxeIEzeaJw4INgNTUgkxg%2BFBbWB6jcixGqni3IZ1%2Bkr5KMEpS4milZFa4DPO5w6xeWgap%2BOcDHohD4AF0tQwALGhQ1Y1%2BCyi9uNHSDS%2FoIABKVcigII%2FgkOQ9v2duMSdRjvPMAk10Z1cZj7bxvwk2v%2FGShd%2FL3FZbAKRRieQ84RGjE8JJgkCzyHHDAzZngGO4ULfpxnWwAMPckCT3PV4O8Hj1ym2kHnEI4YHhKmkgWeZ9MADF7JAg9Xp6c%2FP7%2B%2F6q4Hz8K6tkwLCBDc3Gg99ODZv%2Fl6Nepm51CXYwdQX1VxmNXs22e1HBJ2AjjTqHZFJu%2Buu7j4i85ubwF8T6XXylkp2cwjh1aRmYaissWRIKMbqmLZx%2BMEBjItjQencg7c7wQS2FdYIERwcnRzrEz4Cq9oE628yp9NlIlVjNS1dLj3EtIPIr9MP6sqE03Prx8%2FmV6UP0i3gqgcA8nZsJLXrtC5DYvOzfL8oy3n0au0jt79JGG9KQ3W3h%2FMXCRcVGYhcvx4LQeJbn3GXXgkWe8zuGKM3WAknc4CtMV%2Ff%2Fgne1gvYduRtTcsYw5%2FY6f88%2FkKVG%2B9NzBrFIYuGphZBvFNSPLL7upIfYE1mDLVKzfWFE1ExzKYQuz56F2uPbpV6SaUrj2q2qY1ul0hSFXGEytLN9io52D7aYOoZLJgt6%2FscsVDzZ6LIciCKraul7d3IG8HLrmEzTzkfPp%2BOsMXhjixmr6XDKoaG9y%2Fzm5J1lfQBN%2FdNHPHKuq51abrVjuTVur9Mwy8HNtULKYw51tay2MY3YfStNxkqf0eR6WOwMm%2F5w3nfOLq1s3XSRgOno9f7J64U2MCjEbQ0TZgkUDBomZ1YYdL8lPLda1MUooHQK1%2FyNiRvEQXcTjT6h1qPEH2Pm03EnzcgcXWtZ7%2FcO8zAv27QXECKk85PICCJTvwAAg3d9vAuKieJLclxYTijX%2BL3d24en35%2Bq9XrNQ%2BxshrpY4jTNd0PCsU36aVb3cNArni2z%2FcOzeeR9466W53p8iCrsubFru708wHB9enQRm94KaPMEDZQEgKhoz7PapJnwhK7tF2FKFAeWATousOm1mgxPWe2lZCwR783SXauwb2vZNgN%2B8kDN04sDPHEkYwj4e093aWy7W02IYs54vF7lxJF%2F%2F%2FVxamzRaOLkXnoGqCA1QZfdIOq8l6PtuYLX6abRLP9xIPxbM7D21jKdcEhybk8GuCDXlzbBPlNabtZ8y%2BT2xFsPfGSMYVoe9Y4xFx4%2B5XBN6tX8LIHceO9g35qA6dnuBoFAcIiMnYzcntAowGjMuxB1iKZRybN%2BYomSlhs%2B766wVe2Apb4qlaETYtGIBqFWVFgCc0smFLETLDxcFNJ0jKEjTXqYagOu3mdxeghE9XZORiGabst6vSlbHdlUkZEyYQQNGgEypVYbXqwDkL1a4BiZfIcSxAIw8cnLZcnEc5WLcA4GCAJ1hCq7G6qYnf%2Bl9bYdqzzk5%2BCkB%2BhJyESkQ1KKfRAdrxGJBPondxVhJMx5oeqPHmeuUl0rSgbeaBPSwX6hBbi9UhmqEpQOsEYVoE2NSRvRlzR2gYumJTrVF5O8AI60hLwgwyHMWwJ%2BHLmh7%2BbRNOVW8NVlDc%2BNwlCcnVE9H2n7KTwa7D%2BxFJB33UF29LSWGiobKpp%2F0WRuwlPI%2BJWDZ%2FJhaXFdV4YHyrbJEFVxLZUtlw01NMWy3QLkHdWrlwBNpAjnJP5Qe1KUeWYtpT03GsqWkaE7uiPGx604E7lWli06EebaI4ulGcOOhUbyw6csCVBwIMnQZom5pP6WpxeqJdcB8TT4bitRuUxk7SHlwHviJfXL7l6TyObnaZIlvMkAlebQIpnzNcS%2FlYWUWMlE%2BGbXd5Hy5CC3TjBWgWBv7DLFl6cebySfms5cImTM%2BZ78XJafNTtuxsDpL22LgMd5H2aBtU%2F8aOEh9VZ1rUUBOj1FI0aq%2B0k%2BxHmEaD9BWqy8SvFnG01kgdUBbQrXky5H6DqlOBryl9XK5os4FNlyNll6eb9aIUNZdZR9SdpHuAjsAAVIsjO1IRUyq%2BpqlkQLx%2BIAVoe%2BmHingLc1a51cNJ2X3R%2BnRfwImELSRxVg9qzSAMYUOl%2FNup47ThfHAxVuPhcU8OR6FB1pO9gg5wz4NhWx5wgz1ozIE5qN2mVD1vkMGmtnadaWpoUjcTbCGIrauvsqQ9Gp6EavWl4knm%2BHRunqQSPqaTAXjykD63opa7PVm4W56Ce8AIYal9s0R1KkBqO22FvpTWzLdVukoqhc%2FZZBfcnnta7WUOH8E8QBOKxtVUtEIyqFNvVcsylYnpOJpualNsQlLhE279ZIJc15dqMsl2Zrl8b7cXOwvQdhZGs7SJkZJxA8169Xk4RcvM%2BiabtbyxTxYIVdAHZvPZwN5q0fmx%2B5Nw2SyQT9ke9wnpDLXr5zR5gSmSOvy7WGg%2B3u2u90FZxM1swo%2BNRmfoANDoNpShI%2Bz0GaAkbBf1wd8VhEmyzF7Ga3yrXW73izjLR0gHd4k744dJBc4z6xsnc%2BBzAfZs7HP4Kgc1YXkKyQakbQ%2FY6VfKpeJM16t87gBHLYE9STqp84PVEUvFefkwrOtNkuxOxXqL%2F3r314ev%2BJ%2Fzq6tTWbWPtS8qFCa8RymKO8Z%2BOoTiqXh6RygT3r5tnftbx0nB0G1699sA7AEfuWK81tAup1VtZakqE9VuAQkMzx8SjOtbNHvaxz1TJ1pF805NvpBvV26nxdZPjydbUdRuH8RFjc3phbMRlQ1gW1NlOjWxx53%2Fx8VTAHc6dChOU1TzMVVRWBc2mJqDeCOHs4nRkxIxVEeZlv6YlCNp6wduI6lUZNVR1X4BZ%2FMPnmL8nbgXrerCHOzgLPi5BzHChdZrNkajWvEh4jB0Gw2bkksrj13XyzGdc6523AwVJpf2bFvszYxQSRncN7in%2FRbVpHtTqIemJUx1JsipcnYX7ownRWYlDMuTLS2xgWNpeuBSS4zK5OFSOjjFzaVMa8%2FOshTwZRSGSXl65K6X78NFmg37%2Bv8%3D) of the major Classes and Functions (Javascript and Python) 


* Running tests:

you need to have `selenium` and `factory-boy` installed (`pip install selenium` and `pip install factory-boy`).
  1. test for "Creating and Reading a text":

```
./manage.py test functional_tests.selenium_text_read.Text_read
```
  2. test for "Creating and Modifying Language":

```
./manage.py test functional_tests.selenium_language_detail.Language_detail
```

