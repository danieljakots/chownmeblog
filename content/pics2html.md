Title: How I accidentally wrote a static site generator
Date: 2020-04-08
Category: Tech

## [Some context first](#context) {: #context }

I bought my
[DSLR](https://en.wikipedia.org/wiki/Digital_single-lens_reflex_camera) at the
end of 2014. I wanted to host the resulting pictures somewhere. I never liked
Flickr much, so I went with 500px. I liked the website and the UI/UX was pretty
nice. The community was pretty cool. Having skilled photographers around is
really valuable, as you can learn and find inspiration. But it might also hurt
(it definitely did, sometimes) to see photographs much better than yours!

For some reason, I kinda stopped photography in 2017. I took a few pictures
here and there but didn't do anything with them. Basically, the cost (i.e. the
time the whole thing took) was way too high for what I felt I got from it
(emotions or whatever).

At the beginning of 2020, I went through all my data on my personal storage
(which included my pictures) to sort and rearrange them. It made me happy to
have all those *souvenirs* and I thought I should really go shoot again.

This narrative is not entirely true, though. ;)

While it did happen, it didn't happen initially. I bought [a case for my
photography
gear](https://dumpster.chown.me/mastodon/media_attachments/files/000/050/759/original/18e91ddf4f0c6ce4.jpeg)
for unrelated reasons (compulsive buying) and thought if I was spending money
on it again, I should make good use of it. Nevertheless, the souvenirs really
nailed my motivation!

Initially, I thought I could keep using 500px but I realized I'd lost my access
and that during my hiatus [they had been
pwned](https://support.500px.com/hc/en-us/articles/360017752493-Security-Issue-February-2019-FAQ).
Now that I have more experience publishing pictures on the Internet, I have a
better idea of what I want and care about. During the ensuing years, I have
also acquired much more experience in [hosting my own
services](./infrastructure-2019.html), which I try to do for everything I use.

## [Looking for some FOSS](#foss) {: #foss }

I thought writing my own would be difficult/time consuming, so I went for doing
what I do best: using existing Free Software. I carefully thought through my
requirements, and here they are:

A quality project is both subjective, and an obvious requirement so I won't
talk more about it. But PHP apps written by someone who wanted to make their
first project?  I'll pass. :)

I really care about showing [EXIF](https://en.wikipedia.org/wiki/Exif) for
pictures. As with software, being able to study how they're made is really
helpful. I feel like pictures without EXIF are as interesting as closed source
software, so I tend to ignore both. (In a photography context, of course. I
won't look at which phone model took that cat picture).

On a side note, surprisingly, I learned that people recently created gallery
software and added machine learning. Well, I've better use for my computing
power and I prefer simpler things.

AND SHOW THOSE DAMN EXIF!

## [Writing my own - the process](#myown) {: #myown }

Sadly, I didn't find anything that met those two simple requirements.

Because of that, I thought I would either write something myself or put the
photos into my blog. I was not very fond of the idea of putting my pictures on
my blog (as a weird application of the "do one thing and do it well" rule), but
even if I were to do so, I wouldn't want to extract the EXIF myself/manually
for each picture.

I began writing a python script which parsed the EXIF, which was kind of funny.
For instance, the library I use gives a tuple for the exposure and depending on
each field's value, [it has a different
meaning](https://github.com/danieljakots/pics2html/blob/c08e2b17476e28e8304bfaadc94f76d77d4c74df/pics2html.py#L62-L74).

I had already used jinja2 in my [uv](https://github.com/danieljakots/uv)
script, so I thought "let's generate a basic html page!" since it was easy.
That was my planned alternative to using my blog. Since I know nothing about
web design/frontend and I wasn't very enthusiastic, I thought maybe I would
later hire someone to do it.

I began to add some very basic CSS to experiment. I had scavenged it from some
random website which had the nice quality of being very simple! I was happy
with the result, so I tried to improve it further. I thought "if I'm stuck or
stop having fun, then I'll look into hiring" which eased my mind a lot!

Surprisingly, I didn't struggle that much and I did have fun!  Tackling one
small issue at a time made it a breeze.

I thought that using icons was better than text since they convey as much
information while being much much shorter. I had bookmarked a [set of
icons](https://github.com/tabler/tabler-icons) (because they're MIT-licensed) a
few days before, thinking "I doubt I'll ever need these, but who knows?" The
set didn't have an icon for the *lens* so I used the *lego* icon.  It looks
similar and it has a smile on it! What's not to love?

During the process, I went to look at how I did stuff with my blog and I
noticed it was a complete mess. Seeing how easy writing a static site generator
was made me want to write one for my blog. So, stay tuned! ;)

## [The result](#result) {: #result }

The result is available here: <https://px.chown.me/>. The [code is, of course,
available](https://github.com/danieljakots/pics2html) as well.

I would not necessarily advise someone to reuse the code as-is (even though you
definitely can since it's Free Software). It's pretty tailored to my needs. For
instance, the red color used is the same as on my [blog](./new-design.html)
(coherency FTW).  I made no effort to make it easily customizable, more than
what I needed to make the code maintainable (up to a certain point, since I
have exactly 0 tests... I already feel my future self's frustration, *oops!*).

That said, if you're thinking about building something similar, you're totally
free (well as long as you abide by the license terms ;)) to study/take parts
from it!

I'm really happy with the result. The code is pretty simple (though some hacks
exist here and there), as you would expect from a less-than-300-line python
script. I learned quite a few things (e.g. improved my skill with jinja2,
discovered that creating a RSS feed is actually not that hard, etc). I'm really
happy with how the website looks. Doing web design is completely out of the
ordinary for me, so it was nice to do something different!

And it's funny... I do things that are 1000x times more complicated, but
generating 200 html files with a single command really feels like magic!
