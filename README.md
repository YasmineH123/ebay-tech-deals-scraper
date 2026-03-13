*Summary:*

This project builds a complete data pipeline that automatically scrapes tech product deals from eBay, stores the data every 3 hours, cleans it, and analyzes it with charts and visualizations. 

By that we practice real web scraping, automation, data cleaning, and exploratory data analysis in one project.

*Key Findings:*

- Apple and Samsung were the most frequently appearing brands in the listings
- Most products were priced under $200, but only some high-end items pushed the average up
- The majority of discounts were between 40% amd 60%.
- Most of items had no shipping information

*Challenges Faced*

1. Empty CSV error on the first GitHub Actions run
The CSV file existed in the repository but was empty at first. I fixed this by adding a check for the file size before trying to read it "for the scraper not crash" if the file is empty, treat it like it doesn't exist and write a fresh one with the header.

2. Shipping values disappearing after cleaning
After running the cleaning script, the entire shipping column turned blank. The issue was that pandas reads empty cells in a CSV as NaN, not as empty strings. My replacement logic was only checking for empty strings, so it was silently skipping all the NaN values. I fixed it by adding a fillna() call before the string replacements.

3. GitHub Actions YAML configuration
Writing the workflow file was probably the most frustrating part. YAML is very strict about indentation, one wrong space and the whole workflow breaks with a confusing error. I had to rewrite and debug the file several times before it worked correctly. And what should I write even was confusing.

*Key things I learned:* permissions need to be set to contents: write for the script to push back to the repo, and the git pull before git push is necessary to avoid conflicts.

*Potential Improvements*

- Track individual product prices over time to see how deals change
- Add more keywords or use NLP techniques for deeper title analysis