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

* 4.2 [Flowchart](https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=AAA_LingLibre.draw.io#R7V1bd5u4Fv41Xul5CIv75TFN2rSn6TTT9DSdefEiBtu0GFzAcdJffwAjB6QNljECxUnXTGtkwLC%2Fra1910g5XzxcRvZy%2Fjl0XH8ki87DSLkYybJsilr6TzbyuBkxNH0zMIs8ZzMkPQ3ceH%2FcYlAsRlee48aVE5Mw9BNvWR2chEHgTpLKmB1F4bp62jT0q7%2B6tGcuMXAzsX1y9NZzknkxKunW0xcfXG82Rz%2Bta%2Brmm4WNzi5eJZ7bTrguDSnvRsp5FIbJ5tPi4dz1M%2Bohwmyue1%2Fz7fbJIjdIaC5YKG%2Bvb3%2B44%2FllrH9fRB8v%2Ftzrp1IBx73tr4pXtn%2FaD%2BPV0rETV%2FgZF8%2BePCKKxGtv4dtBevR26vn%2BeeiHUf6N4tiuOZ2k43EShb%2Fc0jf6xHTvpuk35DMXr3HvRon7UBoq3uHSDRduEj2mpzwgDiroWXCUrBbH6yd8NKsYm5eg0dCJdsETs%2B29n6iWfigIBxPxfKW6H9fmH%2Bn%2Bxv0i%2Fr7%2F%2BduKTlWNoFIUrgLHzS4S09cOo2QezsLA9q%2FCcJkOSungTzdJHguOt1dJmA7Nk4VffJsSKHr8UVyfH%2FyTHQgaOrx4KH958VgcxYkdJWcZ56cDQZjjlI%2B997KXys8hUWjkjThcRRO34US5mJh2NHOTBjoV57lOZc6RSEeubyfefXUKHoJa01PDnD9OaZas4jf%2F2YHseu4l7s3SzumzTmVgFcUuZkjzvKWeN2p12ujkrJFkYNborCaNRJD%2FWCkvYaSXFFnQ6KivaYyoTzJ%2FQf3ES3z3iIkvi5SMz4z0Cj%2BLhfvgJT82Z5rFYXahJIiqXBw%2FXZkdlC%2B8diMvpYgbDbyqSF2vKsWl16GXvsgTI4nYLJYxybh5oeIqjEe2j0HFNhe%2FHv6Zy7Mf995%2Fz%2Bzvn4z3tzP5VLYIvsle%2BaY4fOKad0%2Bjbyer6D5nrIxLumMzaT82O4AzYFJwr3CAj62IrwjuiyCbyZ3qx%2FZj6YRlNmnj%2BrkvY3NfETFTCztfkQ47X9JFjNs2T9ypQFEkfthxz3WrD3aET1T4kigytxAa%2FGKo8oUhqQ%2FygiG%2FEGp8Qai%2BQrg3hDpfEJIuvFcId0Fo8AWh%2Fgrh3hCaQ0F4Of28uL%2B%2B%2FPuvH9qnT6ub9fKz8RHZa68IggiCJOvcQDpoDqLHJv2K6V%2F2OJyO1%2BF4EqZ%2F2YEzjr3FMfl5DTPTeit2HxCbktWt97drP3ujyQK4eiM7iDOuCIMjQkHRcdubhEBk5O9ttDdIAKJwYQfen2NHQAJc7j1DoNVB4MWTcLHMCL0OI%2BeYQTAGB4FMNUARv3m4Hr8QHKB0hZ5xMOpwmIRHuiQY2JJgDo6BWY%2FBsa4KGAiq1iMITaozhEEmhNL3So6Y%2FtuYQx%2F0h9%2BBnARz119mKXU8Jp6d4hQECCiZJkBBGQ8Vd5fDRFrMHZrAgiFhcUJRUnYYwvlR29SAgiF2pgagTNCScQye17mbGA7fWXiCj4bhvXnQLlIDmshRmkfXkRvHXjBLR0%2Fsk%2Bz6IKNXKtHGkWs7nQq1qTlxJ%2BDsuzO1TMrvjf8e2T2iia0qtNk9rGYkaWmMF%2BG9Ow4y2vOt2%2B5PfQXj%2Bz6pD6YLGARtyw7EIh22SwmpVeRjR05CQAyCb6uRYhA8b7BQS9NTl2bISNb99PnfOt59%2BnGWfbwM01NCTGi9zz%2BnNy%2FOT0dKlxDQZ2dXgauXUHUyzfa9WZCOTVLIsuXsbTY7vIntnxVfLDzHyf3Q0LStchqzeWgSigmtasdqHpKm%2FkhW3zjhZLVIX%2F4%2FQobn45vpKpjkVo57PDLR0KsuYAlKtDYALJglWitWo3rgpOrBeTbZouzoonSk24uMzsFdvMwpJp7MGr%2B9PGJFQ1aG0zPgmhPSrQ%2BI0YnvTX4hSZppHwBCr1K1pmACUy0lIJIgSX1irpGKPoB5PrnJ%2BQmC%2B04emfrIgm6TsQzVPchLX5lrt%2Bos7ZYn0IrNbJXQGHgSaGrRSrq0ouhlbfpUFEStb3dD47zjxt8ga4KlV4UTO5cDTBIyqNmNKBKB2%2BB3eBVNbH0quyQTVF3bhWD6%2Fvf3q5%2Fal8%2Ffzt7e%2Fmsb3%2FT78Tng3AJgFQQhmbuZYjNJovSWVcXHDsL022irAr3iXcZbx704feo5YHRMqnFoZkaGVJggJzL6oKAPasWS0U6OxviQZMUQqmYlpC8YQFpRFxjdetfWh6lh2vLMWXz9Ook%2B33w6JY3KOvMDOT27mnVbG77O6n8Ws06TsVlnUWqAXcSSYIuSzGLv0lMqD%2BoqReZyWYVr4mteehSQNVqDea8r2vzEt%2BPYm2AKfT5f5%2FYy%2B%2BGp7z4UZ9dHX9sUAcOMMFhFyN2XlTa7%2FLK4%2B0dZrMeTr%2FHcuQLK6yELO8XrLD2r0vcAnXcXodOK8fzU6jk7td11mOm3%2BZWbj8TNKcVyRtYr%2B871q6xEL2nT5dv7Y9%2Fl98uYqai4TG%2BuvR1pF%2FQzvjZuv%2B0BVPzKqNxlB5LAomCoanVVRbgdaJ%2BphoBKgh7Rb0lW9Y9evWk4ncYuk%2BCwzLQ5zaEBMFo5QGuBy3yJbzIOks6TxTSMFsLykcClIcNFc01HhbQhU75TdL2JtntYAlgegwlkuGxT2ss6yTaXqHu3VHPXg64iuh12TUKY72Zp2vCtNliRDhzba64bZxBkVyVjVE1DUo0dkgb0C3KNMnKgcCK6JKowPZJm1PbdQWHdNkKwWS5Ti0arqigAyfSg%2BW0wk4tk7iQAT%2Bza0WQ%2BXoaprp5qRbG38Hw72ssgf66A4W2foDIgKGCrsEIMze82iJ1jtRFHjRzmjpQNSdB1UnMuA6lAfhJTQK0VOseSnHy5p2ucOZ83n5JwNvO5TGOW8f6ZJtSNDiSpxEyckd5EmKA8JE82ckRbLrcMqCWgxijQArdaam5PxV%2FyJGA7NiWj7dTABnP9wXCQQZC8P%2Bk2gsmjcDnFi0yAIh9FhBQlZkkzEumLy%2Bm4FS2uw13tYTND0MuYqtIKZSKyCuXCTniyQwcf3mxqW7ARmJ2CSLIoJZEyWGcV2NggV4bhIkNcA6dytoaQetVG9hVy78jkXV0Z1mACTyFLrXP6O94kWbt3WaXjEZEfW27AHAWI%2FOz68pPsn5I%2BXvr2Y51P5DihUKCm16yggJtzkSbzZia4%2FrFJIRnL1AGaDTCTQiDtgVKBLe2zKhDfPTIEsBIcVR6a%2BzVyHfB%2BBeHa9v0jIruGCR2w8olRjhr8Cs2tVTv3aBzcVJtWH6VVR5Hty4s6SiaNF5s5jX0v%2BMWjQ0PBioAssKMbIEtMZloNEJnLfUKIlFmO0HgV%2FFpz0T2mmRHaJqUP7sqQSIk%2Bidy8q94LggFMFe8VB5n07pGTYZ3e6KhxkGk1HHY4kKL9Bc4HGUri7hcHKOMMnw%2FeLAgjl2ON%2F1AcoAZvPeNAtz4cPRJQl7eefXBk3gU5I3zXjoLUFD5eIDRabxw7IMiAJjQljh8KHWoc169HiJRO5%2BWCyZML13cTNzMx3WixbevxbYNTp7i0qqvrCBcVT%2BoDcNEZOSxgXEiHdQ0uG7%2FdsQOEWtcggKC0S1YAwa9gErTdvUMBR5sSdO5g4itQvd1q%2B8U6%2FPiKPwPliy97ugxWpQjD02brsSOGBzmTeIGnzZ5UxwzPYBv3wY%2FzqguAride4GmuHHx58PClqrXauvSI4UFuKl7geVUNQOcVL%2FDUxIDzugAOK8tPt5ER5I6kjeCys%2BUVMlQCFORhqZp8Vt4180jbmiRNFSSy2A5sSqRKgm4cjhPoFNNlGpzK%2BVQvCSSw5z5DiOBE22a%2FC%2FPVQpBFubxiZK1DdXnHouE%2BeAnqL1AcZtdKgigrxfHTldlB%2BUK8tUBlF1Kw%2BUD7NUqhXqQ6V%2FGKS7H%2BNtte8nXNRzevxKz5qErqjoOpHoiLyiwkZvuANnEQ61Za1EUsnPXSgquPyGAV6pwVuOv07y9f84f1ErK91e4GWMTeg%2BQpX79dgeKt94ZYjZOhi4ZYuor0XJRIsTk6UF6kEkywlMqNZUFm0QELphDpqBksBDDIzEfrwu4FhC8XjtZz%2FjYm%2BuW9wKzrb77VMvSqkiHtr2RQcUBTY%2FLnFj%2FSGBQM7weaVgatGTD%2FLr8lkviDuDNQW%2FYBgIZFv4HZ%2FVvVsac%2B9TqZl3r17vLdXxcEY5VcJLX038PhoeEpiYCZBratwQnUXQMiKn%2FHT%2FvejieRt0wo7Wj%2BOzY3M0br3HcoW6jXhs0K1R4MH759vuoOSke%2F0zWdhHI6nco9tLw%2FFMqG9m0gdKy665F5XgBy%2F4vzPQu8jJB2vlHa0WxdwGZK0rrCupiRq1tl%2Fu%2Fpxfg0XMx%2F68n4YfXvI%2BpS27MbrI2yUtd9Y6sPN6ommNawB7Y7NVVaJ4XVk14Ke0hIl%2FT1Ywpc0GYqbl3GdU7m5zgVwcqwXldHMGyA63yAme0GTo19Tg6XYN2TsDv17hLdoC5waOxA9RxHzaRz5JL32XUj1mo%2B2eLg7Kf9kBPo98qNE1Aw8%2BHA2zJqBw48xOPd9rPfFtKj2yL5x953p5PO30yk8hjjljR8w0h0j13b8DK0%2BagUzTx1wHET23tu4dMte9B3Z2mnMrKMniJrhNPGm%2B0arlE35yyc87v7o%2FPlmtTJhkZnjrPZU9lO%2F%2F8rD03l6l%2BXU6dVNU4LUYa57SRSkvW73bFBFg%2BOV4nne4nnxuN7z13HXK4JJk7I4dcEA1KMyUbky5S231L2fWYrgrE3RjyuCMMGvrqIex2wItCmuyBG7jiGkb6Y%2FVg6oVDs620oE0%2FJMmWMAza37FQxNpqLQxgoDSkue2gNYA4UW8YxaINfnKkSBunHf%2BekC9tWl3iuWoSBTwxAtLLSIsC9hEkPEIs5Q8XBTXsdE%2B5Vutb1nQdvFbTLDIph4s667rw68D7AxLyYhxn7barceWwXh%2B%2FqqgFBQhnaS1li1usB2Kuk2nUj8RI%2BNtZo5IG2jmgD3Fij124bwMYaz7AEXSZFURO%2F9b%2B2wrQnjZ1iF41iG0YOhYikYkajCbSzUiGbROligx6YjjU9hOPV3cJLuGnh3MwDe2gu2HbrOrBDkrrdN6kXKQJkMvHezLwjNFRFMLDWwrQdlJh1dEZuBh62MtmT8GVJD7%2BbSCnqqYOZ%2Fch69NylGVKIJyTtb%2FLd9e7ChyOaHfh2ebQtWZlNDdTmabBisL0mz1P2jEGfPkOlRcHEASy6xgWXk7klke6m51hDsUW7BPXOaq0D0FZItHsquarN09AFzbA009QtTVNFoyI8DDzoQJ3%2FIRq4q0cWBVNRt7t2mtUbs%2FYcUOU6A0MngbvO1KdstTgZyed1sY%2Fae8VLOyiNjbIedi0%2FoR8u3%2FJkEkfTTQ7KOmXIJF1tAi6fM1xy%2BVh5FSCXT5bq7vw%2BXOQ67tQL3HEY%2BI%2FjZO7FucnH5bOWizlTeo59L05Omp9yR2RzkFyxxmW4i1wxQ8X6n3aULSaZ1rZvBFJKdUHGYqWdpIzBNBqkLxfZAKCsVdKmV7fJ5e5WPelnZ9wazlEwx5eF78bOWm0g0%2BVQqfnJaumUvOY8y4i6vahbyIgUgGpBeEciwsL8a7KEBtjLB1QNvZd8qExvZsYqtXgYlc0XuU%2FzBTwRsQUnxmqrdjTMEFYlzL61THMXzq0byDRuvvjscGTqZB3t5XSA%2B7wM2%2BaFGuxBfQ64h1I1MFFP62QwsNCuaWWKJnYzxhqCSjo3mbGkcTQ8qfLmB8N50qDsYEXyJJbwYYkD8GSbPtGslrs9WbhbnoJbXTBhqX2zRBXMQWoUMf06xsLPV4uwSldJpfA%2BtcMUMB9WjNyKeYCOSI2rKWuBpGK7Rku6rgmiZpqyoslWqkJi7hNq%2BaSBXNeXaNJQOLNcvreJxY4Ddz0Oo3HWuE3IuQFnvfo8nG23ifr%2BFLW8sU8WCFbQB2bzGUBsddvttvudpMkskJs8xj1C3fA2PezENylFMoN%2F4wstxruNerfKIm5mE3psZDxDB4BGMaAMHWa7NwElYRuvT%2FpbQZgk8%2FxjvExvtcntfhPn%2BQjZ4CZx5%2FhhkoD9APvGSRt4Xw3MJ7x%2Feg%2FtKgd1A3sOyQao7RvY3ZzLpeJUUap8bgIthsBGDp3U%2BcHiiKTipLyZ3N0qSTa7yn1M%2F%2Fr015fb9J%2Bzq6sTXqWPvi8qGCa0W5Eyy4zSrCEET8XSO0CY0DYR7dzeOmwWDN2afL8AYA%2F48OXj1Yc2OXXdqAAkiJKxAyTQPd%2FGGdf31OwpjnsqiXJF8loancu3K7NTJ%2BunjydbkVW0D%2BKixg05mLMRlg1g6JZgWVpqcRf%2FUfEUwJ0m7oqTBUl7SlW0qvdl7CLRB7FG2rOJ2pMQUSVTsEp%2FNMyQNJSWYSQJ86yaktQv4GT%2BwXP0vyPzYqe40AbbeA5%2B7kGUcKb1mo3eqJ34oOkwdBsNA5uXeuG7rp%2FHeM45ajrJNEaCuo686hZ7MCNUUgY3sO8p3iJpeG8KqW1agqUQTk6JXZd7mLwssxKG5ckdfYzb7pJxGJfqbEQmDZfizilqLiXa17PLUrj1rq0PU8O05Zmz%2BPp1En2%2B%2BQR1QWDcsEhRlDLrZpvC7cyoaZ14B74zbSerwfoRwUixrW0WTRwV2doFS8%2BbrLVnA9gjKpN8MGwZoFET2N47vUCtCXv0JVQKyr7uDdc4k1%2Fi3nDpYRSGSfn0yF7OP4dOBsy7%2FwM%3D) of the major Classes and Functions (Javascript and Python) 


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

