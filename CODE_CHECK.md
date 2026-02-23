# Code Check: Discord → Image Processing → Etsy Automation Script

## High-priority issues

1. **Hardcoded secrets and credentials**
   - API keys, OAuth client secrets, usernames, passwords, and tokens are embedded directly in code.
   - This is a critical security risk and can lead to account compromise.

2. **Script duplicated almost entirely**
   - The full script appears repeated, which makes maintenance error-prone and can cause accidental double execution when pasted/run.

3. **Global variable coupling / undefined references**
   - Several functions depend on globals (`first_line`, `the_folder`, `title`) rather than arguments.
   - `retrieve_first_url()` references `response` in an error path where `response` is never defined.

4. **Fragile browser automation**
   - Extensive use of absolute XPaths and fixed `time.sleep(...)` delays is brittle against UI changes and timing variance.

5. **No robust error handling / retries**
   - Network calls and API responses are used without consistent status checks and exception handling.

6. **Platform-specific hardcoded file paths**
   - Multiple `/Users/...` paths make the script non-portable and difficult to run outside one machine/account layout.

7. **Deprecated OpenAI API usage**
   - Uses legacy completion model (`text-davinci-003`) patterns.

## Functional correctness concerns

- `add_mockup()` uses `alt_text: title`, but `title` is not a local parameter.
- `upload_folder()` computes `folder_name` but uses `the_folder` global instead.
- `retrieve_first_url()` can return `new_filename` before guaranteed assignment in all branches.
- `scroll_to_top()` function name and behavior mismatch (it scrolls to bottom repeatedly).

## Recommended first refactor steps

1. Move all secrets to environment variables (`os.environ`) and fail fast if missing.
2. Remove duplicate script body and split into modules:
   - `discord_client.py`
   - `image_pipeline.py`
   - `etsy_client.py`
   - `main.py`
3. Replace global state with explicit function parameters / return values.
4. Add a `requests.Session()` with helper methods for retries, timeout, and status checking.
5. Replace fixed sleeps with explicit Selenium waits (`WebDriverWait` + expected conditions).
6. Centralize config paths and use `pathlib.Path` for portability.
7. Add structured logging and per-item exception boundaries so one failure does not kill the entire batch.

## Minimal safety checklist before production use

- [ ] Rotate all leaked keys/tokens/secrets immediately.
- [ ] Add `.env` loading and a `.env.example` template.
- [ ] Add dry-run mode for Etsy listing creation.
- [ ] Add idempotency checks to avoid duplicate listing creation.
- [ ] Add unit tests for utility methods (`convert_webp_to_png`, crop ratio math, metadata builders).
- [ ] Add integration smoke tests with mocked APIs.

