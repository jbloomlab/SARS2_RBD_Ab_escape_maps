# Webpage served through GitHub Pages

The webpage hosting the interactive visualizations is rendered through [GitHub pages](https://pages.github.com/) from this `./docs/` subdirectory of the main branch.
The repo was configured to do this using the options on the GitHub site for the repo.
This subdirectory contains the content for [GitHub pages](https://pages.github.com/).

## How the contents of this directory were built

### Basic setup

All of this was done on a Mac.

First, used [brew](https://brew.sh/) to install [ruby](https://www.ruby-lang.org/en/) with:

    brew install ruby

and added ruby to the PATH:

    echo 'export PATH="/usr/local/opt/ruby/bin:$PATH"' >> /Users/jbloom/.bashrc

Then installed [bundler](https://bundler.io/) and [jekyll](https://jekyllrb.com/) with:

    gem install --user-install bundler jekyll

Added the local install directory to PATH with:

    echo 'export PATH="$HOME/.gem/ruby/3.0.0/bin:$PATH"' >> ~/.bashrc

(Note that above is for ruby version 3.0, command would need to be different for a different ruby version.)

Then followed the [GitHub Pages instructions here](https://docs.github.com/en/github/working-with-github-pages/creating-a-github-pages-site-with-jekyll).
Navigated into this `./docs/` subdirectory and ran:

    jekyll new .

As described in the [GitHub Pages instructions here](https://docs.github.com/en/github/working-with-github-pages/creating-a-github-pages-site-with-jekyll), commented out the line in [Gemfile](Gemfile) beginning `gem "jekyll"`.
Also uncommented out the line beginning `# gem "github-pages"` to make it read:

    gem "github-pages", "~> 213", group: :jekyll_plugins

where the `213` represents the latest `github-pages` gem as determined by looking [here](https://pages.github.com/versions/).

Then also ran: 

    bundle add webrick

to fix the issue [described here](https://github.com/jekyll/jekyll/issues/8523).

Finally, ran:

    bundle update

### Editing content
Then make the following manual edits to create the content:

 - Edited [_config.yml](_config.yml] in various ways to better reflect this project.

 - Copied [_layouts/default.html](__layouts/default.html) from the [equivalent file from the RBD DMS repo](https://github.com/jbloomlab/SARS-CoV-2-RBD_DMS/blob/master/docs/_layouts/default.html) created by Sarah Hilton. Then edited this file to load the interactive chart and put the content in [index.md](index.md) below the chart.

 - Edited [index.md](index.md) to refer to the *default* style and have the appropriate content. Note that the citations are automatically added by the top-level processing script in the main repo.

 - Created the [escape-calc.md](escape-calc.md) file and its style to implement and document the escape calculator.


### Previewing GitHub Pages webpage
Assuming the above software is installed, simply do:

    bundle exec jekyll serve

and then open `http://127.0.0.1:4000/` in a web browser.

## Google analytics
Google analytics were set up [as described here](https://desiredpersona.com/google-analytics-jekyll/).
