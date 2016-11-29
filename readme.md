Tiny python script for parsing one CSV file and transforming it into another

Note to self (see comment):

```
{
  "type": "infomart",
  "schema": [
    {
      "Publication": { "rename": "Outlet" },
      "Title": true,
      "Lead": { "rename": "Snippet" },
      "Byline": { "rename": "AuthorName" },
      "Page": false,
      "Length": false,
      "Date": true,
      "Region": true, // we'll need to change to acronyms
      "Media": false,
      "Tone": false,
      "Ad Value": false,
      "Circulation": { "rename": "Followers" },
      "Link": true, // not sure if currently exists, check if null
      "Note": false,
      "Outlet Type": true, // does not currently exist
    }
  ]
}
```
