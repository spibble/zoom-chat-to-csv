# zoom-chat-to-csv
A web tool that takes in a Zoom chat log and spits out a CSV file for easier analysis. This tool is an extended version of an internal one I developed to make tracking lecture attendance & participation easier for remote classes, since for some reason, Zoom does not provide this functionality by default.<sup>1</sup> I figured there's a chance someone else might find it useful.

This app uses vanilla **HTML/CSS** and **TypeScript** for the frontend, and **Python/Flask** for the backend. Hosting is done via **Vercel**. Check it out<sup>2</sup> at https://zoom-chat-to-csv.vercel.app@

If you would like to run this app locally:
  1. Clone the repo: `git clone https://github.com/spibble/zoom-chat-to-csv.git`
  3. Spin up a dev server: `npm run dev`
  4. Once you see `> Ready! Available at [url]` in your terminal, navigate to `url` in your web browser

<sub>1. Actually, [apparently they do](https://www.reddit.com/r/Zoom/comments/10k8og1/exporting_channel_chat_history_to_csv_no_longer/), but it's a total PITA to use</sub>\
<sub>2. Unfortunately, the hosted version of the app doesn't work because of some complications with `tsc` (my best guess). Locally hosting is the only way for now, sorry :P</sub>

## Features
- Takes a `.txt` Zoom chat log and turns it into a `.csv`, with each row corresponding to a different Zoom display name present in chat.
- [Planned] Normalizes usernames by a specified delimiter, or from a set of multiple delimiters.
  - i.e., `Real Name (username)` can be normalized to `username` automatically. Also supports custom delimiters!
- [Planned] Tracks participation points given timestaps.
  - i.e., if a participation question was asked between `11:59:04` and `12:03:57`, then specifying `11:59:04-12:03:57` will automatically award 1 participation point to everyone who sent a message within that time period.
