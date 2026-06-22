Milywan Education Auto-Posting Starter v3

What this includes:
- posts.json: 30 carousel posts
- /posts/day_01 ... /posts/day_30: pre-generated JPG carousel images
- post_to_instagram.py: publishes a 5-image carousel to Instagram using Meta Graph API
- .github/workflows/daily-instagram.yml: GitHub Actions workflow for daily posting
- create_images.py: regenerates carousel images if you edit posts.json

Important:
- This version uses GitHub Pages for image hosting.
- It does NOT use Cloudinary.
- It posts to Instagram first. Facebook cross-posting can be added after Instagram works reliably.
- Your META_ACCESS_TOKEN may expire. Update the GitHub Secret when needed.

Required GitHub Secrets:
- META_ACCESS_TOKEN
- INSTAGRAM_BUSINESS_ACCOUNT_ID
- FACEBOOK_PAGE_ID

GitHub Pages base URL used:
https://tanxzero.github.io/milywan-auto-posts

To test manually:
1. Upload all files to your repo.
2. Go to Actions → Daily Instagram Carousel.
3. Click Run workflow.
4. Optional: enter post_id like day_01.
