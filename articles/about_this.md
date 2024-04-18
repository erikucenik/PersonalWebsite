---
title: About this website.
subtitle: And its creation.
---

I think having a website is pretty much a requirement for the modern world. Not as a technical display nor to get to be known, but rather as an index for your identity. I know perfectly well who I am and what I do and people around me also know, but if a stranger were to get interested in me, he wouldn't be able to find much if not for this website.

I encourage you to make your own website, it doesn't matter whether you do it with a WCMS and self host it in a Raspberry Pi or set up a sophisticated system. As long as I can type your full name and find what you've done, it's fine. If it serves as inspiration, I'll tell you how I made this website.

# The Design

Look, I've never been a good artist, I still draw like a toddler and design isn't my best. To illustrate this point, here's a website I made some years ago that I may or may not plan to bury forever.

![*An actual site I hosted.*](/static/articles_media/about_this/old_site.png)

However I think anyone can make a half decent product by applying some principles:

1. First: less is more. Look at the abomination above. You start adding gradients, rounded corners and complex colorschemes and you end up with a *collage* of horror. Now look at this very page. About 70% of it is just black text over a white background. Look at Apple's design, it tends to be simple yet crystal clear. That's what I mean by "less is more". You might be tempted to use every technique you learned in that Photoshop course, but it's not really necessary.
2. Second: think about or improvise the **general** aesthetics of your design and then make a few sketches using plain old pencil and paper. I say this because when using a program like Figma or Photoshop we tend to want perfect mathematical relationships between the size of buttons and their border radius, or the exact hex value of the color we are picking for a header, or obsess about snapping every element to a grid. This is all important, of course (except the hex value thing. Just pick a color and use it consistently), but it undernimes what you are actually trying to do: coming up with a design.
3. Third: patterns and repetition. School has taught us that more work equals better results. Nothing further from truth. Have something that works perfectly? Great! Use it. This is not project to grade, more complexity won't yield a better outcome.

Once you apply these principles, you'll also understand the languages that control frontend's look: HTML and CSS. Your mind will be accustomed to thinking in terms of containers and variables. Give it a try and you'll understand these words. Designing a website using raw HTML/CSS is something I'll never repeat.

If you want to get a hint of how I came up with the design language for this site, check out its [design files repo.](https://github.com/erikucenik/PersonalWebsiteDesign) Just to be clear, I'm not trying to say how things should be done, these are just some behavioural patterns I've come across when trying to make designs.

# The Brains

So I wasn't lying with the self hosting thing. This site is currently running on a Raspberry Pi 4 about 40 centimeters away from my elbow. I know the traffic on this thing isn't going to be immense, in the end it's just a bunch of articles, so the little guy does just fine.

![The host of what you're seeing right now.](/static/articles_media/about_this/rpi.png)

It consists on a [FastAPI](https://fastapi.tiangolo.com/) backend which uses [Jinja Templates](https://jinja.palletsprojects.com/en/3.1.x/) and converts articles in Markdown format into actual HTML using [Pandoc](https://pandoc.org/) and a bit of my own code. You can actually find it in [this site's repo](https://github.com/erikucenik/PersonalWebsite). It's pretty simple, and so is the site. I learned the hard way to not overcomplicate things (looking at you, **Django**).

I've set up [NGINX](https://www.nginx.com/) as a reverse proxy to [Gunicorn](https://gunicorn.org/), and to open the site to the public I've set a port forwarding rule on my personal router. [Certbot](https://certbot.eff.org/) is set up for HTTPS, and as an extra layer there's [Cloudflare](https://www.cloudflare.com/), which I've set up to route HTTPS connections as well as SSH.

I used cloudflare both as a [DNS](https://en.wikipedia.org/wiki/Domain_Name_System) and to solve the problem with static IPs. See, my personal router provides me with a dynamic public IP address, this means that it changes. I didn't want to update the DNS record every time that happened, so I set up Cloudflare and [a script to update it automatically](https://github.com/K0p1-Git/cloudflare-ddns-updater). In my Raspberry Pi, it just runs periodically without me looking thanks to [Cron](https://en.wikipedia.org/wiki/Cron). I also used Cloudflare to route emails from [contact@erikucenik.com](mailto:contact@erikucenik.com) to other addresses. Pretty fancy.

I think everything is perfectly secure. If you wan't to try and prove me wrong, go ahead! Just please don't steal anything important if you actually manage to do it.

I don't know how to end this article. Bye.

*15/04/2024*
