Inspired by [Chris Boette](https://newschematic.org/resume/) to generate a smaller index of my favorite blog authors to enable cross-author searching, this is what I've come up with.

In essence, it reads from my selected author's site's list page(s). A little configuration allows me to define how to get the right links off the page. Then I iterate over those links and download their content.

With the content downloaded (a cache mechanism so I don't have to do it on every run), I parse each one for title and content. This is also configured per site.

Finally, I take all that metadata and build a [Lunr index](https://lunrjs.com/guides/index_prebuilding.html). This I serve with chaos-index for my search page to interpret.
