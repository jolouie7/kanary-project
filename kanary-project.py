# sync api but can be used in async mode
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def main():
    # context manager
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto('https://golookup.com/')

        try:
            # Fill out the search form
            fill_first_name(page, 'kevin')
            fill_last_name(page, 'lee')
            select_state(page)
            page.click('button[type=submit]')
        except:
            raise Exception('Failed to fill out form')

        # Close both modals
        location_modal_skip_btn = page.wait_for_selector(
            'button:has-text("Skip")', timeout=50000)
        location_modal_skip_btn.click()

        notification_close_btn = page.wait_for_selector(
            '//*[@id="content"]/div/button', timeout=50000)
        notification_close_btn.click()

        try:
            success_text = page.wait_for_selector(
                '//*[@id="content"]/section/div/section/div[1]/div[1]/h3')

            # No records found page
            if not success_text and page.wait_for_selector('//*[@id="content"]/div[2]/div/div/div/div'):
                print('No results found!!')

            # Get the headline text
            headline = page.inner_text('div.headline h3')

            print('headline: ', headline)
        except:
            print("An error has occurred")
            raise Exception("An error has occurred")


def fill_first_name(page, first_name):
    try:
        page.fill('input.frm-fld-w1', f'{first_name}')
    except:
        raise Exception("Error in first name")


def fill_last_name(page, last_name):
    try:
        page.fill('input.frm-fld-w2', f'{last_name}')
    except:
        raise Exception("Error in last name")


def select_state(page, state=None):
    try:
        if state is None:
            return
        else:
            page.select_option('select[name="state"]', state)
    except:
        raise Exception("Error selecting state")


if __name__ == '__main__':
    main()
