# Photographs from open archives

Read this when the brief's Imagery line is photography and nobody supplied any. Supplied photographs always come first; this is how to find real ones instead of building a stand-in, and how to credit them so the page can ship.

## What an archive photograph may show

An archive photograph was taken by someone else, of somewhere else, unless it shows the place the subject names. That decides where it can go.

- **The subject's own place** (the street, the river, the building, the town the brief names): true of the client, so it can carry the first screen. Check the photograph shows that place, not one with the same name.
- **The subject's world** (the ingredient, the craft, the landscape, the species, the tools): not the client's, so it takes a supporting position, at most one large image per section. Never caption it, describe it or set copy beside it so that it reads as the client's dish, room, staff, volunteers or product.
- **Never**: a recognisable person (on Commons, a `Restrictions` value of `personality` flags one), a logo or a brand's product, a watermark, a photograph presented as evidence of something the subject did, or a rendered or AI-generated image.

"No external images" means no image loaded from another host at runtime. A photograph downloaded into the build and credited meets it, so that wording is not a reason to skip the search. State this reading in the report as an assumption to confirm. Only a brief that rules out photographs, stock or archive imagery by name rules these out.

## Licences

Use only licences that allow commercial use and changes: public domain (including the Public Domain Mark), CC0, CC BY and CC BY-SA, any version. Never use NC (a client's site is commercial), ND (a crop or grade is a change), "all rights reserved", "fair use", or a licence you cannot name. The licence counts only when the source's own page confirms it: Commons states it on the file's description page, and an Openverse result is confirmed on its `foreign_landing_url`. If it cannot be confirmed, do not use the photograph.

## Search

Write search terms URL-encoded (`%20` for a space). Send a User-Agent naming the client and its purpose, such as `web-ui-craft-build/1.0 (page build)`: Wikimedia refuses a missing or generic one with HTTP 403. Give each request a 20 s timeout, and stop after six searches in total: whatever has been found by then is the set.

1. **Wikimedia Commons**, first for named places. Search the file namespace with a width floor (1,800 px for a first-screen image, 1,200 px for a supporting one):

   ```
   curl -s -m 20 -A "<user agent>" "https://commons.wikimedia.org/w/api.php?action=query&format=json&formatversion=2&generator=search&gsrnamespace=6&gsrlimit=10&gsrsearch=filetype:bitmap%20filew:%3E1800%20<terms>&prop=imageinfo&iiprop=url|size|extmetadata&iiextmetadatafilter=ObjectName|Artist|LicenseShortName|LicenseUrl|Restrictions&iiurlwidth=1920"
   ```

   Each result gives the licence (`LicenseShortName`, `LicenseUrl`), the author (`Artist`, HTML: credit the person named there, not the uploader), the title, `descriptionurl` (the page to credit and to confirm the licence on) and `thumburl` (a copy scaled to about `iiurlwidth`; Commons may return a larger standard size).

2. **Openverse**, for things rather than places. It indexes Flickr and other sites:

   ```
   curl -s -m 20 -A "<user agent>" "https://api.openverse.org/v1/images/?q=<terms>&license=cc0,pdm,by,by-sa&page_size=20"
   ```

   Each result gives `title`, `creator`, `license`, `license_version`, `license_url`, `foreign_landing_url` and `url`. Short queries in plain nouns work best; a narrow phrase often returns nothing.

Open the shortlisted images and look at them before choosing: the subject, the light, the crop the layout needs, and anything on the never list above. Three or four photographs are usually enough; past five the set stops reading as one voice.

## Into the build

- **Download, never hotlink.** Save each file into the build's own folder (for example `img/`) with a name that says what it shows, and point the markup there. A hotlinked image can vanish, change or track visitors.
- **Size for the slot.** Download the scaled copy, not the original: about 1,920 px wide for a full-width image and half that for a supporting one, with a second copy near 800 px for phones in `srcset`. Set `width` and `height`, give the first-screen image `fetchpriority="high"`, and lazy-load the rest.
- **One treatment** for the whole set, as `references/visual-system.md` describes, drawn from the palette: a grade, a duotone, a shared crop ratio or grain. Archive photographs come from different cameras and years, and the treatment is what makes them one set.
- **Alt text written new** for this page. The archive's title describes the photographer's day, not what the image does here.

## Credits

Credit every photograph on the page itself, with its title, author, source and licence, each linked: title to the source page, licence to its deed. A credits section in the footer, or a credits page linked from the footer, is enough for a page with several. When the page changes the image beyond a crop (a grade, a duotone, a mask), the credit says "adapted from". A CC BY-SA photograph that was changed stays under CC BY-SA; the rest of the page does not.

```
Photographs: "<title>" by <author>, <source>, <licence>[, adapted]; ...
```

## When nothing usable comes back

No archive reachable, every result too small, every licence unconfirmed, or nothing on the subject after six searches: build the hero in code with `references/artefacts.md`, and say in the report which searches ran and why nothing was used. A weak photograph is worse than a strong drawing.

## Report

Add a line to the report:

```
Photographs:  each one used, its licence and where it is credited; or why none were used
```
