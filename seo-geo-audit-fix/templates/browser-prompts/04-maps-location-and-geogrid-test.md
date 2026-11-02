# 04 — Maps location, duplicates and geo-grid visibility (read-only)

You are a local-SEO tester working in my real browser. Check how Google Maps and Google Search place and show our office. Read-only; no guessing.

## Our office (as stated on our website)
- Listing name: <listing name> · Listing URL: <maps URL or cid>
- Address: <address incl. building, floor, postcode> · Alternate/legacy address forms: <e.g. lot-number address>
- Geo in JSON-LD: <lat>, <lng> · Phones: <main>, <direct> · Website: <url> · Hours: <hours>
- Known issues to re-check: <list>

## Hard rules
- Read only. If this browser manages the profile, do NOT open the profile manager to edit, click "suggest an edit", claim a listing, post, review or reply.
- One search every 20–30 seconds. On a CAPTCHA or empty results, stop that part and mark the rest NOT VERIFIED.
- Evidence for every claim. State whether results are signed in (manager view) or signed out, and the location Google says it uses.

## Part 1 — Pin, address, building
1. Record: exact name, all categories shown, the full address text, Plus Code, coordinates (from the place record or the share link), phone, website, hours, and claim status.
2. Give the pin's distance from our JSON-LD point in metres, and say whether it sits on the right building.
3. Street View and photos: the building name on the façade or sign, our signage (outside, lobby directory, office door), and the image dates. This decides disputed building names.
4. Search the street address and any alternate address form. Record the building name Google uses and every business at that address.
5. Directions: walking or transit from the nearest stations. Record the route, the exit (if named), the distance and the minutes.

## Part 2 — Conflicting or duplicate listings
1. For the searches "<brand>", "<brand> <service type>" and "<brand> <district>", list every result: name, category, address, phone, website, rating (count), claimed/unclaimed.
2. For each similar-name listing, say:
   - is it ours, another office of the same brand, or a different business?
   - does it use OUR phone or website?
   - does it share our address or Plus Code?
3. For any different business at our exact pin, record everything public, including whether it shows before or after us.

## Part 3 — Geo-grid (Maps visibility from different places)
Use URLs of the form `https://www.google.com/maps/search/QUERY/@LAT,LNG,14z` and do not drag the map. (The skill's `scripts/geo_grid.py plan` can generate them.)

Centres:

| Code | Area | Lat, Lng |
|---|---|---|
| A | office | <lat>, <lng> |
| B | <nearby district> | … |
| C–H | <other districts, court area, transit hub, neighbouring city> | … |

Queries:
- <service provider>
- <firm type>
- <service 1> <provider>
- <service 2> <provider>
- <service 3> <provider>

For each search, record:
- our position (count organic results only, ads skipped; up to 20; "20+" if absent);
- the top 3 with category and rating (count);
- other same-brand offices and their positions.

Output a grid table (rows = queries, columns = centres). If rate-limited, do centres A, C and D first.

## Part 4 — Search map pack
For 5–6 head queries (`https://www.google.com/search?q=QUERY&gl=<cc>&hl=<lang>&pws=0`):
- is there a map pack (3-pack)? Its 3 listings;
- are we in it or under "More places", and at what position?
- does our knowledge panel appear for the brand query, and what does it show?

## Part 5 — The listings that beat us
For the 5 listings most often in the top 3, record:
- primary category;
- hours filled;
- description;
- services;
- photo count;
- review count and rating;
- owner-reply share (sample of 10);
- latest post;
- website;
- keywords stuffed in the business name.

Do the same for ours and compare. Note any platform-rule violations by competitors (keyword-stuffed names, false "Open 24 hours"); do not recommend copying them.

## Output
1. 5-line summary.
2. Part 1 table: Field | Google | Website | Match? | Evidence, plus the pin distance, building-name evidence and directions.
3. Part 2 listings table with conflict notes.
4. Part 3 grid and top competitors.
5. Part 4 map-pack table.
6. Part 5 comparison table.
7. Fixes by impact: problem + evidence, exact fix, who does it (profile owner / website code / other business owner). No fake reviews, no keyword stuffing, no false hours.
8. A short summary in the owner's language.
9. NOT VERIFIED list.
