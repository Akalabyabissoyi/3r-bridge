# Privacy and data governance

- 3R Bridge stores **nothing** you type: no database, no accounts, no analytics (`gatherUsageStats = false`). Entries live in your
  browser session and are gone when you close the tab. Exports (Markdown, Word, JSON) are generated on the fly and downloaded to your device.
- Do not enter identifiable personal data or confidential study details into a **shared public deployment**. Run it locally or
  in your institution's own deployment (see docs/DEPLOY.md) for sensitive projects.
- The app page loads two fonts from Google Fonts, so a request goes to Google when the page opens. To avoid that,
  self-host the fonts by editing the `@import` in `bridge/ui.py`.
- Hosting platforms (Streamlit Community Cloud, Hugging Face) keep their own server logs.
- The exported JSON contains only what you entered plus the catalogue content.
