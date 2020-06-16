Title: Improvements to this blog
Date: 2020-06-16
Category: Tech

This article announces a new version of this blog. Available right now!

In my [previous article](./pics2html), I said that "seeing how easy writing a
static site generator was made me want to write one for my blog," and that's
what I did! I initially wrote a very long article to tell the whole story, but
then I decided I didn't want to have such a long article here. Here's a short
version.

Basically, I used a small subset of all the features pelican provides. Writing
my own software gives me more control. However, with great power comes great
ownership of the code, since I doubt anyone else is going to touch my code. But
I like it.

Here's a short list of the changes:

* Cleaner and much simpler CSS.
* Related to the previous point, the text is always centered. It was not
  exactly easy to achieve this, hence the joke in the footer.
* HTML headers (like h2 and h3) have now HTML anchors to make it easy to share
  specific parts of a post.
* No more sharing buttons. I doubt they were used (but what do I know?) and
  copying and pasting a link is not that hard. Less clutter on the interface,
so it's an improvement.
* I have a contact page. I hope it will make the experience better for
  everyone.
* No breakage. I was careful to keep the same link for most things. Please let
  me know if you notice otherwise!
* [Clean URL](https://en.wikipedia.org/wiki/Clean_URL). But to keep everything
  working as before, all pages will be reachable with the .html extension as
  well.
* New pygment style (for inline code), which I think is nicer.
