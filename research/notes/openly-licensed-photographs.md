# Openly licensed photographs for pages built without supplied images

Scope note: gathered on 24 November 2026 for the rule in `skills/web-ui-craft/references/photographs.md`. The idea of finding real photographs in open archives and crediting them comes from Taste Skill (github.com/Leonxlnx/taste-skill, MIT); it is restated here in our own words, and no text is copied. The two archive APIs were queried from the build machine on the same day to confirm they answer and what their records hold.

## Q1. Which archives can a builder search, and what does each record say about its licence?

### Takeaway
Wikimedia Commons and Openverse both answer anonymous searches and return a machine-readable licence with each result. Commons is strongest for real places (streets, rivers, buildings), because its contributors photograph them by name; Openverse adds breadth from Flickr. Neither guarantees the licence it reports, so the licence is confirmed on the source's own page before use.

### Cited findings
- Commons search through the MediaWiki API, `generator=search` in the file namespace with `prop=imageinfo&iiprop=url|size|extmetadata`, returns per file `LicenseShortName` (for example `CC BY-SA 2.0`), `LicenseUrl`, `Artist`, `Credit`, `ObjectName`, `AttributionRequired` and `Restrictions`: queried 24 November 2026 for "River Don Sheffield" and "pintxos".
- The search syntax accepts a width filter: `filetype:bitmap filew:>1800 River Don Sheffield` returned five photographs 1,888 to 5,010 px wide, all CC BY-SA 2.0. Without the filter, the top three were 800 to 1,280 px wide: queried 24 November 2026.
- `iiurlwidth` returns "a URL to an image scaled to this width", and "no more than 50 scaled images will be returned" when it is used; the scaled image may be wider than requested: [MediaWiki, API:Imageinfo](https://www.mediawiki.org/wiki/API:Imageinfo). A request for 1,600 px returned a 1,920 px thumbnail on 24 November 2026.
- `iiprop=extmetadata` "is an expensive property to request, and should be avoided unless you need it": [MediaWiki, API:Imageinfo](https://www.mediawiki.org/wiki/API:Imageinfo).
- Commons: "Each media file has its licensing specified on its file description page", reusers should "Confirm that the file is available under license terms that suit you", and the Foundation "does not provide any warranty regarding the copyright status": [Commons, Reusing content outside Wikimedia](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia).
- Commons: "Directly using a Commons file via embedding its URL ("hotlinking") is also possible, but is not recommended": [Commons, Reusing content outside Wikimedia](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia).
- Wikimedia sites "require a HTTP User-Agent header for all requests", and "if you don't supply a User-Agent header, or you supply an empty or generic one, your request will fail with an HTTP 403 error"; generic agents such as "curl" are named: [Wikimedia Foundation, User-Agent policy](https://foundation.wikimedia.org/wiki/Policy:User-Agent_policy).
- Openverse's image search, `GET https://api.openverse.org/v1/images/?q=...`, filters by `license` ("`by`, `by-nc`, `by-nc-nd`, `by-nc-sa`, `by-nd`, `by-sa`, `cc0`, `nc-sampling+`, `pdm`, and `sampling+`") and by `license_type` ("`all`, `all-cc`, `commercial`, and `modification`"); `q` "should not exceed 200 characters": [Openverse API schema](https://api.openverse.org/v1/schema/), fetched 24 November 2026.
- Each Openverse result carries `license`, `license_version`, `license_url`, `creator`, `title`, `foreign_landing_url` and the image `url`: queried 24 November 2026 for "river litter volunteers", 240 results, the first a Flickr photograph under CC BY 2.0. The same query style returned no results for "grilled fish charcoal" with `license_type=commercial,modification`, so a narrow query can come back empty.
- Openverse says page size is "subject to limitations based on authentication and access level", and that an unverified application has "the same rate limits as an anonymous user"; no anonymous figure is published: [Openverse API schema](https://api.openverse.org/v1/schema/).

### Inferences
- Search Commons first for the place the subject names, with a width filter, then Openverse for things rather than places. Ask Openverse for `license=cc0,pdm,by,by-sa` rather than `license_type`, so the filter names exactly the licences the rule allows.
- Openverse indexes other sites, so its licence is a pointer: the landing page decides. A licence that cannot be confirmed there is not used.

### Gaps
- No published anonymous rate limit for Openverse; the rule bounds the number of searches instead.
- Openverse's statement on licence accuracy was not readable (its about page returned 403).

## Q2. Which licences suit a client's site, and what must the credit hold?

### Takeaway
Public domain, CC0, CC BY and CC BY-SA allow commercial use and modification. NC rules out a commercial site and ND rules out a crop or grade. A credit names title, author, source and licence, may sit on a credits section or page, and says when the image was changed.

### Cited findings
- CC recommends that attribution "include the Title, Author, Source, and License", and that "This is true whether you're sharing the work as-is or if you have made an adaptation"; its example credits an adaptation as "adapted from" the original: [Creative Commons, Recommended practices for attribution](https://wiki.creativecommons.org/wiki/Recommended_practices_for_attribution).
- Attribution may be given "in any reasonable manner based on the medium, means and context in which the Licensed Material is used", and for images "consider publishing a web page with attribution information": [Creative Commons, Recommended practices for attribution](https://wiki.creativecommons.org/wiki/Recommended_practices_for_attribution).
- NC: "You may not use the material for commercial purposes": [CC BY-NC 4.0 deed](https://creativecommons.org/licenses/by-nc/4.0/deed.en). ND: "If you remix, transform, or build upon the material, you may not distribute the modified material": [CC BY-ND 4.0 deed](https://creativecommons.org/licenses/by-nd/4.0/deed.en).
- BY-SA: "If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original": [CC BY-SA 4.0 deed](https://creativecommons.org/licenses/by-sa/4.0/deed.en). The CC FAQ, as summarised by the fetch tool rather than quoted, says that combining works without adapting them leaves each under its own licence: [Creative Commons FAQ](https://creativecommons.org/faq/).
- Commons: "If the uploader is not the content creator, it is the content creator who must be credited, not the uploader": [Commons, Reusing content outside Wikimedia](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia).

### Inferences
- A page that shows a BY-SA photograph does not put the page under BY-SA; a graded or cropped copy of the photograph is the part that stays BY-SA, so its credit names the licence and says it was adapted.
- The `Restrictions` field on Commons flags personality rights. A recognisable person on a business's page reads as an endorsement they never gave, so such photographs are left out.

## Q3. How does Taste Skill use archive photographs?

### Takeaway
Taste Skill downloads vetted Commons and Unsplash photographs into the build, keeps stock of another place to small detail positions, writes new alt text and credits the sources in one footer line with a full credits page.

### Cited findings
- "The photographs are real, found in open archives and credited by the skill": [Taste Skill README](https://github.com/Leonxlnx/taste-skill).
- Live search asks Commons for "JPEG, 1600 px wide or more; CC0, CC BY, CC BY-SA or public domain"; library frames "are stock of another place, so they fill detail slots only"; files are written into the build's `assets/img/`; alt text is written new because "the file's title names someone else's place": [Taste Skill, references/photos.md](https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/references/photos.md), read 24 November 2026; commit not recorded.
- It rules out "Stock photographs passed off as the client's product, people or place": [Taste Skill, SKILL.md](https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md).

### Inferences
- The distinction that matters is between a photograph of the place the subject names (the street, the river) and a photograph of a thing like the client's (a dish, a volunteer). The first is true of the client and can carry the first screen; the second is not the client's and belongs in a supporting position, never captioned or described as theirs.
- Taste Skill's footer credits name only the sources. CC's guidance asks for title, author and licence too, so the rule here credits each photograph in full.
