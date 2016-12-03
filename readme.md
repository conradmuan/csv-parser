Python script that takes a bunch of sysomos and infomart csv data dumps and copies the columns we're interested in into a schema.

This was a personal programming exercise.

## Usage

- place csv data dumps into the `./raw_data` folder
- csv files need to have the word `infomart` or `sysomos` in them to be parsed appropriately
  - you will be prompted if neither word is found in the filename
- run `python csv_parse.py`

## Gothas

- skipped csv files will be recorded in a `skipped.txt` file
- csv files need to be are expected to have the following headers:
  - infomart csv files: `['Publication','Title','Lead','Byline','Page','Length','Date','Region','Media','Tone','Ad Value','Circulation','Link','Note']`
  - sysomos csv files: `["No.","Source","Host","Link","Date(ET)","Time(ET)","time(Eastern Standard Time)","Category","AuthorId","AuthorName","AuthorUrl","Auth","Followers","Following","Age","Gender","Language","Country","Province","City","Location","Sentiment","Title","Snippet","Description","Tags","Contents","View","Comments","Rating","Favourites","Duration","Bio","UniqueId"]`
- The script is **not** smart enough to skip csv files if the headers don't match

## MIT License

Copyright (c) 2016 Conrad Muan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
