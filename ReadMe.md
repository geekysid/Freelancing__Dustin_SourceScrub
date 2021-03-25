<p align="center">
    <img src="https://user-images.githubusercontent.com/59141234/93002341-ff261d00-f553-11ea-874d-19ab5cb1068f.png" height="70px" />
</p>
<h4 align="center">
    SOURCESCRUB Scraper
</h4>
<p align="center">
    Scraper to fetch details of companies from SourceScrub.com
    <br />
    <a href="https://www.upwork.com/ab/f/contracts/26640552">
        Project Contract
    </a>
    &nbsp;&nbsp;·&nbsp;&nbsp;
    <a href="#">
        Client - Dustin Johnson
    </a>
    &nbsp;&nbsp;·&nbsp;&nbsp;
    <a href="#">
        Status - Completed
    </a>
</p>

<br />

<!-- Details of Content -->

## Table of contents

- [Prerequisite](#Prerequisite)
- [Unpacking](#Unpacking)
- [Installation Dependencies](#Installation-Dependencies)
- [Understanding Project File](#Understanding-Project-File)
- [Running The Script](#Running-The-Script)
- [Show Your Support](#Show-Your-Support)
- [Contact Me](#Contact-Me)

<br />

<!-- Prerequisite -->

## Prerequisite

    - Windows
    - Python 3.6 or above
    - Chrome Webdriver

[Install Python on Windows 10](https://phoenixnap.com/kb/how-to-install-python-3-windows)

[Get Chrome WebDriver according to your Google Chrome Version](https://chromedriver.chromium.org/downloads)

<br />

<!-- Unpacking -->

## Unpacking

- Unzip the SourceScrub*Scrapper.zip in desired location. Let's assume that we unzip the file in location \_E:\SourceScrub*
- After this the path of the Project lookes like _E:\SourceScrub_
- The project folder should look something like this:

![SourceScrub](https://user-images.githubusercontent.com/59141234/112516943-cc3fca00-8dbd-11eb-922c-ee925ca91ee7.png)

<br />

<!-- Instalation -->

## Installation Dependencies

- Start terminal and type below command in terminal to point to the project folder:

```
~$ E:\
~$ cd SourceScrub
```

- Now we need to download all the dependencies required to run the script. For this we will type below command in terminal:

```
~$ pip3 install -r requirements.txt
```

<br />

<!-- Understanding File -->

## Understanding Project File

#### requirement.txt ⛔

This file contains all the dependencies that we need to install on our system. You can delete this file but its Ok to keep it there and forget that it exists.

#### script.py 🚫

This file is the main script that we need to run to get the desired output. **Please never touch this file**.

#### config.json ✍️

This file needs to be edited everytime you run the script and so it needs some explation...

- **path_to_chromedriver** => Path where the chrome webdriver executeable file is located. Take care of the _Double Black Slash_.

- **starting_pont** => URL which script should open when initiated.

- **sleep_time** => List of two integer, represents time for which the script should sleep between each hit to the server.

<br />

<!-- Running the script -->

## Running The Script

So before running the script please make sure of two things:

- You have edited the config file properly.
- The pointer in terminal is pointing to the project forlder. If not then use below code:

```
~$ E:\
~$ cd SourceScrub
```

Now we need to enter below code to execute the script.

```
~$ python3 script.py
```

Now just grab yourself a pint of 🍺 and let the script do its task.

<br />

<!-- Asking for Supports -->

## Show Your Support

If you are happy with my work then please give me :star::star::star::star::star: rating and also leave really nice recommendation/feedback on upwork. This will help me a lot in getting more project. A small and happy bonus is always appreciated 🤩. Also kindly rememeber me if you have any such project or any scraping projects. <p />Thank You for giving me opportunity to work on this project.

<br />

<!-- Displaying message about me -->

## Contact Me

**Siddhant Shah** - Please feel free to connect to me in case there is any issue in the script or any changes are required. You can contact on below mentioned connects

> [Website](https://gist.github.com/siddhantshah1986 "My Website") > &emsp;&emsp; > [Mail Me](mailto:siddhant.shah.1986@gmail.com "siddhant.shah.1986@gmail.com") > &emsp;&emsp; > [UpWork](https://www.upwork.com/fl/geekysid "Upwork") > &emsp;&emsp; > [Instagram](https://www.instagram.com/siddhantshah39 "Instagram") > &emsp;&emsp; > [WhatsApp](https://api.whatsapp.com/send?phone=+918584852091 "WhatsApp")
