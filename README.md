<!--
  ╔═══════════════════════════════════════════════════════════════════════╗
  ║  SETUP REMINDER (17 Jan 2026)                                         ║
  ╠═══════════════════════════════════════════════════════════════════════╣
  ║  This is the PUBLIC blog repo, auto-deployed to GitHub Pages.         ║
  ║                                                                       ║
  ║  WORKFLOW:                                                            ║
  ║  1. Edit posts in: ~/Documents/ObsidianVault/crw-notes-raw-GIT/BLOG/  ║
  ║  2. Commit there → post-commit hook auto-syncs here & pushes          ║
  ║  3. GitHub Pages rebuilds (~1 min)                                    ║
  ║                                                                       ║
  ║  LOCALHOST TESTING:                                                   ║
  ║  cd ~/Programming/LocalhostBlog && ./serve-direct.sh                  ║
  ║  → http://localhost:4000/crw-blog/                                    ║
  ║                                                                       ║
  ║  If you edit THIS repo directly, sync back to the private repo!       ║
  ╚═══════════════════════════════════════════════════════════════════════╝
-->

<header>

<!--
  <<< Author notes: Course header >>>
  Include a 1280×640 image, course title in sentence case, and a concise description in emphasis.
  In your repository settings: enable template repository, add your 1280×640 social image, auto delete head branches.
  Add your open source license, GitHub uses MIT license.
-->

# Fruit of Preterition Blog

## Local Development Workflow (GitHub-Compatible)

- **Install dependencies:**
  ```bash
  bundle install --path vendor/bundle
  ```
- **Start local server (identical to GitHub Pages):**
  ```bash
  bundle exec jekyll serve --config _config.yml,_config.local.yml
  ```
  Or use the helper script:
  ```bash
  ./dev-server.sh start
  ```
- **Stop server:**
  ```bash
  ./dev-server.sh stop
  ```
- **Edit posts in `_posts/`, preview at [http://localhost:4000/crw-blog/](http://localhost:4000/crw-blog/)**
- **For local-only settings (like live reload), use `_config.local.yml`** (ignored by GitHub Pages)
- **All dependencies are locked to GitHub Pages via the `github-pages` gem in the Gemfile.**

See `DEVELOPMENT.md` for full details, troubleshooting, and explanations.

---

## Adding Images to the Blog

Place image files under the `assets/images/` folder so Jekyll will copy them into the site output. Example path in the repo:

```
assets/images/my-photo.jpg
```

Examples of how to reference images in posts and pages:

- Markdown (recommended):

```markdown
![Alt text]({{ '/assets/images/my-photo.jpg' | relative_url }})
```

- HTML (with caption):

```html
<figure class="post-figure">
  <img src="{{ '/assets/images/my-photo.jpg' | relative_url }}" alt="Descriptive alt" class="responsive-img">
  <figcaption>Figure 1 — A short caption.</figcaption>
</figure>
```

- Featured image via front matter (add to a post):

```yaml
---
layout: default
title: Example Post
image: /assets/images/featured.jpg
---
```

Then add this snippet to your layout (example already available in many themes):

```liquid
{% raw %}{% if page.image %}
  <div class="post-featured">
    <img src="{{ page.image | relative_url }}" alt="{{ page.title }}">
  </div>
{% endif %}{% endraw %}
```

Tips:
- Optimize images before committing (resize/compress) for faster loads.
- Use `git lfs` for very large assets (>100 MB).
- Always include `alt` text for accessibility.


# Original README content below

# GitHub Pages

_Create a site or blog from your GitHub repositories with GitHub Pages._

</header>

<!--
  <<< Author notes: Finish >>>
  Review what we learned, ask for feedback, provide next steps.
-->

## Finish

_Congratulations friend, you've completed this course!_

<img src=https://octodex.github.com/images/constructocat2.jpg alt=celebrate width=300 align=right>

Your blog is now live and has been deployed!

Here's a recap of all the tasks you've accomplished in your repository:

- You enabled GitHub Pages.
- You selected a theme using the config file.
- You learned about proper directory format and file naming conventions in Jekyll.
- You created your first blog post with Jekyll!

### What's next?

- Keep working on your GitHub Pages site... we love seeing what you come up with!
- We'd love to hear what you thought of this course [in our discussion board](https://github.com/orgs/skills/discussions/categories/github-pages).
- [Take another GitHub Skills course](https://github.com/skills).
- [Read the GitHub Getting Started docs](https://docs.github.com/en/get-started).
- To find projects to contribute to, check out [GitHub Explore](https://github.com/explore).

<footer>

<!--
  <<< Author notes: Footer >>>
  Add a link to get support, GitHub status page, code of conduct, license link.
-->




---

Get help: [Post in our discussion board](https://github.com/orgs/skills/discussions/categories/github-pages) &bull; [Review the GitHub status page](https://www.githubstatus.com/)

&copy; 2023 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

</footer>
